/// This file is referenced by externalapps\admin.py - InstanceAdmin
$(function(){	
    $('#add_id_instance_properties').after('<a style="margin-left:8px;" id="edit_instance_properties_link" href="#"></a>');
   
	setInstancePropertiesLink($('select[name=instance_properties]'))
		.change(function(){setInstancePropertiesLink(this);});
		
	$('div[id^=participant_set]').each(function() {
		$(this).data("default", $(this).clone());
	});
	 //hook user mapping check change event
    $("#id_is_user_mapping_enabled").change( function () { IsUserMappingDisabledValidation(this); });
	$('input[name=context_type]').change(function() {contextTypeChanged(this);});
	contextTypeChanged($('input[name=context_type]:checked'));
	
	$('form#instance_form').submit(function() {
		$("div[id^=participant_set]:hidden").each(function() {
			data = $(this).data("default");
			data.hide();
			$(this).replaceWith(data);
		});
	});
		
	
	$('#id_user_mapping_file_path').on('input',function(e){
		var userMappingFilePath = $("#id_user_mapping_file_path");
		$('input[name=_continue]').attr("disabled", (userMappingFilePath.val().trim().length == 0));
	    });
	
	// -- Passcode
	
    $('textarea[name$="passcode"]').after('<input type="Button" value="Generate" id="generate_passcode" class="passcode" onclick="generatePasscode(this);" />');

    // Show/hide fields according to reporting type
    var reportingTypeDropdown = $('#id_mu_reporting_type');

    reportingTypeDropdown.click(function () {
        showHideMUReportingFields($(this).val());
    }).click();
});

function IsUserMappingDisabledValidation() {	
    var isUserMappingEnabled = $("#id_is_user_mapping_enabled").is(':checked');
    $("#id_user_mapping_file_path").attr("disabled", !isUserMappingEnabled);
    var isFilePathDefined = true;
    
    //get user mapping div    
    var fieldset = $("#id_user_mapping_file_path").parent().closest('fieldset');
    if (isUserMappingEnabled)
    {
    	//show user mapping group
    	fieldset.show();
	    var userMappingFilePath = $("#id_user_mapping_file_path");	    
	    isFilePathNotDefined = (userMappingFilePath.val().length == 0);
	    $("label[for=id_user_mapping_file_path]").addClass('required');
	    
	    
    }
    else
    {        	    	
    	 //uncheck  all check box in fieldset
    	 fieldset.find('input[type=checkbox]:checked').removeAttr('checked');
    	 fieldset.find('textarea').val('');
    	 $("label[for=id_user_mapping_file_path]").removeClass('required');
    	 //close user mapping  group
    	 fieldset.hide();
    }
    
    //disabled/enabled save button
    $('input[name=_continue]').attr("disabled", isUserMappingEnabled && isFilePathNotDefined); 
}





function generatePasscode(obj){
	$.ajax({
		cache: false,
	    url: '/passcode',
	    type: 'get', //this is the default though, you don't actually need to always mention it
	    success: function(data) {
	    	$(obj).siblings('textarea[name$="passcode"]').val(data);
	    },
	    failure: function(data) { 
	        alert('Error generating passcode');
	    }
	});
}


function setInstancePropertiesLink(input){
	if ($(input).val() === "")
		$('#edit_instance_properties_link').hide();
    else
    	$('#edit_instance_properties_link')
            	.attr('href', '/admin/externalapps/instanceproperties/' + $(input).val() + '/')
            	.text('Go to ' + $(input).find('option:selected').text())
            	.show();
    
    return input;
    
}

function contextTypeChanged(input){
	if ($(input).val() == "NonCcow")
	{
		$("div[id^=participant_set]:eq(0)").hide();
		$("div[id^=participant_set]:eq(1)").hide();
        $("div.form-row.field-ccow_item_name").hide();
	    $("div.form-row.field-exclude_dash_from_mrn").hide();
		$("div.form-row.field-interceptor_type").show();
		$("label[for=id_interceptor_type]").addClass('required');
		//handle user mapping
		$("div.form-row.field-is_user_mapping_enabled").show();
		$( "div.form-row.field-nonCcowPluginType" ).show();
		//Create dropdown list of options for NonCCow context type
		/*$( "div.form-row.field-interceptor_type" ).find('textarea').val("");
		var opt = "<select id='context-provider-options'></select>";
		$("div.form-row.field-context_type").append(opt);*/
		var dropList = $( "div.form-row.field-nonCcowPluginType" ).find( "select" );
		
		//Hide UI Automation configuration file text area - need onl;y in case of UI Automation is selected
		if ($.inArray(dropList.find('option:selected').text(), ['UI Automation']) > -1)
		{
			$( "div.form-row.field-uiAutomation_config_file_path" ).show();
			$( "div.form-row.field-interceptor_type" ).find('textarea').attr("readonly", true);
			if($( "div.form-row.field-uiAutomation_config_file_path" ).find('textarea').val().trim() == "")
				$('input[name=_continue]').attr("disabled", true); 					      
			else
				$('input[name=_continue]').attr("disabled", false);
		}
		else
		{
			$('input[name=_continue]').attr("disabled", false);
			$( "div.form-row.field-uiAutomation_config_file_path" ).hide();
		}
				
		dropList.change(function () {
			//Put to Plugin type name value of dropdown list
			$( "div.form-row.field-interceptor_type" ).find('textarea').val(dropList.val());						
			//Disable/Enable editing to Plugin Type name accordingly to isHardCodedPluginData attribute of selected option
			if ($.inArray(dropList.find('option:selected').text(), ['UI Automation']) > -1)
			{
				$( "div.form-row.field-interceptor_type" ).find('textarea').attr("readonly", true);				
			}
			else
			{
				$( "div.form-row.field-interceptor_type" ).find('textarea').attr("readonly", false);				
			}			
			if (dropList.find('option:selected').text() != 'UI Automation')
			{	
				//Hide UI Automation configuration File path
				$( "div.form-row.field-uiAutomation_config_file_path" ).hide();
				$("label[for=id_uiAutomation_config_file_path]").removeClass('required');
				$( "div.form-row.field-uiAutomation_config_file_path" ).find('textarea').val("");
				$('input[name=_continue]').attr("disabled", false);
			}
			else
			{
					//Show UI Automation configuration File path					
					$("label[for=id_uiAutomation_config_file_path]").addClass('required');
					$( "div.form-row.field-uiAutomation_config_file_path" ).show();
					if($( "div.form-row.field-uiAutomation_config_file_path" ).val().trim() == ""){
						$('input[name=_continue]').attr("disabled", true); 
				      }
					//The textarea should not be empty
					$( "div.form-row.field-uiAutomation_config_file_path" ).bind('input propertychange', function() {						
						if($( "div.form-row.field-uiAutomation_config_file_path" ).find('textarea').val().trim() == "")
							$('input[name=_continue]').attr("disabled", true); 					      
						else
							$('input[name=_continue]').attr("disabled", false);
					});
			}
	    });			 
	}
	else 
	{
		//disabled/enabled save button
	    $('input[name=_continue]').attr("disabled", false); 
		$("div.form-row.field-interceptor_type").hide();			
		$("label[for=id_interceptor_type]").removeClass('required');		
		$("label[for=id_user_mapping_file_path]").removeClass('required');	
			
		//handle user mapping
		$("#id_is_user_mapping_enabled").prop("checked", false); 
		$("div.form-row.field-is_user_mapping_enabled").hide();
		
		//Hide UI Automation configuration File path
		$( "div.form-row.field-uiAutomation_config_file_path" ).hide();
		$("label[for=id_uiAutomation_config_file_path]").removeClass('required');
		$( "div.form-row.field-uiAutomation_config_file_path" ).find('textarea').val("");
		$('input[name=_continue]').attr("disabled", false);
		$( "div.form-row.field-nonCcowPluginType" ).hide();
		
		//Remove NonCCOW context types dropdownlist
		var dropList = $( "div.form-row.field-context_type" ).find( "select" );		
		dropList.remove();
		
		if ($(input).val() == "CcowParticipant"){
			$("div[id^=participant_set]:eq(1)").hide();
			$("div[id^=participant_set]:eq(0)").show();
            $("div.form-row.field-ccow_item_name").show();
		    $("div.form-row.field-exclude_dash_from_mrn").show();
		}
		else if ($(input).val() == "CcowReceiver")
		{
			$("div[id^=participant_set]:eq(0)").hide();
			$("div[id^=participant_set]:eq(1)").show();
            $("div.form-row.field-ccow_item_name").show();
		    $("div.form-row.field-exclude_dash_from_mrn").show();
		}
	}
	IsUserMappingDisabledValidation();	
	return input;
	 
}

function showHideMUReportingFields(reportingType) {
    var thumbrint = $('#id_thumbprint');
    var login = $('#id_mu_reporting_login');
    var password = $('#id_mu_reporting_password');
    var appName = $('#id_mu_reporting_app_name');
    var communityOid = $('#id_mu_reporting_community_oid');

    var scmControls = [thumbrint];
    var twControls = [login, password, appName, communityOid];

    switch (reportingType) {
        case "SCM":
            showHideControls(scmControls, "show");
            showHideControls(twControls, "hide");
            break;
        case "TW":
            showHideControls(scmControls, "hide");
            showHideControls(twControls, "show");
            break;
        default:
            showHideControls(scmControls, "hide");
            showHideControls(twControls, "hide");
            break;
    }
}

function showHideControls(controlsList, actionType) {
    if (actionType === 'show') {
        for (var itemToShow in controlsList) {
            // parent().parent() to show the whole div that incldes the control
            controlsList[itemToShow].parent().parent().show();
        }
    }
    else {
        for (var itemToHide in controlsList) {
            // parent().parent() to hide the whole div that incldes the control
            controlsList[itemToHide].parent().parent().hide();
            controlsList[itemToHide].val("");
        }
    }
}

