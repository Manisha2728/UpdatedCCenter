from dbmconfigapp.models.base import ModelDescriptor, Service, Component
import logging

def findServiceByCodeName(code_name):        
    return Service.objects.filter(code_name=code_name)[0]

def findComponentByVerboseName(verbose_name):        
    return Component.objects.filter(verbose_name=verbose_name)[0]

def add_to_model_descriptor(model_name, services_codes, export_in_api= True):
    # A helper method for adding a new model descriptor
    # Use services_codes argument as a list of codes. e.g. ['VPO', 'EHRAgent']
    md = ModelDescriptor()
    md.model_name = model_name
    md.export_in_api = export_in_api
    md.save()
    md.services = [findServiceByCodeName(s) for s in services_codes]

def log_exception(exception, initial_msg):
    initial_msg += '\n{0}'
    ex_msg = initial_msg.format(str(exception).capitalize())

    inner_ex = exception.InnerException
    while inner_ex != None:
        ex_msg+="\nInner Exception: {0}".format(str(inner_ex).capitalize())
        inner_ex = inner_ex.InnerException

    logger = logging.getLogger('django')
    logger.error(ex_msg)
