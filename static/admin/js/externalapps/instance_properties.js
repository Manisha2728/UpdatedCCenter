/// This file is referenced by externalapps\admin.py - InstanceAdmin
$(function(){
	$('#id_categories_available_for_send').on("keyup", function(){
	
		updateState();
	})
	
	updateState();
});

function updateState(){
	var categories = $('#id_categories_available_for_send').val(); 
	if (categories == null || categories == undefined) return;
	var domains = categories.split(',');
	for (var i = 0; i < domains.length; i++)  
		domains[i] = domains[i].trim();
	if (domains.indexOf("All") >= 0 || domains.indexOf("ClinicalDocuments") >= 0)
	{
		$('#id_send_to_my_EHR_ccda_only').prop("disabled", false);
	}
	else
	{
		$('#id_send_to_my_EHR_ccda_only').prop("disabled", true);
		$('#id_send_to_my_EHR_ccda_only').prop("checked", false);
	}
}

container = null;

$(function(){
	
	container = $('<span/>').insertAfter($('div.form-row.field-app_id > div'));
	
	div = $('div.form-row.field-app_id_description');
	div.hide();
	container.append(div.find('div#app_id_description > span'));
	
	$('<span name="prefix" />').insertBefore($('input[name$=suffixes]'));

	$('tr.form-row').each(bindRow);
    
	$('select[name=app_id]')
		.change(setAppIdDescription);
	setAppIdDescription($('select[name=app_id]')[0]);
	
	
});

function updateUserContextRow(row){
	var ad_admin = false;
	var prefix = '';
	
	var input = $(row).find('select[name$=user_context_type]');
	if (input.length == 0) return null;
	
	switch ($(input).val()){
		case "Managed":
			ad_admin = true;
			prefix = 'user.id.logon.';
			break;
		case "UnmanagedCredentials":
			prefix = 'user.id.logon.';
			break;
		case "UnmanagedSAML":
			prefix = 'user.tk.saml.';
			break;
		case "SendToMyEHR":
			prefix = 'user.id.logon.';
			break;
	}
	
	if (ad_admin){
		$(row).find('input[name$=ad_domain]').prop('disabled', false);
	}
	else{
		$(row).find('input[name$=ad_domain]').val('').prop('disabled', true);
	}
	
	$(row).find('span[name=prefix]').text(prefix);
	
	return $(input);
}

function updatePatientContextRow(row){
	var input = $(row).find('select[name$=suffix_type]');
	if (input.length == 0) return null;
	
	if ($(input).val() == "MRN"){
		$(row).find('span[name=prefix]').text('patient.id.mrn.');
		$(row).find('input[name$=suffixes]').show();
	}
	else{
		$(row).find('span[name=prefix]').text('patient.id.mpi');
		$(row).find('input[name$=suffixes]').hide();
	}
	return input;
}

function bindRowToFunction(r, f){
	triggerInput = f(r);
	if (triggerInput){
		triggerInput.change(
			function(){ f(r); } 
		);
	}
}

// Implementing bindRow that is called from dbm_common.js with the object <row>
// whenever the "Add another..." link is clicked.
function bindRow(index_or_row, row){
	if (row === undefined) {
	    row = index_or_row;
	}
	
	bindRowToFunction(row, updateUserContextRow);
	bindRowToFunction(row, updatePatientContextRow);
	
}

function setAppIdDescription(input){
	$(container).find('span[id^=appid]').hide();
	$('a#edit_id_app_id').removeAttr('href');
	if ($(input).val() != null && $(input).val() != "")
	{
		$(container).find('span[id=appid_' + $(input).val() + ']').show();
		$('a#edit_id_app_id').attr('href', $('a#edit_id_app_id').attr('href_base').replace('{0}', $(input).val()));
	}
}



