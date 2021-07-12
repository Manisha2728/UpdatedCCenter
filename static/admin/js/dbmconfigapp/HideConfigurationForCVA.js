$(document).ready(function () {
    HideConfiurations();


});
function HideConfiurations() {
    var isCVA = false;
    //in case CVA application there is no need to present the following settings
    $("div").each(function () {
        var currentId = $(this).attr('class');
        if (isCVA)
        {
            switch (currentId) {
                case "form-row field-get_application_state_url":
                case "form-row field-launch_url":
                case "form-row field-is_user_alias_required":
                case "form-row field-is_window_resizable":
                case "form-row field-window_default_width_size field-window_default_height_size":
                case "form-row field-window_minimal_width_size field-window_minimal_height_size":
                case "form-row field-window_maximal_width_size field-window_maximal_height_size":
                case "form-row field-get_application_state_url":
                case "form-row field-get_application_state_url":
                    $(this).attr("style", "display:none;");
            }
        }
        else {
            if (currentId == "form-row field-app_name") {
                var textField = $(this).find('input');
                var appName = textField.attr('value');
                if (appName == "Clinical View Agent") {
                    isCVA = true;
                }
            }
        }
        
    });
}
