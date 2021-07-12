/// This file is referenced by via\admin.py - viaAdmin

$(function(){
	$('select[name=initiateconnection_set-0-initiate_version]').click(function(){
		if ($(this).val() == "PatientAdapter92")
		{
			$('input[name=initiatevpo_set-0-enable_federated_search]').prop("disabled", true);
			$('input[name=initiatevpo_set-0-enable_federated_search]').attr('checked',false);
			
			$('input[name=initiatevpo_set-0-enable_federated_match]').prop("disabled", true);
			$('input[name=initiatevpo_set-0-enable_federated_match]').attr('checked',false);
		}
		else
		{
			$('input[name=initiatevpo_set-0-enable_federated_search]').prop("disabled", false);
			$('input[name=initiatevpo_set-0-enable_federated_match]').prop("disabled", false);
			
		}
	}).click();
	
});