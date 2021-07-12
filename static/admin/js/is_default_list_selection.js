
$(document).ready(function() {	
	$("input[name*='isDefaultList']").click(function() {				
	    $("input[name*='isDefaultList']").attr("checked",false);	    
	    $(this).prop('checked', true);		
	});
	$("input[name*='enabled']").click(function() {				
	    if (!$(this).is(':checked'))
	    {
	    	var isDefault = $(this).parent().next().find('input');
	    	if (isDefault.is(':checked'))
	    	{
	    		alert('Note: If the Default checkbox is checked, then the Enabled checkbox must also be checked.')
	    		$(this).prop('checked', true);
	    	}else{
	    		$(this).parent().next().find('input').prop('disabled', true); 
	    	}	    	  	
	    }else {
	    	$(this).parent().next().find('input').prop('disabled', false);
	    }
	});
})