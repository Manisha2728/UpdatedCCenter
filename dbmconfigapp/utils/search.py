from bs4 import BeautifulSoup, Comment
import os
from configcenter import settings
import urllib, base64
import sys, logging

#===============================================================================
# to execute: python manage.py shell < dbmconfigapp/utils/search.py
#===============================================================================
def main():
    base_url = 'localhost:8000'
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    print(base_url)
    save_pages_to_files(base_url)
    pass
    
if __name__ == '__main__':
    main()

# syntax: 'file name':  [('Name in tree'  , 'url', u'path in tree (without page name)'), ],
PAGES_INFO = {
    'Allergies.htm':            [('Allergies'            , '/admin/dbmconfigapp/clinicaldomainallergies/1/', u'Clinical Viewer\Clinical Domains'), ],
    'Clinical Documents.htm':   [('Clinical Documents'   , '/admin/dbmconfigapp/clinicaldomaindocuments/18/', u'Clinical Viewer\Clinical Domains'), ],
    'Demographics.htm':         [('Demographics'         , '/admin/dbmconfigapp/clinicaldomaindemographics/12/', u'Clinical Viewer\Clinical Domains'), ],
    'Diagnoses.htm':            [('Diagnoses'            , '/admin/dbmconfigapp/clinicaldomaindiagnoses/3/', u'Clinical Viewer\Clinical Domains'), ],
    'Encounters.htm':           [('Encounters'           , '/admin/dbmconfigapp/clinicaldomainencounters/7/', u'Clinical Viewer\Clinical Domains'), ],
    'Encounters Details.htm':   [('Encounters Details'   , '/admin/dbmconfigapp/clinicaldomainencounterdetails/8/', u'Clinical Viewer\Clinical Domains'), ],
    'Imaging.htm':              [('Imaging'              , '/admin/dbmconfigapp/clinicaldomainimaging/17/', u'Clinical Viewer\Clinical Domains'), ],
    'Immunizations.htm':        [('Immunizations'        , '/admin/dbmconfigapp/clinicaldomainimmunizations/4/', u'Clinical Viewer\Clinical Domains'), ],
    'Labs.htm':    [('Labs'    , '/admin/dbmconfigapp/clinicaldomainlaboratory/16/', u'Clinical Viewer\Clinical Domains'), ],
    'Lab Results.htm':    [('Lab Results'    , '/admin/dbmconfigapp/clinicaldomainlabresults/19/', u'Clinical Viewer\Clinical Domains'), ],
    'Lab Results History.htm':    [('Lab Results History'    , '/admin/dbmconfigapp/clinicaldomainlabresultshistory/15/', u'Clinical Viewer\Clinical Domains'), ],
    'Medications.htm':    [('Medications'    , '/admin/dbmconfigapp/clinicaldomainmedications/6/', u'Clinical Viewer\Clinical Domains'), ],
    'Pathology.htm':    [('Pathology'    , '/admin/dbmconfigapp/clinicaldomainpathologies/5/', u'Clinical Viewer\Clinical Domains'), ],
    'PLV.htm':    [('PLV'    , '/admin/dbmconfigapp/clinicaldomainplv/9/', u'Clinical Viewer\Clinical Domains'), ],
    'Problems.htm':    [('Problems'    , '/admin/dbmconfigapp/clinicaldomainproblems/2/', u'Clinical Viewer\Clinical Domains'), ],
    'Procedures.htm':    [('Procedures'    , '/admin/dbmconfigapp/clinicaldomainprocedures/11/', u'Clinical Viewer\Clinical Domains'), ],
    'Summary.htm':    [('Summary'    , '/admin/dbmconfigapp/clinicaldomainsummary/10/', u'Clinical Viewer\Clinical Domains'), ],
    'Vitals.htm':    [('Vitals'    , '/admin/dbmconfigapp/clinicaldomainvitals/13/', u'Clinical Viewer\Clinical Domains'), ],
    'Clinical Code Display.htm':    [('Clinical Code Display'    , '/admin/dbmconfigapp/clinicalcodedisplaypage/1/', u'Clinical Viewer'),
                                     ('Clinical Code Display'    , '/admin/dbmconfigapp/plclinicalcodedisplaypage/1/', u'Patient List'),
                                     ('Clinical Code Display'    , '/admin/dbmconfigapp/pvclinicalcodedisplaypage/1/', u'Patient View'),],
    'Clinical Viewer General.htm':    [('General Definitions'    , '/admin/dbmconfigapp/clinicalviewergeneralpage/1/', u'Clinical Viewer'), ],
    'Patient Display.htm':    [('Patient Display'    , '/admin/dbmconfigapp/cvpatientdisplaypage/1/', u'Clinical Viewer'),
                               ('Patient Display'    , '/admin/dbmconfigapp/plpatientdisplaypage/1/', u'Patient List'),
                                ],
    'Patient Display for Agent.htm': [
                               ('Patient Display'    , '/admin/dbmconfigapp/pvpatientdisplaypage/1/', u'Agent Hub'),
                                ],
    'Patient Search.htm':    [('Patient Search'    , '/admin/dbmconfigapp/cvpatientsearch/14/', u'Clinical Viewer'),
                              ('Patient Search'    , '/admin/dbmconfigapp/pvpatientsearchpage/1/', u'Agent '),],
    'Reporting.htm':    [('Reporting'    , '/admin/dbmconfigapp/cvreportingpage/1/', u'Clinical Viewer'),
                         ('Reporting'    , '/admin/dbmconfigapp/plreportingpage/1/', u'Patient List'),
                         ('Reporting'    , '/admin/dbmconfigapp/pvreportingpage/1/', u'Patient View'), ],
    'ACDM.htm':    [('ACDM'    , '/admin/dbmconfigapp/directmessagingacdmpage/1/', u'Direct Messaging'), ],
    'CCDA Export.htm':    [('CCDA'    , '/admin/dbmconfigapp/dataexportccdadisplaypage/1/', u'Data Export'), ],
    'CCDA Display and Report.htm':    [('CCDA Display and Report'    , '/admin/dbmconfigapp/cvccdadisplaypage/1/', u'Clinical Viewer'), 
                                      ('CCDA Display and Report'    , '/admin/dbmconfigapp/pvccdadisplaypage/1/', u'Patient View'), ],
    'Usage Reports.htm':    [('Usage Reports'    , '/admin/dbmconfigapp/operationalmanagerpage/1/', u'Operational Manager'), ],
    'Data Access Auditing.htm':    [('CDR Instance Data Access Auditing'    , '/admin/dbmconfigapp/dataaccessauditingpage/1/', u'Operational Manager'), ],
    'CAG Data Access Auditing.htm':    [('CAG Instance Data Access Auditing'    , '/admin/dbmconfigapp/cagdataaccessauditingpage/1/', u'Operational Manager'), ],
    'Clinical Domains.htm':    [('Clinical Domains'    , '/admin/dbmconfigapp/pvclinicaldomainpage/1/', u'Patient View'),],
    'AgentHub General Definitions.htm':    [('General Definitions'    , '/admin/dbmconfigapp/agenthubgeneralpage/1/', u'Agent Hub'), ],                           
    'Agent Hosted Apps.htm':    [('Hosted Applications'    , '/admin/dbmconfigapp/agentpphostedapppage/1/', u'Agent Hub'), ],
    'EHR Integration - EHR list.htm':    [('EHRs'    , '/admin/externalapps/ehr/', u'Agent Hub\EHR Integration'), ],
    'EHR Integration - EHR.htm':    [('Add EHR'    , '/admin/externalapps/ehr/add/', u'Agent Hub\EHR Integration'), ],
    'EHR Integration - Instance list.htm':    [('EHR Instances'    , '/admin/externalapps/instance/', u'Agent Hub\EHR Integration'), ],
    'EHR Integration - Instance.htm':    [('Add EHR Instance'    , '/admin/externalapps/instance/add/', u'Agent Hub\EHR Integration'), ],
    'EHR Agent Installation Profiles List.htm':    [('Installation Profiles'    , '/admin/externalapps/installationprofile/', u'Agent Hub'), ],
    'EHR Agent Installation Profile.htm':    [('Add Installation Profile'    , '/admin/externalapps/installationprofile/add/', u'Agent Hub'), ],
    'EHR Integration - Properties Package list.htm':    [('Properties Packages'    , '/admin/externalapps/instanceproperties/', u'Agent Hub\EHR Integration'), ],
    'EHR Integration - Properties Package.htm':    [('Add Properties Package'    , '/admin/externalapps/instanceproperties/add/', u'Agent Hub\EHR Integration'), ],
    'EHR Integration - AppID.htm':    [('Add Application ID'    , '/admin/externalapps/appid/add/', u'Agent Hub\EHR Integration'), ],
    'EMPI General.htm':    [('General Definitions'    , '/admin/via/viapage/1/', u'EMPI'), ],
    'EMPI Initiate.htm':    [('Initiate'    , '/admin/via/initiatepage/1/', u'EMPI'), ],
    'EMPI Initiate Mappings.htm':    [('Initiate Mappings'    , '/admin/via/initiatemappingspage/1/', u'EMPI'), ],
    'EMPI Authority Systems.htm':    [('Authority Systems'    , '/admin/via/authoritysystemspage/1/', u'EMPI'), ],
    'EMPI Provider Registry.htm':    [('Provider Registry'    , '/admin/via/empippolgeneralpage/1/', u'EMPI'), ],
    'AD Providers.htm':    [('Managed Users'    , '/admin/security/adproviders/', u'Security'), ],
    'AD Providers_form.htm':    [('Add Active Directory Provider'    , '/admin/security/adproviders/add/', u'Security'), ],
    'Application Domain Qualifiers.htm':    [('Unmanaged Users'    , '/admin/security/applicationdomains/', u'Security'), ],
    'Application Domain Qualifiers_form.htm':    [('Add Application Domain Qualifier'    , '/admin/security/applicationdomains/add/', u'Security'), ],
    'Applications Role Mapping.htm':    [('Role Mapping'    , '/admin/security/applications/', u'Security'), ],
    'Applications Role Mapping_form.htm':    [('Add Role Mapping'    , '/admin/security/applications/add/', u'Security'), ],
    'Security General Definitions.htm':    [('General Definitions'    , '/admin/security/securitygeneralpage/1/', u'Security'), ],
    'Federation Node List.htm':    [('Nodes'    , '/admin/federation/node/', u'Federation'), ],
    'Federation Node.htm':    [('Add Node'    , '/admin/federation/node/add/', u'Federation'), ],
    'Federation Group.htm':    [('Add Group'    , '/admin/federation/group/add/', u'Federation'), ],
    'Data Loading Partitioning.htm':    [('Partitioning'   , '/admin/dataloading/partitioningpage/1/', u'Data loading'), ],
    'Data Loading BatchLoading.htm':    [('Batch Loading'   , '/admin/dataloading/batchloadingpage/1/', u'Data loading'), ],
    'PatientList General Definitions.htm':    [('General Definitions'   , '/admin/dbmconfigapp/plgeneralpage/1/', u'Patient List'), ],
    'Capsule.htm':    [('Capsule'   , '/admin/dbmconfigapp/capsulepage/1/', u'Capsule'), ],
    'MyHR Connectivity.htm':    [('MyHR'    , '/admin/dbmconfigapp/myhrconnectivitypage/1/', u'MyHR Connectivity'), ],
    'PV General Definitions.htm':    [('General Definitions'    , '/admin/dbmconfigapp/patientviewpage/1/', u'Patient View'), ],
    'Measurements.htm': [('Measurements', '/admin/dbmconfigapp/pvmeasurementpage/1/', u'Patient View'), ],
    'Direct Addresses.htm': [('Direct Addresses', '/admin/externalapps/directaddressendpointspage/1/', u'Direct Messaging'), ],
    'Documents Search.htm': [('Documents Search', '/admin/dbmconfigapp/documentsearchgeneral/1/', u'Documents Search'), ],
    'Document Search Bootstrap.htm': [('Bootstrap Indexing', '/admin/dbmconfigapp/documentsearchbootstrap/1/', u'Documents Search'), ],
    'Document Search Live Feeds.htm': [('Live-Feed Indexing', '/admin/dbmconfigapp/documentsearchlivefeeds/1/', u'Documents Search'), ],
    'Carequality_Integration_Settings.htm': [('Carequality Integration', '/admin/dbmconfigapp/carequalityintegrationsettingspage/1/', u'Patient View'), ],
}




def read_page(base_url, key):
    response = urllib.request.urlopen(u'http://%s%s' % (base_url, PAGES_INFO[key][0][1]))
    soup = BeautifulSoup(response.read())
    return clean_soup(soup)

# Still can't login. probably need csrf
#-------------------------------------------------
# auth_handler = urllib2.HTTPBasicAuthHandler()
# auth_handler.add_password('realm', u'http://127.0.0.1:8000/', 'admin', '123')
# opener = urllib2.build_opener(auth_handler)
# urllib2.install_opener(opener)
# response = urllib2.urlopen(u'http://127.0.0.1:8000/admin/security/adproviders/')
# soup = BeautifulSoup(response.read())
# html = clean_soup(soup).prettify()

def save_pages_to_files(base_url):
#     request = urllib2.Request('http://%s/welcome/' % base_url)
#     base64string = base64.encodestring('%s:%s' % ('admin', '123')).replace('\n', '')
#     request.add_header("Authorization", "Basic %s" % base64string)   
#     result = urllib2.urlopen(request)
    
    base_path = os.path.normpath(os.path.join(settings.PROJECT_DIR, 'resources'))
    for key in PAGES_INFO:
        cleaned = read_page(base_url, key)
        html = cleaned.prettify()
        with open(os.path.join(base_path, key), "wb") as f:
            f.write(html)
    
    return None

# for debugging porpuses - saves the cleaned html files in a debug folder
def save_pages():
    base_path = os.path.normpath(os.path.join(settings.PROJECT_DIR, 'resources/html/debug'))
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    try:
        for fname, pinfo in PAGES_INFO.items():
            soup = pinfo[1]
            with open(os.path.join(base_path, fname), "wb") as f:
                f.write(soup.prettify().encode("UTF-8"))
    except:
        exc_class, exc, tb = sys.exc_info()
        new_exc = Exception('Error in page %s: %s' % (fname, exc or exc_class))
        raise new_exc.__class__
        
        
def clean_soup(soup):
#     contentdiv = soup.find('div', {'id': 'content'})
    contentdiv = soup.select('#content')[0]
    
    # strip the content div out for hidden elements
    to_del = contentdiv.select('div[style*="display:none;"]')
    [d.extract() for d in to_del]
    
    # script elements
    to_del = contentdiv.find_all('script')
    [d.extract() for d in to_del]
    
    # extra rows that django generates
    to_del = contentdiv.select('div[class~=empty-form]')
    [d.extract() for d in to_del]
    
    # comments
    to_del = contentdiv.find_all(text=lambda text:isinstance(text, Comment))
    [d.extract() for d in to_del]
    
    # all inputs
    to_del = contentdiv.find_all('input')
    [d.extract() for d in to_del]
    
    return contentdiv


files_loaded = False

#===============================================================================
# Read the files and save the content to search, in PAGES_INFO dictionary 
# TODO: handle second call (every call extends PAGES_INFO)
#===============================================================================
def read_search_files():
    global files_loaded
    global PAGES_INFO
    files_loaded = True
    base_path = os.path.normpath(os.path.join(settings.PROJECT_DIR, 'resources/html'))
    errors = []
    
    try:
        # read all files in dictionary
        for fname, pinfo in PAGES_INFO.items():
            f = os.path.join(base_path, fname)
            if not os.path.isfile(f):
                errors.append('File not found: %s' % fname)
            soup = BeautifulSoup(open(f))
            PAGES_INFO[fname] = (pinfo, clean_soup(soup))
    
    except Exception as e:
        errors.append('Error reading file %s - %s' % (fname, e))
    
    try:
        if settings.DEBUG:
            save_pages()
            # look for files not in dictionary
            for file_name in os.listdir(base_path): 
                if file_name.endswith('.htm'):
                    if not file_name in PAGES_INFO: errors.append('The file: %s is not in dictionary' % file_name)
                
    except Exception as e:
        errors.append('Error in saving files (debug): %s' % e)
        
    if errors:
        logger = logging.getLogger('django')
        for e in errors:
            print(e)
            logger.error(e)
        
        
    return errors
#     if errors:
#         HttpResponseRedirect('<b>Errors in search files:</b><br/>%s' % '<br/>'.join(errors))

import re


class result_page:
    link = ''
    name = ''
    texts = []
    
def go(search_string):
    search_results = []
    errors = None
    
    if not files_loaded: errors = read_search_files()
    # TODO: if errors:
    
    for fname, pinfo in PAGES_INFO.items():
        # for debugging
        # print(fname)
        element = pinfo[1]
        results = element.find_all(text=re.compile(re.escape(search_string), re.I))
        if results:
            for item in pinfo[0]:
                p = result_page()
                p.name = u'%s\%s' % (item[2], item[0])
                p.link = item[1]
                p.texts = results
                search_results.append(p)
                
    search_results = sorted(search_results, key=lambda k: k.name)
                
    return search_results, errors







