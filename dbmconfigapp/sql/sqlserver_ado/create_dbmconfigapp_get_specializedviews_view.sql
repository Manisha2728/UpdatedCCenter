CREATE OR ALTER VIEW [dbo].[dbmconfigapp_get_specializedviews_view]
	AS

	SELECT  
		dbo.dbmconfigapp_specializedviews.*, 
		dbo.dbmconfigapp_dbfiles.data as DomainCodesData
	FROM        
		dbo.dbmconfigapp_specializedviews 
		LEFT OUTER JOIN dbo.dbmconfigapp_dbfiles ON 
		dbo.dbmconfigapp_specializedviews.[domain_codes_file_name] = dbo.dbmconfigapp_dbfiles.[filename]
 

 