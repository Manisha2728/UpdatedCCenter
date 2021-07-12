CREATE OR ALTER VIEW [dbo].[dbmconfigapp_agentpphostedapp_view]
	AS
	SELECT          dbo.dbmconfigapp_agentpphostedapp.id, 
					dbo.dbmconfigapp_agentpphostedapp.app_key,
					dbo.dbmconfigapp_agentpphostedapp.agentpp_hosted_app_page_id, 
					dbo.dbmconfigapp_agentpphostedapp.app_name, 
					ISNULL(dbo.dbmconfigapp_agentpphostedapp.display_name, dbo.dbmconfigapp_agentpphostedapp.app_name) as display_name,
					CAST (case  when dbo.dbmconfigapp_launchergeneralproperties.default_app_id is null then 0 else  1 end AS BIT) as is_default,
					dbo.dbmconfigapp_agentpphostedapp.enabled,
					dbo.dbmconfigapp_agentpphostedapp.get_application_state_url,
					dbo.dbmconfigapp_agentpphostedapp.is_user_alias_required,
					dbo.dbmconfigapp_agentpphostedapp.is_window_resizable,
					dbo.dbmconfigapp_agentpphostedapp.launch_url,
					dbo.dbmconfigapp_agentpphostedapp.permitted_roles,
					dbo.dbmconfigapp_agentpphostedapp.window_default_height_size,
					dbo.dbmconfigapp_agentpphostedapp.window_default_width_size,
					dbo.dbmconfigapp_agentpphostedapp.window_maximal_height_size,
					dbo.dbmconfigapp_agentpphostedapp.window_maximal_width_size,
					dbo.dbmconfigapp_agentpphostedapp.window_minimal_height_size,
					dbo.dbmconfigapp_agentpphostedapp.window_minimal_width_size,	
					dbo.dbmconfigapp_agentpphostedapp.LogoFile, dbo.dbmconfigapp_dbfiles.data AS LogoFileData
	FROM            dbo.dbmconfigapp_agentpphostedapp LEFT OUTER JOIN
							dbo.dbmconfigapp_dbfiles ON dbo.dbmconfigapp_agentpphostedapp.LogoFile = dbo.dbmconfigapp_dbfiles.filename
					LEFT OUTER JOIN  dbo.dbmconfigapp_launchergeneralproperties  
					on dbo.dbmconfigapp_launchergeneralproperties.default_app_id =  dbo.dbmconfigapp_agentpphostedapp.id