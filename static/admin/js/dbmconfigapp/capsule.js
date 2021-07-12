/// This file is referenced by dbmModelAdmin, which is the base of all configuration pages in dbmconfigapp
/// file: admin\dbm_ModelAdmin.py

$(document).ready(function () {

    var i = $('#id_capsuleservice_set-0-capsule_type').val();

    if (i == 1) // equal to a selection option
    {
        $('.form-row.field-confidentiality_filter').show();
        $('.form-row.field-outbound_csv_vault_folder').hide(); // show the other one
        $('.form-row.field-inbound_csv_vault_folder').hide(); // show the other one
        $('.form-row.field-end_scheduled_time').hide();
    }
    else if (i == 2) {
        $('.form-row.field-confidentiality_filter').hide(); // hide the first one
        $('.form-row.field-outbound_csv_vault_folder').show(); // show the other one
        $('.form-row.field-inbound_csv_vault_folder').show(); // show the other one
        $('.form-row.field-end_scheduled_time').show();

    }
    $('#id_capsuleservice_set-0-capsule_type').bind('change', function (event) {

        var i = $('#id_capsuleservice_set-0-capsule_type').val();

        if (i == 1) // equal to a selection option
        {
            $('.form-row.field-confidentiality_filter').show();
            $('.form-row.field-outbound_csv_vault_folder').hide(); // show the other one
            $('.form-row.field-inbound_csv_vault_folder').hide();
            $('.form-row.field-end_scheduled_time').hide();// show the other one
        }
        else if (i == 2) {
            $('.form-row.field-confidentiality_filter').hide(); // hide the first one
            $('.form-row.field-outbound_csv_vault_folder').show(); // show the other one
            $('.form-row.field-inbound_csv_vault_folder').show(); // show the other one
            $('.form-row.field-end_scheduled_time').show();

        }
    });


});
