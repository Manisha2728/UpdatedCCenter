from dbmconfigapp.models.base import *
from django.db.models.signals import post_save 
from django.dispatch import receiver
import xml.etree.ElementTree as ET
import shutil, sys, os, logging
from django.core import validators
from configcenter.settings import get_param

AUDITING_TYPE_CHOICES = (
    (0, 'Enable suspicious activity auditing'),
    (1, 'Enable suspicious activity and application authorized user auditing'),
    (999, 'No auditing')
    )

# Calculating 40 MB * Customer size + 3.2 GB
def GetCDRAuthorizedUsersSize():
    env_size = settings.get_param('environment_size')
    b = env_size.lower()
    if(b == 'small'):    
        return 7000                  #cal 40 * 4000 + 3200
    elif(b == 'medium'):
        return 25000                 #cal 40 * 20000 + 3200
    elif(b == 'large'): 
        return 180000                 #cal (40 * 175000) + 3200 
    
  

# tbener 14/6/2018: changed to shared folder support.
# tbener 16/6/2016: moved here from settings.py with try - except in order
# to better handle a bad SSRS parameters intializing
def GetReportingServicesSharedPath():
    logger = logging.getLogger('django')

    server = settings.get_param('usage_reporting_server')
    shared_folder = settings.get_param('usage_reporting_shared_folder', 'ReportServer')
    
    try:
        return r'\\{server}\{folder}'.format(server=server, folder=shared_folder)
    except Exception as e:
        str_err = """
An error occurred while trying to build SSRS configuration file path (rsreportserver.config).
This usually happens because of not initializing parameters properly or not setting the correct shared folder:
usage_reporting_server = {0}
shared_folder = {1}
This impacts only the Usage Reports Settings page.
            """.format(server, shared_folder)
        #print("Error in dbmconfigapp.models.operational_manager.GetReportingServicesSharedPath():\n{0}" % str_err)
        logger.error("{0}\nFull error:\n{1}".format(str_err, e))
        return ""


ERR_SSRS_APPLY = "An error occurred while trying to apply the configuration: %s"
SSRS_COFIG_FILE = os.path.join(GetReportingServicesSharedPath(), r'\rsreportserver.config')


class Status():
    none = 'none'
    to_apply = 'to_apply'
    applied = 'applied'
    error = 'error'
    not_applied = 'not_applied'



class OperationalManagerPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Usage Reports'

class UsageReports(ConfigurationEntityBaseModel):
    parent                  = models.ForeignKey('OperationalManagerPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    smtp_url            = models.CharField(max_length=512, verbose_name='SMTP URL', default='db-cas', null=True, blank=True)
    smtp_port           = models.IntegerField(verbose_name='SMTP port', null=True, blank=True, default=25, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(65536)] )
    from_address        = models.EmailField(null=True, blank=True, default='ReportingServices@dbMotion.com')
    status               = models.CharField(max_length=20, null=True, blank=True)
    message               = models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
        # This will stand for the row in history log 
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'Usage Reports'
        verbose_name_plural = 'Usage Reports'
        
        
    def apply_configuration(self):
        root = None
        
        def update_value(value, xpath):
            if value==None: value=''
            node = root.find(xpath)
            node.text = str(value)
            
        try:
            tree = ET.parse(SSRS_COFIG_FILE)
            root = tree.getroot()
            shutil.copyfile(SSRS_COFIG_FILE, SSRS_COFIG_FILE + ".backup")
            
            update_value(self.smtp_url      , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/SMTPServer")
            update_value(self.smtp_port     , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/SMTPServerPort")
            update_value(self.from_address  , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/From")
            
            # update static values (ST-837)
            update_value(False  , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/SendEmailToUserAlias")
            update_value(2      , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/SendUsing")
            update_value(0      , "Extensions/Delivery/Extension[@Name='Report Server Email']/Configuration/RSEmailDPConfiguration/SMTPAuthenticate")
            
            tree.write(SSRS_COFIG_FILE)
            self.status = 'applied'
            self.message = 'The configuration was applied successfully.'
        except IOError as strerror:
            print ("Error in models.UsageReports.apply_configuration(): {0}" % "I/O error({0})".format(strerror))
            self.status = 'error'
            self.message = ERR_SSRS_APPLY % ("{0} (I/O)".format(strerror))
        except:
            print("Error in models.UsageReports.apply_configuration(): %s" % sys.exc_info()[0])
            self.status = 'error'
            self.message = ERR_SSRS_APPLY % sys.exc_info()[0]





# When saving UsageReports the save_to_file() method is executed.
# Use this saving_flag to avoid infinite loop.
saving_flag = 0

@receiver(post_save, sender=UsageReports)
def save_to_file(sender, instance=False, **kwargs):
    global saving_flag
    if saving_flag == 1:
        saving_flag = 0
        return
    
    instance.message = ''
    
    if instance.status == Status.to_apply:
        # save data to configuration file
        instance.apply_configuration()
    elif instance.status == Status.none:
        # after applied and message displayed
        return
    
    saving_flag = 1    
    instance.save()

class DataAccessAuditingPage(PageBaseModel):
    help_text_1         = models.TextField(blank=True, default='Use this configuration to audit database access.')

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'CDR Instance Data Access Auditing'

class DataAccessAuditing(ConfigurationEntityBaseModel):
    parent              = models.ForeignKey('DataAccessAuditingPage', on_delete=models.SET_NULL, null=True, editable=False, default=1)
    auditing_type       = models.IntegerField(verbose_name='', choices=AUDITING_TYPE_CHOICES, default=0, help_text=get_help_text("""
        Suspicious activity is any access to the database by non-dbMotion service accounts.<br/>
        Application authorized users are dbMotion application service accounts.""", 'Enable suspicious activity auditing'))
    suspected_max_storage_size = models.IntegerField(verbose_name='Suspicious activity auditing files maximum storage(in MB)', default=500, validators=[validators.MinValueValidator(50),])    
    authorized_max_storage_size    = models.IntegerField(verbose_name='Authorized activity auditing files maximum storage(in MB)', default=GetCDRAuthorizedUsersSize, validators=[validators.MinValueValidator(50),], help_text=get_help_text("""<br/>
        SQL Server audit files are kept in the file system.<br/> 
        Specify the maximum storage limit to keep disk space use under control.<br/> 
        After the limit reached, SQL Server overwrites the current files.<br/>
        Default calculated according to expected amount of activity."""))    
    server_principals = models.TextField(verbose_name= 'Authorized User Name', default='', max_length= 500, null=False, help_text=get_help_text("""
    Users listed are not monitored for suspicious activites.<br/>
    Use comma seperated list of users in a format domain\\user name, domain\\user name, ..."""))    
    def __unicode__(self):
        # This will stand for the row in history log 
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'CDR Data Access Auditing'
        verbose_name_plural = 'CDR Data Access Auditing'

class CAGDataAccessAuditing(ConfigurationEntityBaseModel):
    parent              = models.ForeignKey('CAGDataAccessAuditingPage', on_delete=models.SET_NULL, null=True, editable=False, default=1)
    auditing_type       = models.IntegerField(verbose_name='', choices=AUDITING_TYPE_CHOICES, default=0, help_text=get_help_text("""
        Suspicious activity is any access to the database by non-dbMotion service accounts.<br/>
        Application authorized users are dbMotion application service accounts.""", 'Enable suspicious activity auditing'))
    suspected_max_storage_size = models.IntegerField(verbose_name='Suspicious activity auditing files maximum storage(in MB)', default=500, validators=[validators.MinValueValidator(50),])    
    authorized_max_storage_size    = models.IntegerField(verbose_name='Authorized activity auditing files maximum storage(in MB)', default=500, validators=[validators.MinValueValidator(50),], help_text=get_help_text("""<br/>
        SQL Server audit files are kept in the file system.<br/> 
        Specify the maximum storage limit to keep disk space use under control.<br/> 
        After the limit reached, SQL Server overwrites the current files.<br/>
        Default calculated according to expected amount of activity.""", '500'))    
    server_principals = models.TextField(verbose_name= 'Authorized User Name', default='', max_length= 500, null=False, help_text=get_help_text("""
    Users listed are not monitored for suspicious activites.<br/>
    Use comma seperated list of users in a format domain\\user name, domain\\user name, ..."""))    
    def __unicode__(self):
        # This will stand for the row in history log 
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'CAG Data Access Auditing'
        verbose_name_plural = 'CAG Data Access Auditing'

class CAGDataAccessAuditingPage(PageBaseModel):
    help_text_1         = models.TextField(blank=True, default='Use this configuration to audit database access.')

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'CAG Instance Data Access Auditing'
