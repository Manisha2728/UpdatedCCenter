/// This file is referenced by dbmModelAdmin, which is the base of all configuration pages in dbmconfigapp
/// file: admin\dbm_ModelAdmin.py

$(document).ready(function () {

    var i = $('#id_documentsearchbootstrapproperties_set-0-frequency_mode').val();
    if (i == 2) // equal to a selection option
    {
        $('.form-row.field-start_scheduled_time').show();       
		$('.form-row.field-end_scheduled_time').show();
	}
    else  {
        $('.form-row.field-start_scheduled_time').hide();       
		$('.form-row.field-end_scheduled_time').hide();
    }
    $('#id_documentsearchbootstrapproperties_set-0-frequency_mode').bind('change', function (event) {

        var i = $('#id_documentsearchbootstrapproperties_set-0-frequency_mode').val();        
        if (i == 2) // equal to a selection option
        {
            $('.form-row.field-start_scheduled_time').show();       
			$('.form-row.field-end_scheduled_time').show();
        }
        else  {
            $('.form-row.field-start_scheduled_time').hide();       
			$('.form-row.field-end_scheduled_time').hide();
        }
    });


});
