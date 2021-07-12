

CREATE OR ALTER VIEW [dbo].[dbmconfigapp_agentsmartonfhirapp_view]
	AS
	SELECT        dbo.dbmconfigapp_agentsmartonfhirapp.id, dbo.dbmconfigapp_agentsmartonfhirapp.agentpp_hosted_app_page_id, dbo.dbmconfigapp_agentsmartonfhirapp.app_name, 
				 dbo.dbmconfigapp_agentsmartonfhirapp.enabled, dbo.dbmconfigapp_agentsmartonfhirapp.client_id, dbo.dbmconfigapp_agentsmartonfhirapp.launch_url, 
					dbo.dbmconfigapp_agentsmartonfhirapp.redirect_url,
					dbo.dbmconfigapp_agentsmartonfhirapp.resizable_window, dbo.dbmconfigapp_agentsmartonfhirapp.window_default_width_size,
					dbo.dbmconfigapp_agentsmartonfhirapp.window_minimal_width_size, dbo.dbmconfigapp_agentsmartonfhirapp.window_maximal_width_size,
					dbo.dbmconfigapp_agentsmartonfhirapp.window_default_height_size, dbo.dbmconfigapp_agentsmartonfhirapp.window_minimal_height_size,
					dbo.dbmconfigapp_agentsmartonfhirapp.window_maximal_height_size, dbo.dbmconfigapp_agentsmartonfhirapp.use_dbmotion_fhir_server,
							dbo.dbmconfigapp_agentsmartonfhirapp.logo_file, dbo.dbmconfigapp_dbfiles.data AS LogoFileData
	FROM            dbo.dbmconfigapp_agentsmartonfhirapp LEFT OUTER JOIN
							dbo.dbmconfigapp_dbfiles ON dbo.dbmconfigapp_agentsmartonfhirapp.logo_file = dbo.dbmconfigapp_dbfiles.filename


							
						
							
					

