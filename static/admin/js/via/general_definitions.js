/// This file is referenced by via\admin.py - viaAdmin

$(function(){	
	
	$('select[name=via_set-0-empi_type]').click(function(){
	
		var empi_type_val = $(this).val();
		var hmo_type_val = $('select[name=via_set-0-hmo_id]').val();
		
		if (empi_type_val == "FEDCDR")
		{
			$('select[name=via_set-0-hmo_id]').prop('disabled',false);
		}
		else
			{
			$('select[name=via_set-0-hmo_id]').val(0)
			$('select[name=via_set-0-hmo_id]').prop('disabled',true);
			}
	}).click();
});
