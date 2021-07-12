CREATE OR ALTER VIEW [dbo].[dbmconfigapp_patientview_generaldefinitions_view]
	AS

	SELECT  dbo.dbmconfigapp_patientviewgeneraldefinitions.*, 
			dbo.dbmconfigapp_dbfiles.data as DefaultLogoFileData
	
	FROM        
		dbo.dbmconfigapp_patientviewgeneraldefinitions 
		LEFT OUTER JOIN
    	dbo.dbmconfigapp_dbfiles ON dbo.dbmconfigapp_patientviewgeneraldefinitions.[default_logofile] = dbo.dbmconfigapp_dbfiles.filename
   