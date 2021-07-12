from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.utils import timezone
from ldap3 import Connection, Entry, NONE, Server
import requests
import json

from authccenter.models.group import ADGroup
from authccenter.models.settings import SettingsModel
from authccenter.models.user import CCenterUser
from authccenter.signals import login_failure
from dbmconfigapp.utils import encryption
from security.models import ADProviders
from configcenter import settings

# For python type specification.
try:
    from typing import List, Tuple, Union
except ImportError:
    pass


class ActiveDirectoryException(Exception):

    def __init__(self, server, exception):
        super(ActiveDirectoryException, self).__init__()
        if isinstance(exception, ActiveDirectoryException):
            self.server = exception.server
            self.exception = exception.exception
            return

        self.server = server
        self.exception = exception

    @property
    def message(self):
        return "{}: {}".format(self.server, self.exception.message)

    @message.setter
    def message(self, value):
        pass

    def __str__(self):
        return self.message


class ActiveDirectoryExceptionCollection(Exception):

    def __init__(self):
        super(ActiveDirectoryExceptionCollection, self).__init__()
        self.exceptions = []

    @property
    def message(self):
        return "\n".join(str(ex.message) for ex in self.exceptions)

    @message.setter
    def message(self, value):
        pass

    def add(self, value):
        if isinstance(value, ActiveDirectoryExceptionCollection):
            self.exceptions += value.exceptions
            return

        self.exceptions.append(value)

    def __str__(self):
        return self.message

class ErrorMessages(object):
    NO_USER_DATA = "Failure retrieving user '{}' information from Active Directory '{}'."

    NO_USER_GROUPS_CONFIGURED = "The user '{}' does not belong to any configured Active Directory groups."

    ACTIVE_DIRECTORY_GROUPS_NOT_CONFIGURED = 'Active Directory groups not mapped to the configured groups in CCenter.'

    ACTIVE_DIRECTORIES_PROVIDERS_NOT_CONFIGURED = 'Active Directories are not configured in CCenter.'

    INVALID_USER_DOMAIN_NAME = 'The domain name {} given by user {} is not configured in CCenter.'

    USER_CONNECTION_FAILURE_TO_ACTIVE_DIRECTORY = "The user '{}' failed to establish connection to Active Directory '{}'."

    NO_ACTIVE_DIRECTORY_MATCH_FOUND = "No Active Directories found matching the user '{}'."

    USER_AUTHENTICATION_FAILED = "Authentication failed for user '{}'. For details see dbMotion Security log."

    AUTHENTICATION_REQUEST_FAILED = "Authentication request to the Security service failed for user '{}': "


class Backend(object):

    def __init__(self):
        self.exceptions_collection = ActiveDirectoryExceptionCollection()

    def authenticate(self, username=None, password=None):

        # Invalid credentials
        if not username or not password:
            return None

        try:
            self.handle_offline_authentication_error(username)

            if not self.check_security_configurations(username):
                return None

            encryptor = encryption.Encryptor()
            password = encryptor.decrypt(password)

            authenticated_user = self.authenticate_user_get_user_details(username, password)
            if not authenticated_user:
                return None

            user_groups, error = self.get_user_groups_from_ad(authenticated_user, password)

            if not user_groups:
                self.exceptions_collection.add(error)
                login_failure.send(sender=self.__class__, username=username, exception=self.exceptions_collection)
                return None

            user = self.initialize_user(authenticated_user, user_groups)

            return user

        except Exception as e:
            self.exceptions_collection.add(e)
            login_failure.send(sender=self.__class__, username=username, exception=self.exceptions_collection)
            return None

    def get_user(self, user_id):
        """
        Method used to get the user of the given id.
        :param user_id: the id of the user
        :type user_id: int
        :return: CCenterUser with the user id.
        :rtype: User
        """
        try:
            user = CCenterUser.objects.get(pk=user_id)
            if not user.is_active:
                return None

            user.django_login = False
            return user
        except CCenterUser.DoesNotExist:
            return None

    def handle_login_failed_error(self, username, error_message):
        error = Exception(error_message)
        self.exceptions_collection.add(error)
        login_failure.send(sender=self.__class__, username=username, exception=self.exceptions_collection)

    def handle_offline_authentication_error(self, username):

        if not SettingsModel.objects.setting().active_directory_mode:
            try:
                user = get_user_model().objects.get(username=username)
                if user.is_active:
                    error = ActiveDirectoryException("Offline:",
                                                     Exception("Incorrect password for user {}".format(username)))
                    self.exceptions_collection.add(error)
                else:
                    error = ActiveDirectoryException("Offline:",
                                                     Exception("No user found matching '{}'.".format(username)))
                    self.exceptions_collection.add(error)
            except:

                error = ActiveDirectoryException("Offline:", Exception("No user found matching '{}'.".format(username)))
                self.exceptions_collection.add(error)

    def check_security_configurations(self, username):
        error = None

        if not ADGroup.objects.exists():
            self.handle_login_failed_error(username, ErrorMessages.ACTIVE_DIRECTORY_GROUPS_NOT_CONFIGURED)

        if not ADProviders.objects.exists():
            self.handle_login_failed_error(username, ErrorMessages.ACTIVE_DIRECTORIES_PROVIDERS_NOT_CONFIGURED)

        return not error        

    def authenticate_user_get_user_details(self, username, password):
        # type: (str,  str) -> Dictionary
        """
        Function to send request to Security Service to authenticate user.
        :param username: The user username.
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The user details.
        :rtype: Dictionary
        """
        if(settings.DEBUG):
            url = settings.get_param('security_webapi_url') + 'authentication/login'
        else:
            url = 'https://localhost/dbMotionSecurity/api/authentication/login'

        response = requests.post(url, data={'UserName': username, 'Password': password, 'ApplicationName': 'CCenter'}, verify=False)
        if response.status_code != 200:
            error_message = ErrorMessages.AUTHENTICATION_REQUEST_FAILED.format(username)
            if(type(response.content) is str):
                error_message+= 'Response status code ' + str(response.status_code) + ' - ' + response.reason
            else:
                error_message+= response.content['ExceptionMessage']

            self.handle_login_failed_error(username, error_message)
            return None

        if response.content == 'null':
            error_message = ErrorMessages.USER_AUTHENTICATION_FAILED.format(username)
            self.handle_login_failed_error(username, error_message)
            return None

        return json.loads(response.content)

    def active_directory_connection_establishment(self, provider, username, password):
        # type: (ADProviders, str,  str) -> Union[Tuple[Connection,None],Tuple[None,Exception]]
        """
        Function to establish user connection to the given Active directory.
        :param provider: The Active Directory provider.
        :type provider: ADProviders
        :param username: The user username.
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The connection to the Active Directory.
        :rtype: (Connection, Exception)
        """
        try:
            # Define target Active Directory server
            server = Server(host=provider.domain_name, get_info=NONE)

            if provider.domain_port:
                server.port = provider.domain_port

            # Define connection to the target Active Directory
            connection = Connection(server, user=username, password=password)

            # Return error in case of failure establishing connection to the target Active Directory.
            if not connection.bind():
                return None, Exception(
                    ErrorMessages.USER_CONNECTION_FAILURE_TO_ACTIVE_DIRECTORY.format(username, provider.domain_name))

            # Return The connection.
            return connection, None

        # Return the error if exception raised.
        except Exception as e:
            return None, e

    def get_user_groups_from_ad(self, authenticated_user, password):
        # type: (Dictionary,  str) -> Union[Tuple[List[str],None],Tuple[None,Exception]]

        """
        Method to retrieve the user groups from the Active Directory.
        :param authenticated_user: authenticated user details.
        :type connection: Dictionary
        :param password: The user password.
        :type password: str
        :return: The user groups.
        :rtype: (Entry, [str], Exception)
        """
        username = authenticated_user['UserId']
        user_username, user_domain_name = username.split('@', 1)
        provider = ADProviders.objects.get(domain_name__iexact=user_domain_name)

        # Establish connection to Active Directory.
        connection, error = self.active_directory_connection_establishment(provider, username, password)

        if error:
            return None, ActiveDirectoryException(provider.domain_name, error)

        try:
            # Create the container (base filter) if not exist.
            container = provider.container

            if not container:
                container = ','.join('dc=' + domain_name_part for domain_name_part in provider.domain_name.split('.'))

            # Build query to retrieve the user data.
            query = '(&(objectclass=user)(sAMAccountName=%s))' % user_username

            # Define the entry attributes to retrieve from the Active Directory.
            query_attributes = ['sAMAccountName']

            # Retrieve the user data.
            result = connection.search(container, query, attributes=query_attributes)

            # return error if could not retrieve the user data.
            if not result or not connection.entries:
                return None, Exception(ErrorMessages.NO_USER_DATA.format(username))

            user = connection.entries[0]  # type: Entry

            user_dn = user.entry_get_dn()

            special_chars_ldap = {'*': '\\2a', '(': '\\28', ')': '\\29', '\\': '\\5c', 'NUL': '\\00', '/': '\\2f'}

            # Replace characters used by ldap.
            for special_char_ldap in special_chars_ldap:
                user_dn = user_dn.replace(special_char_ldap, special_chars_ldap[special_char_ldap])

            ad_groups_query = ''.join("(cn={})".format(ad_group)
                                      for ad_group in ADGroup.objects.values_list('name', flat=True))

            # Build query to retrieve the groups that the user belongs.
            query = '(&(ObjectClass=Group)(member:1.2.840.113556.1.4.1941:=%s)(|%s))' % (user_dn, ad_groups_query)

            # Retrieve the groups that the user belongs.
            result = connection.search(container, query, attributes=['cn'])

            # Return error if could not retrieve the groups that the user belongs.
            if not result or not connection.entries:
                return None, Exception(ErrorMessages.NO_USER_GROUPS_CONFIGURED.format(username))

            # Return the user groups.
            return [entry.cn.value for entry in connection.entries], None

        # Return error in case of exception.
        except Exception as e:
            return None, e
        finally:
            if(connection):
                connection.unbind()

    def initialize_user(self, user_data, user_groups):
        # type: (str, Entry, List[str]) -> CCenterUser
        """
        Function create or update user data.
        :param user_data: The user information record from Security service.
        :type user_data: Entry
        :param user_groups: list of user groups.
        :type user_groups: [str]
        :return: The user object.
        :rtype: CCenterUser

        """
        # Configure data for user creation or update.
        defaults = {'first_name': user_data['FirstName'],
                    'last_name':  user_data['LastName'],
                    'last_login': timezone.now()}

        # Create or update user.
        user, created = CCenterUser.objects.update_or_create(username=user_data['UserId'], defaults=defaults)
        user.groups = ADGroup.objects.filter(name__in=user_groups)
        user.save()
        user.django_login = False

        return user