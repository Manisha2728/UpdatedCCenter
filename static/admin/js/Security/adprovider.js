$(function(){
	var restartdbMotionAlert = '<div><p class="alertnote">After making a change in the configuration of managed users, Security service and IIS must be restarted for the change to be applied.</p>'
	$('#changelist').before(restartdbMotionAlert);
	
	// add Test Connection button
	
	var html = '<div class="form-row">' +
						'<input type="button" value="Test Connection" id="btn_test_connection" onclick="testConnection(this);" />' +
						'<span style="margin-left:16px;" id="txt_result"></span>' +
						'<div><br/>In the case of a trusted domain, the fields User Name and Password will be used for testing purpose only.</div>' +
					'</div>';
		$('div.form-row.field-untrusted_ad_user_password')
			.after(html);
					
		$('#changelist').css('width', 'auto');		
		
		// // add disabling the user+password section on selection :
		$("#id_untrusted_ad").click(UnTrusted);
		UnTrusted();
		
		setUseDnlState();
		$('#id_netbios_domain_name').keyup(function(){
			setUseDnlState();
		});
});

function UnTrusted(){		
	// add disabling the user+password section on selection :
	if($("#id_untrusted_ad").is(':checked'))
	 {	
		$('#id_untrusted_ad_user_name').removeAttr("disabled");
		$('#id_untrusted_ad_user_password').removeAttr("disabled");
	}
	else
	{
		$('#id_untrusted_ad_user_name').val("");
		$('#id_untrusted_ad_user_password').val("");
		$('#id_untrusted_ad_user_name').attr("disabled","disabled");		
		$('#id_untrusted_ad_user_password').attr("disabled","disabled");
	}	
}


function testConnection(obj){
	$("#txt_result").html('Please wait...');
	$(obj).prop('disabled', true);
	
	var domain = $('input[name="domain_name"]').val();
	var port = $('input[name="domain_port"]').val();
	var container = $('input[name="container"]').val();
	var untrusted_ad = $('input[name="untrusted_ad"]').prop('checked');
	var untrusted_ad_user_name = $('input[name="untrusted_ad_user_name"]').val();
	var untrusted_ad_user_password = $('input[name="untrusted_ad_user_password"]').val();
	
	$.post('/security/test_connection/', {domain: domain, port: port, container: container, is_untrusted: untrusted_ad, user: untrusted_ad_user_name, password: untrusted_ad_user_password}, 
		function(data){
	    	$("#txt_result").html(data);
		})
		.fail(function(o, status, msg) {
			$("#txt_result").html('Unexpected error occurred');
		    //alert( msg );
		})
		.always(function() {
		    $(obj).prop('disabled', false);
		});

}

function setUseDnlState()
{
    if (!$('#id_netbios_domain_name').val() || $('#id_netbios_domain_name').val().length == 0)
	{
		$('#id_use_dnl_format').prop("disabled", true);
		$('#id_use_dnl_format').prop("checked", false);
	}
	else
	{
		$('#id_use_dnl_format').prop("disabled", false);
	}
}
