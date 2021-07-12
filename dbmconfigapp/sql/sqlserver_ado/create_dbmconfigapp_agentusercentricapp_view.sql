

CREATE OR ALTER VIEW [dbo].[dbmconfigapp_agentusercentricapp_view]
	AS
	SELECT        dbo.dbmconfigapp_agentusercentricapp.id, dbo.dbmconfigapp_agentusercentricapp.agentpp_hosted_app_page_id, dbo.dbmconfigapp_agentusercentricapp.app_name, 
				 dbo.dbmconfigapp_agentusercentricapp.enabled, 
							dbo.dbmconfigapp_agentusercentricapp.LogoFile, dbo.dbmconfigapp_dbfiles.data AS LogoFileData
	FROM            dbo.dbmconfigapp_agentusercentricapp LEFT OUTER JOIN
							dbo.dbmconfigapp_dbfiles ON dbo.dbmconfigapp_agentusercentricapp.LogoFile = dbo.dbmconfigapp_dbfiles.filename


							
						
							
					

