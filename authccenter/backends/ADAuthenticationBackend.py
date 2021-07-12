from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.utils import timezone
from ldap3 import Connection, Entry, NONE, Server

from authccenter.models.group import ADGroup
from authccenter.models.settings import SettingsModel
from authccenter.models.user import CCenterUser
from authccenter.signals import login_failure
from dbmconfigapp.utils import encryption
from security.models import ADProviders

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
        return "\n".join(ex.message for ex in self.exceptions)

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


# Error messages for the authentication custom exceptions.
class ErrorMessages(object):
    NO_USER_DATA = "Failure retrieving user '{}' information from Active Directory '{}'."

    NO_USER_GROUPS_CONFIGURED = "The user '{}' does not belong to any configured Active Directory groups."

    PASSWORD_DECRYPTION_FAILURE = "Failure decrypting password for user '{}'."

    ACTIVE_DIRECTORY_GROUPS_NOT_CONFIGURED = 'Active Directory groups not mapped to the configured groups in CCenter.'

    ACTIVE_DIRECTORIES_PROVIDERS_NOT_CONFIGURED = 'Active Directories are not configured in CCenter.'

    INVALID_USER_DOMAIN_NAME = 'The domain name {} given by user {} is not configured in CCenter.'

    USER_CONNECTION_FAILURE_TO_ACTIVE_DIRECTORY = "The user '{}' failed to establish connection to Active Directory '{}'."

    UNKNOWN_USERNAME_FORMAT = "Username '{}' not specified in known format.\nAccepted format:\n- username@domainname\n- netbiosdomainname\\username"

    NO_ACTIVE_DIRECTORY_MATCH_FOUND = "No Active Directories found matching the user '{}'."


def active_directory_connection_establishment(provider, username, password):
    # type: (ADProviders, str,  str) -> Union[Tuple[Connection,None],Tuple[None,Exception]]
    """
    Function to establish user connection to the given Active directory.
    :param provider: Ahe Active Directory provider.
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


def retrieve_user_information(provider, connection, username):
    # type: (ADProviders, str,  str) -> Union[Tuple[Entry, List[str],None],Tuple[None,None,Exception]]

    """
    Method to retrieve the user information from the Active Directory.
    :param provider: The Active Directory provider.
    :type provider: ADProviders
    :param connection: The connection to the Active Directory.
    :type connection: Connection
    :param username: The user username.
    :type username: str
    :return: The user information.
    :rtype: (Entry, [str], Exception)
    """
    try:
        # Create the container (base filter) if not exist.
        container = provider.container

        if not container:
            container = ','.join('dc=' + domain_name_part for domain_name_part in provider.domain_name.split('.'))

        # Build query to retrieve the user data.
        query = '(&(objectclass=user)(sAMAccountName=%s))' % username

        # Define the entry attributes to retrieve from the Active Directory.
        query_attributes = ['sAMAccountName']

        if provider.ad_mapping_FirstName:
            query_attributes.append(provider.ad_mapping_FirstName)
        if provider.ad_mapping_LastName:
            query_attributes.append(provider.ad_mapping_LastName)

        # Retrieve the user data.
        result = connection.search(container, query, attributes=query_attributes)

        # return error if could not retrieve the user data.
        if not result or not connection.entries:
            return None, None, Exception(ErrorMessages.NO_USER_DATA.format(username))

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
            return None, None, Exception(ErrorMessages.NO_USER_GROUPS_CONFIGURED.format(username))

        # Return the user information.
        return user, [entry.cn.value for entry in connection.entries], None

    # Return error in case of exception.
    except Exception as e:
        return None, None, e


def initialize_user(provider, user_data, user_groups):
    # type: (ADProviders, Entry, List[str]) -> CCenterUser
    """
    Function create or update user data.
    :param provider: The Active Directory provider.
    :type provider: ADProviders
    :param user_data: The user information record from Active Directory.
    :type user_data: Entry
    :param user_groups: list of user groups.
    :type user_groups: [str]
    :return: The user object.
    :rtype: CCenterUser

    """
    username = getattr(getattr(user_data, 'sAMAccountName', ''),'value','')



    # Configure data for user creation or update.
    defaults = {'first_name': getattr(getattr(user_data, provider.ad_mapping_FirstName, ''), 'value', ''),
                'last_name': getattr(getattr(user_data, provider.ad_mapping_LastName, ''), 'value', ''),
                'last_login': timezone.now()}

    # Convert username to UPN format.
    username = Backend.UPN_FORMAT.format(username, provider.domain_name)

    # Create or update user.
    user, created = CCenterUser.objects.update_or_create(username=username, defaults=defaults)
    user.groups = ADGroup.objects.filter(name__in=user_groups)
    user.save()
    user.django_login = False
    return user


def user_active_directory_authentication(provider, username, password):
    # type: (ADProviders, str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
    """
    Method used to do all the authentication of the user against the Active Directory.
    :param provider: The Active Directory provider to validate the user against.
    :type provider: ADProviders
    :param username: The user username.
    :type username: str
    :param password: The user password.
    :type password: str
    :return: The user object.
    :rtype: (CCenterUser, Exception)
    """
    # Get the user username.

    if '@' in username:
        user_username = username.split('@', 1)[0]
    elif '\\' in username:
        user_username = username.rsplit('\\', 1)[-1]
    else:
        user_username = username

    # Establish connection to Active Directory.
    connection, error = active_directory_connection_establishment(provider, username, password)

    if error:
        return None, ActiveDirectoryException(provider.domain_name, error)

    # Retrieve the user information.
    user_data, user_groups, error = retrieve_user_information(provider, connection, user_username)

    connection.unbind()
    if error:
        return None, ActiveDirectoryException(provider.domain_name, error)

    # Initialize the user object.
    return initialize_user(provider, user_data, user_groups), None


class Backend(object):
    DLN_FORMAT = '{}\\{}'

    UPN_FORMAT = '{}@{}'

    def single_active_directory_provider_login(self, provider, username, password):
        # type: (ADProviders, str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user if there only one Active Directory provider configured.
        :param provider: The Active Directory provider to validate the user against.
        :type provider: ADProviders
        :param username:
        :type username: str
        :param password:
        :type password: str
        :return: The user object.
        :rtype: (CCenterUser, Exception)
        """

        # If user try to log using UPN format (USER_NAME@DOMAIN_NAME)
        if '@' in username:
            user_username, user_domain_name = username.split('@', 1)

            if provider.domain_name.lower() != user_domain_name.lower():
                return None, Exception(ErrorMessages.INVALID_USER_DOMAIN_NAME.format(user_domain_name, user_username))

            return user_active_directory_authentication(provider, username, password)

        # If user try to log using DLN format (NETBIOS_DOMAIN_NAME\USER_NAME)
        elif '\\' in username:

            return user_active_directory_authentication(provider, username, password)

        # Complete the username.
        else:

            username = Backend.UPN_FORMAT.format(username, provider.domain_name)

            return user_active_directory_authentication(provider, username, password)

    def multiple_active_directory_providers_login(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user if multiple Active Directory providers configured.
        :param username: The user username.
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The user object
        :rtype: (CCenterUser, Exception)
        """

        # Return error if the username not provided in UPN or DLN format.
        if '@' not in username and '\\' not in username:
            return None, Exception(ErrorMessages.UNKNOWN_USERNAME_FORMAT.format(username))

        exception_collection = ActiveDirectoryExceptionCollection()

        # Check Active Directories based on what the user provided in the username.
        user, error = self.first_stage_authentication(username, password)

        if user:
            return user, None

        exception_collection.add(error)

        # Do do the next stage if the user enter the username in UPN format.
        if '@' in username:
            return None, exception_collection

        # Check Active Directories that netbios domain name not configured.
        user, error = self.second_stage_authentication(username, password)

        if user:
            return user, None

        exception_collection.add(error)

        # Check the remaining Active Directories
        user, error = self.third_stage_authentication(username, password)

        if user:
            return user, None

        exception_collection.add(error)

        return None, exception_collection

    def first_stage_authentication(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user against the Active Directory providers that matched the user username.
        :param username: The user username.
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The user object.
        :rtype: (CCenterUser,Exception)
        """

        # Match Active directories that match the domain name specified by the user.
        if '@' in username:
            return self.UPN_authentication(username, password)

        # Match Active directories that match the netbios domain name specified by the user.
        elif '\\' in username:
            return self.DLN_authentication(username, password)

        else:
            return None, Exception(ErrorMessages.UNKNOWN_USERNAME_FORMAT.format(username))

    def second_stage_authentication(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user against the Active Directory providers
        that the netbios domain name not configured.
        :param username: The user username.
        :type username:  str
        :param password: The user password.
        :type password:  str
        :return: The user object.
        :rtype: (CCenterUser,Exception)
        """
        exception_collection = ActiveDirectoryExceptionCollection()

        # Get all the Active Directory providers that the netbios domain name not configured.
        active_directory_providers = ADProviders.objects.filter(
            Q(netbios_domain_name__exact=None) | Q(netbios_domain_name=''))

        # Authenticate the user against each of the Active Directories.
        for active_directory_provider in active_directory_providers.all():
            user, error = user_active_directory_authentication(active_directory_provider, username, password)

            if user:
                return user, None

            exception_collection.add(ActiveDirectoryException(active_directory_provider.domain_name, error))

        return None, exception_collection

    def third_stage_authentication(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user against the Active Directory providers that not given in the previous stages.
        :param username: The user username.
        :type username:  str
        :param password: The user password.
        :type password:  str
        :return: The user object.
        :rtype: (CCenterUser,Exception)
        """

        exception_collection = ActiveDirectoryExceptionCollection()

        active_directory_providers = ADProviders.objects.all()  # type: QuerySet

        # Exclude Active Directory providers that given in the first stage.
        if '@' in username:
            user_username, user_domain_name = username.split('@', 1)
            active_directory_providers = active_directory_providers.exclude(domain_name=user_domain_name)
        elif '\\' in username:
            user_netbios_domain_name, user_username = username.rsplit('\\', 1)
            active_directory_providers = active_directory_providers.exclude(
                netbios_domain_name=user_netbios_domain_name)

        # Exclude Active Directory providers that given in the second stage.
        active_directory_providers = active_directory_providers.exclude(
            Q(netbios_domain_name__exact=None) | Q(netbios_domain_name=''))

        # Authenticate the user against each of the Active Directories.
        for active_directory_provider in active_directory_providers.all():
            user, error = user_active_directory_authentication(active_directory_provider, username, password)

            if user:
                return user, None

            exception_collection.add(ActiveDirectoryException(active_directory_provider.domain_name, error))

        return None, exception_collection

    def DLN_authentication(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user against the Active Directory providers matching the netbios domain name
        specified by the user
        :param username:  The user username in DLN format (NETBIOS_DOMAIN_NAME\\USERNAME)
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The user object.
        :rtype: (CCenterUser,Exception)
        """

        # Get the Active Directory providers matching the netbios domain name given by the user.
        user_netbios_domain_name, user_username = username.rsplit('\\', 1)
        active_directory_providers = ADProviders.objects.filter(netbios_domain_name=user_netbios_domain_name)

        exception_collection = ActiveDirectoryExceptionCollection()

        # Authenticate the user against each of the Active Directories.
        for active_directory_provider in active_directory_providers.all():
            user, error = user_active_directory_authentication(active_directory_provider, username, password)

            if user:
                return user, None

            exception_collection.add(ActiveDirectoryException(active_directory_provider.domain_name, error))

        return None, exception_collection

    def UPN_authentication(self, username, password):
        # type: (str, str) -> Union[Tuple[CCenterUser,None],Tuple[None,Exception]]
        """
        Method to authenticate the user against the Active Directory providers matching the domain name
        specified by the user
        :param username:  The user username in UPN format (USERNAME@DOMAIN_NAME)
        :type username: str
        :param password: The user password.
        :type password: str
        :return: The user object.
        :rtype: (CCenterUser,Exception)
        """

        # Get the Active Directory providers matching the domain name given by the user.
        user_username, user_domain_name = username.split('@', 1)
        active_directory_providers = ADProviders.objects.filter(domain_name=user_domain_name)

        exception_collection = ActiveDirectoryExceptionCollection()

        if not active_directory_providers.exists():
            exception_collection.add(Exception(ErrorMessages.NO_ACTIVE_DIRECTORY_MATCH_FOUND.format(username)))

        # Authenticate the user against each of the Active Directories.
        for active_directory_provider in active_directory_providers.all():
            user, error = user_active_directory_authentication(active_directory_provider, username, password)

            if user:
                return user, None

            exception_collection.add(ActiveDirectoryException(active_directory_provider.domain_name, error))

        return None, exception_collection

    def authenticate(self, username=None, password=None):
        # Invalid credentials
        if not username or not password:
            return None

        exceptions_collection = ActiveDirectoryExceptionCollection()

        if not SettingsModel.objects.setting().active_directory_mode:
            try:
                user = get_user_model().objects.get(username=username)
                if user.is_active:
                    error = ActiveDirectoryException("Offline:",
                                                     Exception("Incorrect password for user {}".format(username)))
                    exceptions_collection.add(error)
                else:
                    error = ActiveDirectoryException("Offline:",
                                                     Exception("No user found matching '{}'.".format(username)))
                    exceptions_collection.add(error)
            except:

                error = ActiveDirectoryException("Offline:", Exception("No user found matching '{}'.".format(username)))
                exceptions_collection.add(error)

        # Skip Authentication if no Active Directory providers configured.
        if not ADGroup.objects.exists():
            error = Exception(ErrorMessages.ACTIVE_DIRECTORY_GROUPS_NOT_CONFIGURED)
            exceptions_collection.add(error)
            login_failure.send(sender=self.__class__, username=username, exception=exceptions_collection)
            return None

        # Skip Authentication if no Active Directory groups configured.
        if not ADProviders.objects.exists():
            error = Exception(ErrorMessages.ACTIVE_DIRECTORIES_PROVIDERS_NOT_CONFIGURED)
            exceptions_collection.add(error)
            login_failure.send(sender=self.__class__, username=username, exception=exceptions_collection)

            return None

        # Try to decrypt password.
        try:
            encryptor = encryption.Encryptor()
            password = encryptor.decrypt(password)
        except Exception as e:
            exceptions_collection.add(e)
            login_failure.send(sender=self.__class__, username=username, exception=exceptions_collection)
            return None

        # Single Active Directory provider login procedure.
        if ADProviders.objects.count() == 1:
            user, error = self.single_active_directory_provider_login(ADProviders.objects.first(), username, password)
            exceptions_collection.add(error)
        # Multiple Active Directory providers login procedure.
        else:
            user, error = self.multiple_active_directory_providers_login(username, password)
            exceptions_collection.add(error)
        if not user:
            login_failure.send(sender=self.__class__, username=username, exception=exceptions_collection)
        return user

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
