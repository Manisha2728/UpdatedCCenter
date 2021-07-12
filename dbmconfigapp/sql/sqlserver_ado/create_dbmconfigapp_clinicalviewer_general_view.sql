CREATE OR ALTER VIEW [dbo].[dbmconfigapp_clinicalviewer_general_view]
	AS
	SELECT      dbo.dbmconfigapp_clinicalviewergeneral.*, dbo.dbmconfigapp_dbfiles.data as DefaultLogoFileData, 
				dbmconfigapp_vpocommon.clinical_data_display_options as ClinicalDataDisplayOptions
	
FROM            dbo.dbmconfigapp_clinicalviewergeneral 
	LEFT OUTER JOIN
    	dbo.dbmconfigapp_dbfiles ON dbo.dbmconfigapp_clinicalviewergeneral.DefaultLogoFile = dbo.dbmconfigapp_dbfiles.filename
    	INNER JOIN dbo.dbmconfigapp_clinicalviewergeneralpage
    	ON dbo.dbmconfigapp_clinicalviewergeneral.id = dbo.dbmconfigapp_clinicalviewergeneralpage.id
    	INNER JOIN dbmconfigapp_vpocommon 
		ON dbmconfigapp_clinicalviewergeneralpage.id = dbmconfigapp_vpocommon.cv_general_id