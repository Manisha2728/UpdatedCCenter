from dbmconfigapp.models.base import ModelDescriptor, Service, Component

def findServiceByCodeName(code_name):        
    return Service.objects.filter(code_name=code_name)[0]

def findComponentByVerboseName(verbose_name):        
    return Component.objects.filter(verbose_name=verbose_name)[0]

def add_to_model_descriptor(model_name, services_codes, export_in_api= True):
    # A helper method for adding a new model descriptor
    # Use services_codes argument as a list of codes. e.g. ['VPO', 'EHRAgent']
    md, created = ModelDescriptor.objects.get_or_create(model_name = model_name)
    md.export_in_api = export_in_api
    md.save()
    md.services = [findServiceByCodeName(s) for s in services_codes]