function first_n_fields_readonly(table, field, count) {
    for (var i = 0; i < count; i++)
    {
        var input = $('#id_' + table + '_set-' + i + '-' + field);
        $(input).attr("readonly", true);
    }
}

function first_n_fields_disabled(table, field, count) {
    for (var i = 0; i < count; i++)
    {
        var input = $('#id_' + table + '_set-' + i + '-' + field);
        $(input).attr("disabled", true);
    }
}

// Only measured fields can have "Hide the UOM" check box enabled. These are the non-readonly fields.
// and only the fields 'BloodPressure', 'BodyHeight' and 'BodyWeight' can have the "Concatenate Values" check box enabled.
function set_vitals_grid_layout(){
	var table = 'dataelement';
	var field = 'name';
	var readonly_values = ['Date', 'Time', 'Documented By', 'Facility', 'Source'];
	var concatenate_values = ['BodyHeight', 'BodyWeight'];
	var sumRow = $('#'+table+'_set-SUM');
    var count = $(sumRow).parent().children('.has_original').length;
    var foundValues = [];
    
    for (var i = 0; i < count; i++)
    {
        var input = $('#id_' + table + '_set-' + i + '-' + field);
        
        var value = $(input).val();

        if (readonly_values.indexOf(value) >= 0 && foundValues.indexOf(value) < 0) {
            $(input).attr("readonly", true);
            foundValues.push(value);
            $(input).closest('tr').find('input:checkbox[id*="hide_uom"]').attr("disabled", true);
            $(input).closest('tr').find('input:checkbox[id*="concatenate_values"]').attr("disabled", true);
        }
        else
        {
        	if (concatenate_values.indexOf(value) < 0){
        		disable_input($(input).closest('tr').find('input:checkbox[id*="concatenate_values"]')); 	//.attr("disabled", true);
        	}
        }
    }
}

function fields_readonly_by_name(table, field, values) {
    var sumRow = $('#'+table+'_set-SUM');

    var count = $(sumRow).parent().children('.has_original').length;

    var foundValues = [];
    
    for (var i = 0; i < count; i++)
    {
        var value = $("#" + table + '_set-' + i + '>td.field-name>p').text();

        if (values.indexOf(value) >= 0 && foundValues.indexOf(value) < 0) {
        	var input = $('#id_' + table + '_set-' + i + '-' + field);
        	var info = $('#id_' + table + '_set-' + i + '-_info');
            $(input).attr("readonly", true);
            // $(input).hide();
            // $(input).parent().append("<p>N/A</p>");
            $(info).val("ignore-report-width-0");
            foundValues.push(value);
        }
    }
}

var td_template = 'td.field-{0}';

function enable_field_by_lookup_value(model, by_field, field, find_values, enable) {
	enable = (enable || false) ? 1 : 0;	// enable variable is boolean but we need it 1 or 0 for bitwise later
	model = model.toLowerCase();
    var table = $('div.inline-group#' + model + '_set-group').find('table > tbody');
    if ($(table).length == 0) 
    {
    	alert('Table ' + '"div.inline-group#' + model + '_set-group" not found' );	
    	return;
    }
    
    $(table).children('tr.has_original').each(function( index ) {
		lookup_value = $(this).find(td_template.replace('{0}', by_field) + ' > p').text();
		found = (find_values.indexOf(lookup_value) >= 0 ? 1 : 0);
		need_disable = found ^ enable;
		if (need_disable){
			var input = $(this).find(td_template.replace('{0}', field) + ' > input');
			$(input).attr("disabled", true);
		}
	});
    
}


function categoriesproperties_fields_disabled(table, field) {

    var count = 100;
    for (var i = 0; i < count; i++) {
        var input = $('#id_' + table + '_set-' + i + '-' + field);
        var row = $('#' + table + '_set-' + i);
        if ($(row).length == 0) { break; }
        //Checking whether Row contains external document or not. If yes, enabling delete checkbox
        var rowExternalDocument = $('#' + table + "_set-" + i + ":contains('External Documents')");
        if ($(rowExternalDocument).length == 0) {
            $(input).attr("disabled", true);
        }
    }
}



