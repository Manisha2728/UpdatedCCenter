CREATE OR ALTER VIEW [dbo].[dbmconfigapp_get_images_view]
	AS

	SELECT  
		dbo.dbmconfigapp_patientviewgeneraldefinitions.*, 
		dbo.dbmconfigapp_dbfiles.data as BackgroundImageData
	FROM        
		dbo.dbmconfigapp_patientviewgeneraldefinitions 
		LEFT OUTER JOIN dbo.dbmconfigapp_dbfiles ON 
		dbo.dbmconfigapp_patientviewgeneraldefinitions.[background_image] = dbo.dbmconfigapp_dbfiles.[filename]
 

 