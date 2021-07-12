CREATE OR ALTER VIEW [dbo].[dbmconfigapp_reporting_view]
	AS
	SELECT p.id, p.font_size, p.header_footer_font_type, p.date_time_format, p.microbiology_report_layout, p.show_confidentiality_disclamer, p.rtf_report_remove_reference_fields,
	p.MrnText,
	p.customer_logo, f_cust.data as customer_logo_data, p.dbmotion_logo, f_dbm.data as dbmotion_logo_data
	from 
	      dbo.dbmconfigapp_appsreporting p
		left join     dbmconfigapp_dbfiles f_dbm
			on p.dbmotion_logo = f_dbm.filename        
		left join     dbmconfigapp_dbfiles f_cust
			on p.customer_logo = f_cust.filename    