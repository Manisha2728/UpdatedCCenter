/// This file is referenced by dbmModelAdmin, which is the base of all configuration pages in dbmconfigapp
/// file: admin\dbm_ModelAdmin.py

$(document).ready(function () {

    var i = $('#id_documentsearchgeneralproperties_set-0-content_free_systems_mode').val();
    if (i == 2) // equal to a selection option
    {
        $('.form-row.field-content_free_systems').show();       
    }
    else  {
        $('.form-row.field-content_free_systems').hide();
    }
    $('#id_documentsearchgeneralproperties_set-0-content_free_systems_mode').bind('change', function (event) {

        var i = $('#id_documentsearchgeneralproperties_set-0-content_free_systems_mode').val();        
        if (i == 2) // equal to a selection option
        {
            $('.form-row.field-content_free_systems').show();
        }
        else  {
            $('.form-row.field-content_free_systems').hide();
        }
    });


});
