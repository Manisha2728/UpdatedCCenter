CREATE OR ALTER VIEW [dbo].[dbmconfigapp_ehragentgeneral_view] AS

	SELECT      
		dbo.dbmconfigapp_ehragentgeneral.my_ehr_data_default_view, 
        dbo.dbmconfigapp_ehragentgeneral.id, dbo.dbmconfigapp_ehragentgeneral.default_bulk_action, dbo.dbmconfigapp_ehragentgeneral.reset_bulk_action, 
        dbo.dbmconfigapp_ehragentgeneral.clean_checkboxes_after_bulk_action, dbo.dbmconfigapp_ehragentgeneral.get_all_data_button_available, 
        dbo.dbmconfigapp_ehragentgeneral.show_launch_collaborate, dbo.dbmconfigapp_ehragentgeneral.show_send_feedback, 
        dbo.dbmconfigapp_ehragentgeneral.enable_patient_mapping, dbo.dbmconfigapp_ehragentgeneral.footer_logo, 
        dbfiles_footer.data AS FooterLogoData,dbo.dbmconfigapp_ehragentgeneral.enable_cv_from_patient_name
	FROM            
		dbo.dbmconfigapp_dbfiles AS dbfiles_footer RIGHT OUTER JOIN
			dbo.dbmconfigapp_ehragentgeneral ON dbfiles_footer.filename = dbo.dbmconfigapp_ehragentgeneral.footer_logo