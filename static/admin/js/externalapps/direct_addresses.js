$(function () {
    // Disable/enable fields according to reporting type
    var firstRow = $('#instance_set-0');
    var count = $(firstRow).parent().children('.has_original').length;

    for (var i = 0; i < count; i++) {
        var reportingType = $('#id_instance_set-' + i + '-mu_reporting_type');

        reportingType.click(function () {
            var idPrefix = '#' + $(this).attr('id').replace("-mu_reporting_type", "");
            var thumbrint = $(idPrefix + '-thumbprint');
            var login = $(idPrefix + '-mu_reporting_login');
            var password = $(idPrefix + '-mu_reporting_password');
            var appName = $(idPrefix + '-mu_reporting_app_name');
            var communityOid = $(idPrefix + '-mu_reporting_community_oid');

            var scmControls = [thumbrint];
            var twControls = [login, password, appName, communityOid];

            switch ($(this).val()) {
                case "SCM":
                    enableDisableControls(scmControls, "enable");
                    enableDisableControls(twControls, "disable");
                    break;
                case "TW":
                    enableDisableControls(scmControls, "disable");
                    enableDisableControls(twControls, "enable");
                    break;
                default:
                    enableDisableControls(scmControls, "disable");
                    enableDisableControls(twControls, "disable");
                    break;
            }
        }).click();
    }
});

function enableDisableControls(controlsList, actionType) {
    if (actionType === 'enable') {
        for (var itemToEnable in controlsList) {
            controlsList[itemToEnable].attr("disabled", false);
        }
    }
    else {
        for (var itemToDisable in controlsList) {
            controlsList[itemToDisable].attr("disabled", true);
            controlsList[itemToDisable].val("");
        }
    }
}