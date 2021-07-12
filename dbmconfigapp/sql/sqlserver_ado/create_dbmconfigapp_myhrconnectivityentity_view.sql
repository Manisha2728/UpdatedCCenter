CREATE OR ALTER VIEW [dbo].[dbmconfigapp_myhrconnectivityentity_view]
	AS
	SELECT p.id, f_stylesheet.data as stylesheet_data
	from 
	      dbo.dbmconfigapp_myhrconnectivityentity p
		left join     dbmconfigapp_dbfiles f_stylesheet
			on p.stylesheet = f_stylesheet.filename        
