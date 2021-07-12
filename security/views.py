from django.http import HttpResponse
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPSocketOpenError
from django.views.decorators.csrf import csrf_exempt
import logging
from dbmconfigapp.utils import encryption

@csrf_exempt
def test_connection(request):
    msg = ''
    logger = logging.getLogger('django')
    
    try:
    
        domain = request.POST.get('domain')
        if not domain:
            raise Exception('Domain not specified')
        
        
        server = Server(domain, get_info=ALL)
        port = request.POST.get('port')
        if port:
            try:
                server.port = int(port)
            except Exception as ex:
                raise Exception('The Port should be a whole number')
        
        container = request.POST.get('container')
        # use default container if not found
        if not container:
            container = 'cn=Users'
            domainArray = domain.split('.')
            for domainPart in domainArray:
                container = container + ',dc=' + domainPart
        conn = Connection(server, container)
        
        is_untrusted = request.POST.get('is_untrusted') == 'true'
        #if is_untrusted:
        user = request.POST.get('user')
        password = request.POST.get('password')
        if (user and password) or is_untrusted:
            conn.user = user if '\\' in user else domain + '\\' + user
            encryptor = encryption.Encryptor()
            conn.password = encryptor.decrypt(request.POST.get('password'))
            conn.authentication = NTLM
        
        result = False
        if conn.bind():
            try:
                result = conn.search(container, '(objectclass=person)')
            except KeyError as keyError:
                msg = ' Container might be incorrect.' 
            msg = 'Connection established but query failed.%s' % msg  # will be used only if result=False
        else:
            msg = 'Could not connect to the server: %s' % conn.last_error
        
        if result:
            return HttpResponse('<span class="successmessage">Test succeeded.</span>')
    
    except LDAPSocketOpenError as socketError:
        logger.error("Test Connection failed.\n{0}".format(socketError))
        msg = 'Socket error occured. See dbMotion CCenter event log for details.'
        
    except Exception as e:
        msg = str(e).capitalize()
    
    msg = msg if msg.endswith('.') else msg+'.'
    return HttpResponse('<span class="errormessage">%s</span>' % msg)
    
    