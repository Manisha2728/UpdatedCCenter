USE [dbmCCenter]
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[spWriteStringToFile]') AND type in (N'P', N'PC'))
BEGIN
	EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE spWriteStringToFile
	 (
	@String Varchar(max), --8000 in SQL Server 2000
	@Path VARCHAR(8000),
	@Filename VARCHAR(8000)

	--
	)
	AS
	DECLARE  @objFileSystem int
			,@objTextStream int,
			@objErrorObject int,
			@strErrorMessage Varchar(1000),
			@Command varchar(8000),
			@hr int,
			@fileAndPath varchar(8000)

	set nocount on

	select @strErrorMessage=''opening the File System Object''
	EXECUTE @hr = sp_OACreate  ''Scripting.FileSystemObject'' , @objFileSystem OUT

	Select @FileAndPath=@path+''\''+@filename
	if @HR=0 Select @objErrorObject=@objFileSystem , @strErrorMessage=''Creating file "''+ @FileAndPath +''"''
	if @HR=0 execute @hr = sp_OAMethod   @objFileSystem   , ''CreateTextFile''
		, @objTextStream OUT, @FileAndPath,2,True

	if @HR=0 Select @objErrorObject=@objTextStream, 
		@strErrorMessage=''writing to the file "''+@FileAndPath+''"''
	if @HR=0 execute @hr = sp_OAMethod  @objTextStream, ''Write'', Null, @String

	if @HR=0 Select @objErrorObject=@objTextStream, @strErrorMessage=''closing the file "''+@FileAndPath+''"''
	if @HR=0 execute @hr = sp_OAMethod  @objTextStream, ''Close''

	if @hr<>0
		begin
		Declare 
			@Source varchar(255),
			@Description Varchar(255),
			@Helpfile Varchar(255),
			@HelpID int
	
		EXECUTE sp_OAGetErrorInfo  @objErrorObject, 
			@source output,@Description output,@Helpfile output,@HelpID output
		Select @strErrorMessage=''Error whilst ''
				+coalesce(@strErrorMessage,''doing something'')
				+'', ''+coalesce(@Description,'''')
		raiserror (@strErrorMessage,16,1)
		end
	EXECUTE  sp_OADestroy @objTextStream
	EXECUTE sp_OADestroy @objFileSystem'
END
GO
sp_configure 'show advanced options', 1; 
GO 
RECONFIGURE; 
GO 

sp_configure 'Ole Automation Procedures', 1;  
GO  
RECONFIGURE;

create table #TableFieldsMetadata (TableName varchar(1000), --COLLATE Latin1_General_CI_AS, 
FieldName varchar(1000), --COLLATE Latin1_General_CI_AS, 
DefaultValue varchar(1000), --COLLATE Latin1_General_CI_AS,
IsKey bit NULL)

----- INPUT DYNAMIC DATA HERE
INSERT INTO #TableFieldsMetadata
SELECT 'auth_group', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_group', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_group_permissions', 'group_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_group_permissions', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_group_permissions', 'permission_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'date_joined', '2021-06-03 10:59:51.170000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'email', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'first_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'is_active', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'is_staff', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'is_superuser', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'last_login', '2021-06-03 10:59:51.170000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'last_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'password', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user', 'username', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user_groups', 'group_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user_groups', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'auth_user_groups', 'user_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'authccenter_adgroup', 'ccneter_group_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'authccenter_adgroup', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'authccenter_adgroup', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'arc_folder', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'duration_unit', 'H', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'duration_value', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'enable', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'interval_value', '10', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingscheduler', 'start_boundary_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingschedulerinpath', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingschedulerinpath', 'in_folder', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_batchloadingschedulerinpath', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_partitioning', 'history_depth', '11000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_partitioning', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dataloading_partitioning', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agenthostedappsbehavior', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agenthostedappsbehavior', 'is_app_related_to_ehr', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agenthostedappsbehavior', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'LogoFile', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'agentpp_hosted_app_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'app_key', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'app_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'display_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'get_application_state_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'is_user_alias_required', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'is_window_resizable', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'launch_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'permitted_roles', 'All', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_default_height_size', '768', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_default_width_size', '1024', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_maximal_height_size', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_maximal_width_size', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_minimal_height_size', '480', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentpphostedapp', 'window_minimal_width_size', '640', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'agentpp_hosted_app_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'app_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'client_id', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'launch_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'logo_file', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'redirect_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'resizable_window', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'use_dbmotion_fhir_server', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_default_height_size', '768', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_default_width_size', '1024', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_maximal_height_size', '1050', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_maximal_width_size', '1400', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_minimal_height_size', '480', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_agentsmartonfhirapp', 'window_minimal_width_size', '640', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsadvancedirectivenodes', 'adv_dir', 'ADVDIR', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsadvancedirectivenodes', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsadvancedirectivenodes', 'is_display_adv_dir', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsadvancedirectivenodes', 'nodes', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'collaborate_address_format', '{0} |{1}, |{2}, |{3}, |{4} |{5}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'cv_address_format', '{0}, |{1}, |{2}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'patient_search_name_format', '{0}, |{1}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'phone_format', '{0}-|{1}-|{2}|(#{3})', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplay', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'age_calc_time_span', '1|0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'date_format', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'display_text', 'Patient younger than:', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'priority_order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayagecalculation', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaycommon', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaycommon', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaycommon', 'is_display_patient_mrn', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaycommon', 'is_display_patient_mrn_report', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaycommon', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'mci_interpretation', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'mci_label', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'mci_oid_system', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'mci_priority', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'mci_tooltip', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaymetriccodebasedindicator', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_high_risk_score', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_low_risk_score', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_medium_risk_score', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_oid_system', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_risk_score_code', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvaluebaseprogram', 'vbp_very_high_risk_score', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'vbp_description', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'vbp_display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'vbp_display_name_long', '''+ cast([vbp_display_name] as varchar(1000))+''', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplayvbp', 'vbp_oid_system', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaywithagent', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaywithagent', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaywithagent', 'patient_name_format', '{0}, |{1} |{2}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaywithagent', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appspatientdisplaywithagent', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'MrnText', 'MRN', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'customer_logo', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'date_time_format', 'G', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'dbmotion_logo', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'font_size', '9', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'header_footer_font_type', 'Arial', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'microbiology_report_layout', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'reporting_pl_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'reporting_pv_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'rtf_report_remove_reference_fields', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_appsreporting', 'show_confidentiality_disclamer', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'auditing_type', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'authorized_max_storage_size', '500', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'server_principals', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_cagdataaccessauditing', 'suspected_max_storage_size', '500', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'capsule_page_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'capsule_type', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'capsules_paging_size', '10', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'confidentiality_filter', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'end_scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'inbound_csv_vault_folder', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'local_folder', 'C:\Capsules', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'num_of_days_to_delete_capsules', '30', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'on_demand_local_folder', 'C:\Capsules\OnDemand\CCD_LOCAL', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'on_demand_vault_folder', 'C:\Capsules\OnDemand\CCD_DEST', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'outbound_csv_vault_folder', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_capsuleservice', 'vault_folder', 'C:\Capsules', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'certificate_thumptrint', '(Enter your Certificate Thumbprint)', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'enable_carequality_integration', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'find_documents_endpoint', 'https://brokeringrespondinggateway- /iti38/<CQ Participant OID>/outbound', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'home_community_id', '(Enter your Home Community ID)', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'patient_discovery_endpoint', 'https://brokeringrespondinggateway- /iti55/<CQ Participant OID>/outbound', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_carequalityintegrationsettingsmodel', 'retrieve_document_endpoint', 'https://brokeringrespondinggateway- /iti39/<CQ Participant OID>/outbound', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'Cve_document_conversion', 'https://viewer-prod-us.csg.az.allscriptscloud.com', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'Pdf_document_conversion', 'https://cdatopdf-prod-us.csg.az.allscriptscloud.com/api/convert', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'customer_name', 'dbMotion', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'cve_renew_certificate', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'display_mode', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'environment', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'retrieval_key_cloud_service', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'service_location', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'source_system', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'transformation_cloud_service', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'transformation_service_subscription', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ccdadisplay', 'vaas_document_conversion', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'business_aspect', '', 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'business_table', '', 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'code_name', '', 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'cv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'display_as', 'Preferred|Baseline|Local|Text', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'pv_parent_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalcodedisplay', 'vocabulary_domain', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_BringExtDocsOnShowAll', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DD_PatientPolicy_URL', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DD_ProviderPolicy_URL', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DD_ResetPasskey', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DocPreviewFontFamily', 'Courier New', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_DocsTreePaneWidth', '33', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_ExtDocsTreePaneHeight', '35', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_ShowEmptyFolders', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_ShowExternalDocumentsLabel', 'Show External Documents', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_ShowExternalDocumentsLabelForAgent', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ClinicalDocument_SortTypeByDesignation', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ConditionTypeToDisplay', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'Documents_CompletionStatusAdded', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'ExteranlDocument_Default_Grouping', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'Imaging_DisplayImagingMetaData', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'Imaging_ShowEmptyFolders', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'LabEvents_DefaultGrouping', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'LabResultHistory_DisplaySearch', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'LabResults_FormatText', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'Laboratory_OpenMicroReportForMicroEvent', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'Laboratory_UseWrappedText', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'clinical_domain_id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'code_system_name_display', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'demography_details_type', '7', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'demography_display_insurances_grid', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'disclaimer', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'display_grid', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'display_not_inactive', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'grouped_by_display', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'grouped_by_selected', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'show_cancelled_display', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'show_cancelled_selected', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicaldomainproperties', 'show_record_count', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'CreditTitlePosition', '120', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'CustomerLogoFileName', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'DefaultDomain', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'DefaultLogoFile', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'IsOtherGroupExpanded', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'IsShowLinkSectionDisclaimer', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'IsShowMessageSectionDisclaimer', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'IsTextWrappingUsedInCD', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'LoginScreenLogosOptions', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'UrlOnLinkSectionDisclaimer', '/dbMotionInformationServices/dbMotionInformationPage.aspx', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'UserNameDisplayOptions', '{0}, |{1}, |{2}|{3}, |{4}, |{5}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'WebApplicationName', 'dbMotionClinicalViewer', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_clinicalviewergeneral', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'ContinueSearchAfterSQQCheckFailure', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'DemographicSearch_AutoEnter', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'LeadingPatientRecordPolicy', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MRN_label', 'MRN', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MinSQQ', '50', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MrnSystemSelectorIsEmptyItemEnabled', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MrnSystemSelectorIsSortingEnabled', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MrnSystemSelectorMaxColumnCount', '2', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'MrnSystemSelectorMaxDropItems', '6', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'PatientSearch_IsDirectEnterPatientFile', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'PatientSearch_IsDirectEnterPatientFile_Demographics', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'PatientSearch_IsDirectEnterPatientFile_Demographics_MinScore', '140', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'PatientSearch_LeadingPatientRecordPolicy', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'System_label', 'System', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'parent_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_collaboratepatientsearchproperties', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_currentculture', 'agenthub_general_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_currentculture', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_currentculture', 'name_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'auditing_type', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'authorized_max_storage_size', '7000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'server_principals', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataaccessauditing', 'suspected_max_storage_size', '500', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', '_info', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'concatenate_values', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'enable', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'hide_uom', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'page_width', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_dataelement', 'report_width', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_demographysearchfields', 'dbm_patient_attribute_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_demographysearchfields', 'demo_search_field_label', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_demographysearchfields', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_demographysearchfields', 'max_chars', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_demographysearchfields', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'acdmCommunityName', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'clientCertificateThumbprint', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'clientOid', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'enableSendingViaAcdm', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'gatewayUrl', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_directmessagingacdm', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'clinical_domain_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'culture', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'cv_general_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'message', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_disclaimertext', 'message_link_text', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'end_scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'frequency_mode', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'protected_systems1', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'protected_systems2', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'protected_systems_rate1', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'protected_systems_rate2', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'start_scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchbootstrapproperties', 'unprotected_systems_rate', '8000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'content_free_systems', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'content_free_systems_mode', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'index_free_systems', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'is_ds_of_cdr_enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'is_ds_of_external_enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchgeneralproperties', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'end_scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'frequency_mode', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'protected_systems1', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'protected_systems2', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'protected_systems_rate1', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'protected_systems_rate2', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'start_scheduled_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_documentsearchlivefeedsproperties', 'unprotected_systems_rate', '2000', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentblinks', 'admission_inpatient_domains', 'e757b766e61d08f435d3e9e6280f355c', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentblinks', 'admission_interval', '1|3', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentblinks', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentblinks', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'attention_searching_option', '3', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'attention_searching_time', '7', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'default_attention_time', '7 Days', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'display_name', 'All Clinical Domains', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'name', 'AllDomains', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentclinicaldomainsproperties', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentcvcommonclinicaldomainsproperties', 'default_searching_option', '4', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentcvcommonclinicaldomainsproperties', 'default_searching_time', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentcvcommonclinicaldomainsproperties', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'clean_checkboxes_after_bulk_action', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'default_bulk_action', 'Print', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'enable_cv_from_patient_name', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'enable_patient_mapping', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'footer_logo', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'get_all_data_button_available', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'my_ehr_data_default_view', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'reset_bulk_action', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'show_launch_collaborate', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentgeneral', 'show_send_feedback', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragenthelp', 'agentpp_hosted_app_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragenthelp', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragenthelp', 'link_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragenthelp', 'link_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentmeasurementproperties', 'domain_id', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentmeasurementproperties', 'hide_uom', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentmeasurementproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentmeasurementproperties', 'order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentmeasurementproperties', 'semantic_group_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticdelta', 'display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticdelta', 'enable_semantic_delta', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticdelta', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticdelta', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticdelta', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticgroup', 'display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticgroup', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticgroup', 'order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ehragentsemanticgroup', 'pv_measurement_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationreasons', 'clinical_domain_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationreasons', 'culture', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationreasons', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationreasons', 'message', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationreasons', 'pv_patient_search_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationtext', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationtext', 'patient_search_page_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationtext', 'pv_emg_declaration_patient_search_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_emergencydeclarationtext', 'text', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_encounterdiagnosisrelationship', 'admitted_diagnosis', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_encounterdiagnosisrelationship', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_encounterdiagnosisrelationship', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_encounterdiagnosisrelationship', 'primary_diagnosis', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_encounterdiagnosisrelationship', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'culture', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'cv_general_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'is_active', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'method', 'GET', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplication', 'uri', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'dbm_param', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'external_application_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'is_static', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_externalapplicationparameter', 'static_value', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'clinical_domain_id', '17', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'device_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'facility', 'ALL', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'method', 'GET', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'pv_clinical_domain_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'schema_code', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'uri', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacs', 'use_code', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsdisclaimer', 'Grouping_by_Modality', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsdisclaimer', 'Pacs_Disclaimer_Text', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsdisclaimer', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsdisclaimer', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsparameter', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsparameter', 'imaging_pacs_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsparameter', 'is_static', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsparameter', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_imagingpacsparameter', 'parameter_value', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'abnormal_values', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'chart_format', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'date_format', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'display_abnormal_in_color', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'display_range_values', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'parent_id', '16', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'range_values', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'report_max_chars_in_remark_col', '600', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'report_max_rows_in_long_row_cell', '33', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_labchartdisplayoptions', 'report_max_rows_in_regular_col', '20', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_launchergeneralproperties', 'default_app_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_launchergeneralproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_launchergeneralproperties', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'action', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'action_time', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'ccenter_user_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'login_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_loginshistory', 'user_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'enable_my_hr_flow', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'gain_access_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'get_document_list_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'get_document_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'my_hr_node_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'my_hr_oid', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'pcehr_exist_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrconnectivityentity', 'stylesheet', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrorganizationsentity', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrorganizationsentity', 'iho_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrorganizationsentity', 'iho_thumbprint', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrorganizationsentity', 'org_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_myhrorganizationsentity', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantbaselinelistmodel', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantbaselinelistmodel', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantbaselinelistmodel', 'paticipant_identifier', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantbaselinelistmodel', 'paticipant_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'healthcare_institude_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'home_community_id_three_level', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'identifier', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistbasedpaamodel', 'patient_assigning_authority_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistmodel', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistmodel', 'institude_name_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistmodel', 'paticipant_identifier', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_participantlistmodel', 'paticipant_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'code', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'pl_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'priority_order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientdetailssectionordering', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdefaultsearch', 'default_search', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdefaultsearch', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdefaultsearch', 'patient_search_page_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'attestation_text', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'authority_text', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'cluster_selection_behavior', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'display_user_attestation', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'display_warning', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'enable_death_indicator', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchdisplayoptions', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchtooltip', 'clinical_domain_id', '14', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchtooltip', 'culture', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchtooltip', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchtooltip', 'message', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientsearchtooltip', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patient_view_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patients_list_label', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patients_list_order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patients_list_roles', 'None', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patients_list_type', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientslistviews', 'patients_relation_type', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewdefaultlandingpage', 'default_page', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewdefaultlandingpage', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewdefaultlandingpage', 'patient_view_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'background_image', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'default_domain_id', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'default_logofile', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'patient_view_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_patientviewgeneraldefinitions', 'project_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'CdrDiscovery', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'GeneralResetWorker', '720', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'MaximumAttemptsNumber', '3', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'MedicalStaffSync', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'MedicalStaffSyncTracing', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'ParsedDateTimeFormat', 'yyyy-MM-dd HH:mm', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'PatientDefaultCacheTolerance', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'PatientResetWorker', '20', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'PcpRelationStrategy', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'RelationSourceResetWorker', '20', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'RelationTargetResetWorker', '20', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_ppolgeneral', 'parent_empi_id_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_prefetchsettingsmodel', 'api_subscription_key', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_prefetchsettingsmodel', 'api_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_prefetchsettingsmodel', 'enable_prefetch', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_prefetchsettingsmodel', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_prefetchsettingsmodel', 'page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'category_name', 'External Documents', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'category_order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'expand_by_default', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'hide_fields', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'information_text', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'nodes', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'roles', 'All', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvcategoriesproperties', 'time_frame', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvpatientnamedisplay', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvpatientnamedisplay', 'pv_parent_patient_display_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_pvpatientnamedisplay', 'pv_patient_name_display', '{FNAME}, |{GNAME} |{MNAME}', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'column_order', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'dbMotion_patient_attribute_name_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'default_fields', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'label', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_searchresultgrid', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_specializedviews', 'domain_codes_file_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_specializedviews', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_specializedviews', 'patient_view_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_specializedviews', 'roles', 'None', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_specializedviews', 'view_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'from_address', 'ReportingServices@dbMotion.com', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'message', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'smtp_port', '25', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'smtp_url', 'db-cas', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_usagereports', 'status', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vitalsinpatientmeasurement', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vitalsinpatientmeasurement', 'include_emergency_measurements', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vitalsinpatientmeasurement', 'include_inpatient_measurements', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'clinical_domain_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'cv_general_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'cv_patient_display_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'domains_to_concatenate_values', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'domains_to_hide_uom', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'encounter_types_to_display', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'encounters_emergency_threshold', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'encounters_enable_episode_filter', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'encounters_remove_duplicated', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'facility_filter_enable', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'filter_cancelled_items', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'filter_mood_codes', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'filter_status_code', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'grouping_mode', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'lab_report_fixed_width_font', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'lab_susceptibility_methods_code_type', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'medical_staff_types_priority', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'patient_id_type_display_priority', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'patient_name_type_priority', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'patient_privacy_indicate_minority', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'patient_privacy_minor_max', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'patient_privacy_minor_min', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pl_parent_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pl_patient_display_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pv_grouping_mode_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pv_parent_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pv_parent_patient_display_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'pv_patient_id_type_display_priority', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'reporting_cv_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'reporting_pl_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'reporting_pv_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_med_filter_undefined_status', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_amount_encounter', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_amount_labs', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_amount_meds', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_unit_encounter', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_unit_labs', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_time_filter_unit_meds', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_top_allergy_intolerance', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_top_conditions', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_top_encounters', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_top_laboratory_events', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'summary_top_substance_administration', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'unit_priority_list_body_height', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'unit_priority_list_body_weight', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpo', 'user_facility_root_oid', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'clinical_data_display_options', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'clinical_domain_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'code_system_name_display', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'cv_general_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommon', 'pl_parent_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommunication', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommunication', 'is_encounter_conf_inheritance', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommunication', 'parent_cv_general_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommunication', 'pl_parent_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpocommunication', 'pvp_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoehragentdomains', 'clinical_domain_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoehragentdomains', 'filter_codes', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoehragentdomains', 'filter_type', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoehragentdomains', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoehragentdomains', 'pv_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpofacilitydisplay', 'facility_source', '2', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpofacilitydisplay', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpofacilitydisplay', 'return_act_organization_as_unit', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpofacilitydisplay', 'use_org_type_mode', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoppol', 'id', NULL, 1
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoppol', 'patient_privacy_mask_ssn', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_vpoppol', 'patient_privacy_remove_excluded_clusters', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'culture', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'cv_general_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'date_separator', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'long_time_pattern', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'short_date_pattern', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'short_time_pattern', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'dbmconfigapp_webculture', 'time_separator', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'app_id', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'categories_available_for_send', 'All', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'send_to_my_EHR_ccda_only', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'send_to_my_EHR_failure_message', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_appid', 'send_to_my_EHR_success_message', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'deployment_type', 'Local', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_exe', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_follow_focused_window', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_launch_title', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_title', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_version', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'detection_window_class', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'position_agent_corner', 'RightTop', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'position_app_corner', 'RightTop', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'position_offset_x', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'position_offset_y', '40', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_ehr', 'prevent_detected_window_topmost', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'display_lang', '$_NODE_DEFAULT_LANGUAGE$', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'install_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'install_url_expiration_date', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_activate_ccow_receiver', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_auto_run', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_ccow_isolated_session', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_display_alert_message', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_install_ccow_context_receiver', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_install_dbm_context_receiver', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_launch_api', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_multitenant', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_show_system_tray_icon', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_uninstall_previous_version', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_update_configuration_enabled', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'is_update_new_version_enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'product_server_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'profile_name', '$_NODE_WEB_SERVER_STATEFUL$', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'user_absolute_domain', '$_NODE_ACCESS_ABSOLUTE_DOMAIN$', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_installationprofile', 'web_server_stateful', '$_NODE_WEB_SERVER_STATEFUL$', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'blink_only_first_doa', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'ccow_item_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'context_type', 'CcowParticipant', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'direct_address', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'direct_address_suffix', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'ehr_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'endpoints_page_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'env_variable_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'env_variable_value', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'exclude_dash_from_mrn', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'facility_extension', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'facility_root', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'instance_properties_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'interceptor_type', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'is_enabled', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'is_user_mapping_enabled', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_app_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_community_oid', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_endpoint', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_login', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_password', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_source_system_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'mu_reporting_type', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'nonCcowPluginType', 'Custom', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'ofek_url', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'supported_profiles', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'thumbprint', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'uiAutomation_config_file_path', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'user_mapping_file_path', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'user_mapping_is_default_to_loggedInUser', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instance', 'user_mapping_is_use_as_role', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instanceproperties', 'app_id_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instanceproperties', 'ehr_user_assign_auth', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instanceproperties', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instanceproperties', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_instanceproperties', 'patient_assigning_Authority_for_Display', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'act_type', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'app_id_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'facility_extension', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'facility_root', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_orderingfacilities', 'instance_properties_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'ccow_passcode', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'instance_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'is_shared', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_participant', 'type', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'instance_properties_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'patient_assign_auth_display', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'patient_assign_auth_resolve', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'suffix_type', 'MRN', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_patientcontext', 'suffixes', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_sourcesystem', 'act_types', 'All', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_sourcesystem', 'app_id_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_sourcesystem', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_sourcesystem', 'instance_properties_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_sourcesystem', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_usercontext', 'ad_domain', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_usercontext', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_usercontext', 'instance_properties_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_usercontext', 'suffixes', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'externalapps_usercontext', 'user_context_type', 'Managed', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_group', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_group', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_group_node', 'group_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_group_node', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_group_node', 'node_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'application_server', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'is_available_during_document_search', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'node_confidentiality_level', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'pas_option_remote', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'pl_active', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'ppol_provider_node_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'request_from_id', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'response_to_id', '-1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'federation_node', 'uid', '''+ cast([id] as varchar(1000))+''', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_Description', 'Description', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_Facility', 'physicalDeliveryOfficeName', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_FirstName', 'givenName', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_LastName', 'sn', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_NationalIdNumber', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'ad_mapping_Title', 'title', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'allow_alternative_authentication', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'container', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'domain_id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'domain_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'domain_port', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'helios', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'netbios_domain_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'untrusted_ad', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'untrusted_ad_user_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'untrusted_ad_user_password', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_adproviders', 'use_dnl_format', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_applicationdomains', 'application_domain_qualifier', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_applicationdomains', 'default_role_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_applicationdomains', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_applications', 'application_id', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_applications', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_internalroles', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_internalroles', 'role_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientauthorization', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientauthorization', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientauthorization', 'pas_option_local', '0', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientproviderrelationship', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientproviderrelationship', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_patientproviderrelationship', 'patient_provider_relationship', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_rolemapping', 'application_id_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_rolemapping', 'external_role_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_rolemapping', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_rolemapping', 'internal_role_name_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuers', 'domain_name_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuers', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuers', 'saml_certificate_thumbprint', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuers', 'saml_issuer_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuersunmanaged', 'application_domain_qualifier_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuersunmanaged', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuersunmanaged', 'saml_certificate_thumbprint', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_samlissuersunmanaged', 'saml_issuer_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_securitygeneral', 'activate_facility_identification', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_securitygeneral', 'active_encounter_validation_rule', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_securitygeneral', 'facility_identification_excluded_codes', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_securitygeneral', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'security_securitygeneral', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'application_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'attribute_code', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'cluster_filter_indication', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'dbmotion_node_id_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'display_for_search', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'facility_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'is_default', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'is_system_mandatory', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'node_uid', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'organization_code', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'segment_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'source_system_dbMotion_oid', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'source_system_display_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'source_system_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_authoritysystems', 'system_type', 'Real', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_ccdawithoutadtsystems', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_ccdawithoutadtsystems', 'load_ccda_without_adt_sources', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_ccdawithoutadtsystems', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_dbmotionsystem', 'dbmotion_system', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_dbmotionsystem', 'dbmotion_system_node_id_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_dbmotionsystem', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_dbmotionsystem', 'node_uid', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_dbmotionsystem', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'empi_url_address_for_patient_identity_feed_v3', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_MinimumScoreThreshold', '5', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_active', 'INOUT', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_deleted', 'NONE', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_merged', 'IN', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_mode', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'filter_overlay', 'NONE', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'patient_entity_type', 'PATIENT', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'patient_member_type', 'PERSON', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'patient_results_sort_order', '-getRecMtime', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiate', 'set_isrealleading', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'initiate_url', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'initiate_version', 'PatientAdapter100', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'patient_credential_password', 'system', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiateconnection', 'patient_credential_username', 'system', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'dbmotion_attribute_description', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'dbmotion_attribute_input', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'dbmotion_attribute_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'dbmotion_attribute_output', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'dbmotion_attribute_weight', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'initiate_hub_attribute_code', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'initiate_hub_field_name', '', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'initiate_hub_id_issuer', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'initiate_hub_segment_name', 'memIdent', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'mapping_values', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatemappings', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatevpo', 'enable_federated_match', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatevpo', 'enable_federated_search', 'False', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatevpo', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_initiatevpo', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'empi_type', 'Initiate', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'hmo_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'hmo_name', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_via', 'systems_parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_viavpo', 'id', NULL, NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_viavpo', 'parent_id', '1', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_viavpo', 'vpo_patient_entrance_apply_cluster_filter', 'True', NULL
INSERT INTO #TableFieldsMetadata
SELECT 'via_viavpo', 'vpo_personindex_dynamic_field_list_for_response', 'GNAME,FNAME,STATE,CITY,ADDR,GEN,BTHDAY,HOSP,PHONE,SSN,INSRNC,SRCINSRNC,ZIP,SENDFAC,SENDAPP,JHINMD,PAR_MDATE,PAR_CDATE,NONMASKSSN,LAST_MODIFIED_DATE', NULL

DECLARE @version decimal(10,3)

select @version=max(cast([version]as decimal(10,3))) from [dbo].[dbmconfigapp_migrationmanager]

  create table #Tables (ID INT IDENTITY (1,1) ,
				SchemaName varchar(1000),--COLLATE Latin1_General_CI_AS ,
				TableName varchar(1000) --COLLATE Latin1_General_CI_AS  
				)

-- Prepare metadata table for INSERT
  insert into #Tables (SchemaName , TableName)
  SELECT DISTINCT  schema_name(A.schema_id) , A.name  
FROM [sys].[tables]  A
inner join #TableFieldsMetadata D
on A.name = D.TableName
INNER JOIN sys.partitions B ON A.object_id = B.object_id  

WHERE A.type = 'U'
AND index_id < 2 -- 0:Heap, 1:Clustered		
AND B.rows > 0
and NOT EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata T
			   WHERE D.TableName = T.TableName
			   AND T.IsKey IS NOT NULL)

DECLARE   @schema NVARCHAR(max)   , 
          @table NVARCHAR(max)   ,
		  @a int = 1 ,
		  @Path as varchar(8000) = '$_NODE_SHARED_FOLDER$\Services\CCenter\Data'
		  -- @Path as varchar(1000) = 'c:\temp\CCenterData'

DECLARE @DirTree TABLE (subdirectory nvarchar(255), depth INT)
INSERT INTO @DirTree(subdirectory, depth)
EXEC master.sys.xp_dirtree @Path


-- Create the @DataPath directory
IF NOT EXISTS (SELECT 1 FROM @DirTree )
EXEC master.dbo.xp_create_subdir @Path

-- DELETE\INSERT
   declare @insert_fields varchar(max),
          @select        varchar(max)  ,
          @error         varchar(500),
          @query         varchar(max) ,
		  @BeforeInsert         nvarchar(max)  , 
		  @AfterInsert         nvarchar(max)  , 
		  @insert         nvarchar(max) , 
		  @update_fields   nvarchar(max) , 
		  @where_fields nvarchar(max)
		  
	declare @values table(description varchar(max));

    declare  @AddingFieds table( FieldName varchar(1000) , DefaultValue varchar(1000))
    DECLARE @FieldName varchar(1000), 
	        @DefaultValue varchar(1000) 

 WHILE exists(SELECT TOP(1) 1 FROM #Tables)
  BEGIN

      SELECT @schema  = SchemaName, 
			 @table = TableName ,
			 @select = NULL,
			 @insert_fields  = NULL, 
			 @query = '' , 
			 @BeforeInsert = '' , 
			 @AfterInsert = '' , 
			 @insert = ''
	 FROM #Tables
	 WHERE ID =  @a 

	 delete from   @values

						  -- Get columns
						  select @insert_fields = isnull(@insert_fields + ', ', '') +'['+ c.name + ']',
								 @select = case type_name(c.system_type_id)
											  when 'varchar' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'nvarchar' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'datetime' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + convert(varchar(1000), [' + c.name + '], 121) + '''''''', ''null'')'
											  else isnull(@select + ' + '', '' + ', '') + 'isnull('''''''' + cast([' + c.name + '] as varchar(max)) + '''''''', ''null'')'
											end
									
							from sys.columns c with(nolock)							
								 inner join sys.tables t with(nolock) on t.object_id = c.object_id
								 inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
						   where s.name =@schema
							 and t.name =@table
							 AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
							             where c.name = D.FieldName
										 AND D.TableName =  @table);


										  insert into @AddingFieds (FieldName , DefaultValue)
										  SELECT FieldName , DefaultValue
										  FROM #TableFieldsMetadata
										   WHERE TableName =  @table
										   AND DefaultValue IS NOT NULL
				                         
										
										   WHILE EXISTS(SELECT TOP(1) 1 FROM @AddingFieds)
											   BEGIN
												  SELECT TOP(1) @FieldName  = FieldName, 
														        @DefaultValue = DefaultValue
												  FROM @AddingFieds
												
												  ---- new field
												  IF  CHARINDEX('['+@FieldName+']'  , @insert_fields)  = 0
												       BEGIN
															 SET @insert_fields = @insert_fields + ',' + @FieldName
															 SET @select = @select + '+'',''+''''''' + @DefaultValue +''''''''
                                                       END
												 
												  DELETE FROM @AddingFieds
												  WHERE FieldName  = @FieldName
												
											   END

						  set @insert_fields = '
	INSERT ' + @schema + '.' + @table + '(' + @insert_fields + ')';
						 
						  set @query = 'SELECT ' +  @select + ' FROM ' + @schema + '.' + @table + '  ' ;
						  
						  insert into @values(description)
						  exec(@query);


						  set @insert = isnull(@insert + char(10), '') + '--' + upper(@schema + '.' + @table);

						IF @table = 'via_authoritysystems'
						      BEGIN
								  select @insert = @insert + char(10) + 'IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.via_authoritysystems 
		WHERE CHARINDEX(''|''+[source_system_dbMotion_oid] +''|'' ,'''+ REPLACE(v.description ,CHAR(39),'|')+''') > 0) ' + @insert_fields  + char(10) + 'values(' + v.description + ');' + char(10)  + char(10)
								  from @values v
								  where isnull(v.description, '') <> '';
															 
							  END
						ELSE IF @table = 'dbmconfigapp_agentpphostedapp'
						      BEGIN 
								  DECLARE @insert1 varchar(max)
								  set  @insert1 = ''
								  select @insert1 = @insert1 + 
'
IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.dbmconfigapp_agentpphostedapp 
		WHERE CHARINDEX(''|''+[app_name] +''|'' ,'''+ REPLACE(v.description ,CHAR(39),'|')+''') > 0) ' + @insert_fields  + char(10) + 'values(' + v.description + ');' + char(10)  + char(10)
								  from @values v
								  where isnull(v.description, '') <> ''
								  and CHARINDEX('Care Coordination' , v.description) = 0
								  and CHARINDEX('Clinical View Agent' , v.description) = 0;

								  IF isnull(@insert1, '') = ''
									BEGIN
									 DELETE FROM #Tables
									 WHERE ID =  @a 
									 SET @a = @a + 1

									 CONTINUE
									END
									
								 select @insert = @insert + @insert1
							  END
						ELSE
						  BEGIN
							  select @insert = @insert + char(10) + @insert_fields + char(10) + 'VALUES(' + v.description + ');' + char(10)  + char(10)
							  from @values v
							  where isnull(v.description, '') <> '';
						  END 

						IF @table = 'dbmconfigapp_ehragentmeasurementproperties' AND @version < 19.6
							SET @AfterInsert = @AfterInsert + '
UPDATE dbmconfigapp_ehragentmeasurementproperties SET [hide_uom] = 1 WHERE [domain_id] IN (''HeartRate'',''BloodPressure'')
							'
						SET @BeforeInsert = ' USE dbmCCenter
GO
IF OBJECT_ID('''+upper(@schema + '.' + @table) + ''') IS NOT NULL
			BEGIN 
			BEGIN TRAN 
			'
						IF @table != 'dbmconfigapp_agentpphostedapp'
						BEGIN
							SET @BeforeInsert = @BeforeInsert + '
			DELETE ' +upper(@schema + '.' + @table)

							IF OBJECTPROPERTY(OBJECT_ID(@schema + '.' + @table), 'TableHasIdentity') = 1			
								  BEGIN
							 
									  SET @BeforeInsert = @BeforeInsert + ' SET IDENTITY_INSERT '+upper(@schema + '.' + @table) +' ON ' 
									  SET @AfterInsert = @AfterInsert + ' SET IDENTITY_INSERT '+upper(@schema + '.' + @table) +' OFF '
								
								  END
						END
					
						set @insert = @BeforeInsert + @insert  + @AfterInsert + ' COMMIT END'
						set @table = @table + '_ins.sql'
						exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
						@Path  = @Path,
						@Filename  = @table

			 DELETE FROM #Tables
			 WHERE ID =  @a 
			 SET @a = @a + 1
	END


---- UPDATE
 TRUNCATE TABLE #Tables
 SET @a = 1 
 insert into #Tables (SchemaName , TableName)
  SELECT DISTINCT schema_name(A.schema_id) , A.name  
FROM [sys].[tables]  A
inner join #TableFieldsMetadata D
on A.name = D.TableName
INNER JOIN sys.partitions B ON A.object_id = B.object_id  

WHERE A.type = 'U'
AND index_id < 2 -- 0:Heap, 1:Clustered		
AND B.rows > 0
and  EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata T
			   WHERE D.TableName = T.TableName
			   AND T.IsKey IS NOT NULL)

WHILE exists(SELECT TOP(1) 1 FROM #Tables)
  BEGIN
    
      SELECT @schema  = SchemaName, 
			 @table = TableName ,
			 @select = NULL,
			 @insert_fields  = NULL, 
			 @query = '' , 
			 @BeforeInsert = '' , 
			 @AfterInsert = '' , 
			 @insert = '' , 
			 @update_fields = NULL ,
			 @where_fields = NULL 
	 FROM #Tables
	 WHERE ID =  @a 

	 IF (@table='dbmconfigapp_clinicalcodedisplay' AND NOT EXISTS 
		(select [display_as] from [dbo].[dbmconfigapp_clinicalcodedisplay] 
			where display_as like '%Preferred%' and display_as like '%Baseline%' and display_as like '%Local%' and display_as like '%Text%'))
	 BEGIN
		DELETE FROM #Tables
		WHERE ID =  @a 
		SET @a = @a + 1
		CONTINUE
	 END

	 delete from   @values
	 ---
	   select @update_fields = isnull(@update_fields + ' +'','' +'' ', '') +' ['+ c.name + '] = ''' +
								case type_name(c.system_type_id)
											  when 'varchar' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39)'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'nvarchar' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'datetime' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + convert(varchar(1000), [' + c.name + '], 121) + '''''''', ''null'')'
											  else isnull(@select + ' + '', '' + ', '') + ' + isnull('''''''' + cast([' + c.name + '] as varchar(max)) + '''''''', ''null'')'
											end + ''
		
		from sys.columns c with(nolock)							
				inner join sys.tables t with(nolock) on t.object_id = c.object_id
				inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
		where s.name =@schema
			and t.name =@table 
			AND c.is_identity = 0 ---???
			AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
						where c.name = D.FieldName
						AND D.TableName =  @table
						AND D.IsKey IS NULL);
--select '00',@a as a , @update_fields
	    select @where_fields = isnull(@where_fields + '+'' AND ', '') +' ['+ c.name + '] =''' + ---cast([' + c.name + ']  as varchar(1000))'
											
							  case type_name(c.system_type_id)
							                  when 'varchar' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(max)) + '''''''
											  when 'nvarchar' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(max)) + '''''''
											  when 'datetime' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(1000)) + '''''''
											  else isnull(@select + ' + '', '' + ', '') + ' +  cast([' + c.name + '] as varchar(max)) ''' 
											end + ' '''
									
		from sys.columns c with(nolock)							
				inner join sys.tables t with(nolock) on t.object_id = c.object_id
				inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
		where s.name =@schema
			and t.name =@table
			AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
						where c.name = D.FieldName
						AND D.TableName =  @table
						AND D.IsKey IS NOT NULL);
	--select '11',@a as a ,@where_fields  as '@where_fields' 

        SET @query =  'SELECT ' + ''' UPDATE ' + @schema + '.' + @table + '
		SET   '  + @update_fields + '
		'+ ' + '' 
		WHERE ' + @where_fields		
		+ ' from ' + @schema + '.' + @table + '  ' ;
		
--select '22',@a as a , @update_fields,@where_fields  as '@where_fields' ,@query


						  insert into @values(description)
						  exec(@query);


--select '33' , * from @values
						  set @insert = isnull(@insert + char(10), '') + '--' + upper(@schema + '.' + @table);
							--select @insert as '00'
						  select @insert = @insert + char(10) +   v.description + ';' + char(10)  + char(10)
						  from @values v
						  where isnull(v.description, '') <> '';

		SET @BeforeInsert = ' USE dbmCCenter
						
						IF OBJECT_ID('''+upper(@schema + '.' + @table) + ''') IS NOT NULL
									BEGIN '
						set @insert = @BeforeInsert + @insert  +  ' END'
	 ------
				set @table = @table + '_upd.sql'
---select '55' , @table , @BeforeInsert as '@BeforeInsert', @insert as '@insert'
				exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
				@Path  = @Path,
				@Filename  = @table

		DELETE FROM #Tables
		WHERE ID =  @a 
		SET @a = @a + 1
	END

---table dbmCCenter.dbo.dbmconfigapp_dbfiles 

   SELECT  @insert ='' ,  @query = '' 
   delete from   @values

set @table = 'dbmconfigapp_dbfiles_ins.sql'


 select @query = 
 'select ' + 
 ''' 
	IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.dbmconfigapp_dbfiles T WHERE T.[filename] ='''''' + [filename] + '''''')
		INSERT INTO dbo.dbmconfigapp_dbfiles ( [filename], [data], [size]) ''' +
  '+'' 
		SELECT '' +''''' + ''''' + [filename] +''''''''+ '''+ ', '+''' +''''''''+ 
  cast([data] as nvarchar(max)) +''''''''+ '''+ ', '+''' +''''''''+ cast([size] as varchar(1000))+ ''''''
  '''
  + ' FROM dbo.dbmconfigapp_dbfiles '

--	select @query
						  insert into @values(description)
						  exec(@query);
	
						  select @insert = @insert + char(10)  + v.description  + char(10)  + char(10)
						  from @values v
    select @insert = 'USE dbmCCenter ' + @insert
	exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
				@Path  = @Path,
				@Filename  = @table

drop table #TableFieldsMetadata
drop table #Tables

GO
EXEC sp_configure 'Ole Automation Procedures', 0;  
GO  
RECONFIGURE;
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[spWriteStringToFile]') AND type in (N'P', N'PC'))
DROP PROCEDURE dbo.spWriteStringToFile
GO
go
	


