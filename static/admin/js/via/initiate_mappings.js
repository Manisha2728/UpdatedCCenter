$(function(){
	
	var servicestorestart = document.getElementsByClassName('services_to_restart_content info')[0].getElementsByTagName('li');
	for (var service=0; service<servicestorestart.length;service++) {
      if( servicestorestart[service].innerText == "VIA")
      	servicestorestart[service].innerText = "VIA(Needs to be restarted first)";
    }
	var OOBRowsCount = 38;   	
	// set DbMotion VIA Attribute Name and Description read only for OOB rows
	first_n_fields_readonly('initiatemappings', 'dbmotion_attribute_name', OOBRowsCount);
	first_n_fields_readonly('initiatemappings', 'dbmotion_attribute_description', OOBRowsCount);
	
	// Disable delete checkbox for OOB rows
	first_n_fields_disabled('initiatemappings', 'DELETE', OOBRowsCount);
	
	// Disable Initiate hub id issuer field if segment name is not "memIdent"
	var firstRow = $('#initiatemappings_set-0');
    var count = $(firstRow).parent().children('.has_original').length;

	for (var i = 0; i <= count; i++)
    {
        var select = $('#id_initiatemappings_set-' + i + '-initiate_hub_segment_name');
        select.click(function(){
        	var input = '#' + $(this).attr('id').replace("-initiate_hub_segment_name","-initiate_hub_id_issuer");
	        if($(this).val() == "memIdent")
	        	$(input).attr("disabled", false);
	        else
	        {
	        	$(input).attr("disabled", true);
	        	$(input).val("");
	        }
        }).click();
    }
});