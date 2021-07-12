$(function(){
	var ch = $("#myhrconnectivityentity_set-0 :checkbox[name*='enable_my_hr_flow']");
	
	var fn = function() {
            if($(ch).prop('checked')){
	        	$("label[for*='pcehr_exist_url']").addClass("required");
				$("label[for*='my_hr_node_id']").addClass("required");
				$("label[for*='gain_access_url']").addClass("required");
				$("label[for*='get_document_url']").addClass("required");
				$("label[for*='my_hr_oid']").addClass("required");
				$("label[for*='get_document_list_url']").addClass("required");
				
	        }
	        else{
	        	$("label[for*='pcehr_exist_url']").removeClass("required");
				$("label[for*='my_hr_node_id']").removeClass("required");
				$("label[for*='gain_access_url']").removeClass("required");
				$("label[for*='get_document_url']").removeClass("required");
				$("label[for*='my_hr_oid']").removeClass("required");
				$("label[for*='get_document_list_url']").removeClass("required");				
	        }
		};
		
	$(ch).change(function() {fn(ch);});
	fn(ch);
})(django.jQuery);

