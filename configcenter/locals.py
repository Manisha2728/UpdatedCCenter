import os
PROJECT_DIR =  os.path.join(os.path.dirname(__file__), '../')
debug = True
version = '7.0' 
db_name = 'dbmCCenter_NewDjango' #'dbmCCenterAlla_Test'
db_host = 'ph-aio-64\INST01' #'du-cc-sql\INST01' 
dbm_shared_folder = os.path.realpath(os.path.join(PROJECT_DIR, 'shared_folder_dev')) 
usage_reporting_server = 'dbm-cc-aio1'
usage_reporting_path = r'c:\Program Files\Microsoft SQL Server\MSRS11.INST02\Reporting Services'
security_webapi_url = 'http://localhost/Security/api/'

cag_db_name = 'dbmADRLV3'
cag_sql_server_name = 'du-cc-sql\INST01'

environment_size = 'Small'