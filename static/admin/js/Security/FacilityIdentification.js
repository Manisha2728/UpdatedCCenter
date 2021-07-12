/// This file is referenced by scurity\admin.py - FacilityIdentification

$(function(){		

	if($("#id_securitygeneral_set-0-activate_facility_identification").is(':checked'))
	 {	
		$('#id_securitygeneral_set-0-facility_identification_excluded_codes').removeAttr("disabled");
	}
	else
	{
		$('#id_securitygeneral_set-0-facility_identification_excluded_codes').attr("disabled","disabled");
	}
	$('#id_securitygeneral_set-0-activate_facility_identification').change(function(){
		
		if (this.checked){
			
			$('#id_securitygeneral_set-0-facility_identification_excluded_codes').removeAttr("disabled");
		
		} else {
		
			$('#id_securitygeneral_set-0-facility_identification_excluded_codes').attr("disabled","disabled");
		
		}

	});	
});