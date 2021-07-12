


$(document).ready(function () {
    //DisableLinkToEditWindowForCVA();
    SetDefaultPCAplicationNotToBeDeleted();
    HookEnabledCheckBoxChangedEvent();
    $('#culture_set-group').find('.services_to_restart_tag').remove();
});

function DisableLinkToEditWindowForCVA() {
    var cvaRow = $("#agentpphostedapp_set-group tr[id=agentpphostedapp_set-1");
    var applicationNameLink = cvaRow.find('td.field-app_name_url a');
    var text = applicationNameLink.text();
    //disable the CVA edit window opening - by replacing the link element
    applicationNameLink.replaceWith("<p>" + text + "</p>");
}

function SetDefaultPCAplicationNotToBeDeleted() {
	//search for PC applications
    $("#agentpphostedapp_set-group tr").each(function () {
        var currentId = $(this).attr('id');
        //three applications are PV, CVA and CDP. Need to disable the delete check box
        if (currentId == "agentpphostedapp_set-0") {
            var columns = $(this).find('td').eq(6);
            var box = columns.find('input:checkbox');
            box.attr("disabled", true);
        }
        if (currentId == "agentpphostedapp_set-1") {
            var columns = $(this).find('td').eq(6);
            var box = columns.find('input:checkbox');
            box.attr("disabled", true);
        }
        if (currentId == "agentpphostedapp_set-2") {
            var columns = $(this).find('td').eq(6);
            var box = columns.find('input:checkbox');
            box.attr("disabled", true);
        }
    });
}

function HookEnabledCheckBoxChangedEvent()
{    	
		//Hook For workflow change
		$("#id_agentppgeneraldefinitions_set-0-default_mode_0").on("change", function () { ValidationForWorflowChange(this); });
    	$("#id_agentppgeneraldefinitions_set-0-default_mode_1").on("change", function () { ValidationForWorflowChange(this); });
		
		//Hook for every application check box
        //each row in div #agentpphostedapp_set-group
        $("#agentpphostedapp_set-group tr").each(function () {
            var currentId = $(this).attr('id');
            //ignore empty row
            if (currentId != "agentpphostedapp_set-empty") {

                //get the third column 
                var columns = $(this).find('td').eq(2);
                //find check box in cell
                var box = columns.find('input:checkbox');
                //hook check box checked changed
                box.change(function () {
                    EnabledCheckBoxChanged("PCMode");

                });                
            }
        });
        
        $("#agentsmartonfhirapp_set-group tr").each(function () {
            var currentId = $(this).attr('id');
            //ignore empty row
            if (currentId != "agentpphostedapp_set-empty") {

                //get the third column 
                var columns = $(this).find('td').eq(2);
                //find check box in cell
                var box = columns.find('input:checkbox');
                //hook check box checked changed
                box.change(function () {
                    EnabledCheckBoxChanged("PCMode");

                });                
            }
        });

        $("#agentusercentricapp_set-group tr").each(function () {
            var currentId = $(this).attr('id');
            //ignore empty row
            if (currentId != "agentusercentricapp_set-empty") {

                //get the third column 
                var columns = $(this).find('td').eq(2);
                //find check box in cell
                var box = columns.find('input:checkbox');
                //hook check box checked changed
                box.change(function () {
                    EnabledCheckBoxChanged("PHMode");
                });
            }
        });
        
        //Hook for Minimize mode default state check box
        $("#id_agentppgeneraldefinitions_set-0-agentpp_minimized_mode").on("change", function () { ValidationForMinimizedMode(); });
}
    
function EnabledCheckBoxChanged(mode) {
	
	var saveButtonEnabled = true; 
	if (mode == "PCMode" && $("#id_agentppgeneraldefinitions_set-0-default_mode_1").get(0).checked) {
        saveButtonEnabled = PCValidationEanabledApplication();
    }
    if (mode == "PHMode" && $("#id_agentppgeneraldefinitions_set-0-default_mode_0").get(0).checked) {
        saveButtonEnabled = PHValidationEnabledApplication();
    }
    //if save button is disabled from previous decision don't need to check for minimized mode'
    if(saveButtonEnabled)
    {
    	ValidationForMinimizedMode();
    }
}

function ValidationForMinimizedMode()
{
	var applicationState = GetApplicationsState();
	var isAppPHEnabled = IsAnyPHApplicationEnabled();
	var isMinimizedModeEnabled = $("#id_agentppgeneraldefinitions_set-0-agentpp_minimized_mode").get(0).checked;
	
	var validationResult = isMinimizedModeEnabled && ((!isAppPHEnabled && applicationState.enabledPCAplications == 1) || (isAppPHEnabled && applicationState.enabledPCAplications == 0));

	if(validationResult)
	{
		alert("Minimized Mode can't be set as default state, when only one application is enabled.");
	}
	
	//Still need to validate the applications state before minimize validation
	var saveButtonEnabled = true; 
	if ($("#id_agentppgeneraldefinitions_set-0-default_mode_1").get(0).checked) {
        saveButtonEnabled = PCValidationEanabledApplication();
    }
    if ($("#id_agentppgeneraldefinitions_set-0-default_mode_0").get(0).checked) {
        saveButtonEnabled = PHValidationEnabledApplication();
    }
    if(saveButtonEnabled)
    {
    	//disabled/enabled save button
    	$('input[name=_continue]').attr("disabled", validationResult);
    }
}

function ValidationForWorflowChange(input) {  
	var saveButtonEnabled = true;
    if ($(input).val() == "PCMode") {

        saveButtonEnabled = PCValidationEanabledApplication();
    }
    if ($(input).val() == "PHMode") {

        saveButtonEnabled = PHValidationEnabledApplication();
    }
    if(saveButtonEnabled)
    {
    	ValidationForMinimizedMode();
    }
}

function PHValidationEnabledApplication() {
    var isAppEnabled = IsAnyPHApplicationEnabled();
    if (!isAppEnabled) {
        alert("At least one Population Health Application must be selected");
    }
    //disabled/enabled save button
    $('input[name=_continue]').attr("disabled", !isAppEnabled);
    //return the decision if the save button is enabled
    return isAppEnabled;
}

function PCValidationEanabledApplication() {
	
	var applicationState = GetApplicationsState();
    if(applicationState.enabledPCAplications > 7)
    {
    	alert("Only seven Patient Centric apllications can be enabled");
    }
    
    if (!applicationState.isAppPCEnabled && !applicationState.isAppSOFEnabled) {
        alert("At least one Patient Centric Application must be selected");
    }
    var saveButtonDisabled = !applicationState.isAppPCEnabled && !applicationState.isAppSOFEnabled || applicationState.enabledPCAplications>7;
    //disabled/enabled save button
    $('input[name=_continue]').attr("disabled", saveButtonDisabled);
    return !saveButtonDisabled;
}

function IsAnyPHApplicationEnabled()
{
	var isAppEnabled = false;
    // agentusercentricapp_set - group
    $("#agentusercentricapp_set-group tr").each(function () {
        var currentId = $(this).attr('id');
        if (currentId != "agentusercentricapp_set-empty") {

            //get the third column 
            var columns = $(this).find('td').eq(2);
            //find check box in cell
            var box = columns.find('input:checkbox');
            if (!isAppEnabled) {
                isAppEnabled = box.is(":checked");
            }
        }
    });
    return isAppEnabled;
}

function GetApplicationsState()
{
	var isAppPCEnabled = false;
    var isAppSOFEnabled = false;
    var enabledPCAplications = 0;
    //each row in div #agentpphostedapp_set-group
    $("#agentpphostedapp_set-group tr").each(function () {
        var currentId = $(this).attr('id');
        if (currentId != "agentpphostedapp_set-empty") {

            //get the third column 
            var columns = $(this).find('td').eq(2);
            //find check box in cell
            var box = columns.find('input:checkbox');            
            if (!isAppPCEnabled) {
                isAppPCEnabled = box.is(":checked"); 
            }
            if(box.is(":checked")){
            	enabledPCAplications = enabledPCAplications + 1;
            }
        }

    });
    
    $("#agentsmartonfhirapp_set-group tr").each(function () {
        var currentId = $(this).attr('id');
        if (currentId != "agentsmartonfhirapp_set-empty") {

            //get the third column 
            var columns = $(this).find('td').eq(2);
            //find check box in cell
            var box = columns.find('input:checkbox');            
            if (!isAppSOFEnabled) {
                isAppSOFEnabled = box.is(":checked");
            }
            if(box.is(":checked")){
            	enabledPCAplications = enabledPCAplications + 1;
            }
        }

    });
    return {
    	isAppPCEnabled: isAppPCEnabled,
    	isAppSOFEnabled: isAppSOFEnabled,
    	enabledPCAplications: enabledPCAplications
    };
}


