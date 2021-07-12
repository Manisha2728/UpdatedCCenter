from .base import *
from .common import *
from .cvtables import *
from .collaborate_patient_search import *
from .apps_patient_display import *
from .cv_patient_display import *
from .ppol_general import *
from .db_files import *
from .apps_reporting import *
from .clinical_viewer_general import *
from .clinical_domain_laboratory import *
from .vpo import *
from .direct_messaging_acdm import *
from .clinical_code_display import *
from .operational_manager import *
from .ehragent import *
from .ehragent_clinical_domains import *
from .ehragent_categories import *
from .ehragent_measurements import *
from .version_manager import *
from .agentpp_hosted_app import *
from .capsule import *
from .system_parameters import *
from .patient_view import *
from dbmconfigapp.models.base import ModelDescriptor, Service, Component
from dbmconfigapp.models.tracking import *



######### Model related helper methods ############

def add_to_model_descriptor(model, services_codes, export_in_api= True):
    # A helper method for adding a new model descriptor
    # Use services_codes argument as a list of codes. e.g. ['VPO', 'EHRAgent']
    model_name = model._meta.db_table
    md, _ = ModelDescriptor.objects.get_or_create(model_name = model_name)
    md.export_in_api = export_in_api
    md.save()
    md.services = [Service.objects.get(code_name=s) for s in services_codes]

def findServiceByCodeName(code_name):        
    return Service.objects.filter(code_name=code_name)[0]

def findComponentByVerboseName(verbose_name):        
    return Component.objects.filter(verbose_name=verbose_name)[0]

def add_to_model_descriptor2(model_name, services_codes, export_in_api= True):
    # A helper method for adding a new model descriptor
    # Use services_codes argument as a list of codes. e.g. ['VPO', 'EHRAgent']
    md, created = ModelDescriptor.objects.get_or_create(model_name = model_name)
    md.export_in_api = export_in_api
    md.save()
    slist = [Service.objects.get(code_name=s) for s in services_codes]
    if not created:
        slist.extend(list(md.services.all()))
    md.services.set(slist)

def add_service_to_existing_model(model, service_codes_list):
    # get the model
    model_name = model._meta.db_table
    md = ModelDescriptor.objects.get(model_name = model_name)
    # get the real service list 
    service_list = [Service.objects.get(code_name=s) for s in service_codes_list]
    # extend it with the existing services attached to the model
    service_list.extend(list(md.services.all()))
    md.services = service_list

    
    