from django.http import HttpResponse
from configcenter.settings import get_param
from django.utils import timezone
import xml.etree.ElementTree as ET
from time import gmtime, strftime
from datetime import datetime

# Apply changes - update communication file
def apply_changes(request):
    try:
        #now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        federationFile = get_param('dbm_shared_folder') + '\Communication\Configuration\FederationSitesConfig.xml'
        xmldoc=ET.parse(federationFile)
        FederationSitesConfig = xmldoc.getroot()
        FederationSitesConfig.attrib['CCenterTimestamp'] = str(now)
        xmldoc.write(federationFile)
    
        return HttpResponse('<span class="successmessage">Applied</span>')
    
    except IOError as io:
        return HttpResponse('<span class="errormessage">%s: %s</span>' % (io.strerror, io.filename))

    except Exception as e:
        return HttpResponse('<span class="errormessage">%s</span>' % e)
    
    