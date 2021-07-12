

function showAddAnotherModalPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var retVal = window.showModalDialog(href, name, 'resizable:yes; dialogWidth:960px; dialogHeight:640px;');	//scrollbars:yes;
    if (retVal) location.reload();
    return false;
}


(function($) {
	// Show either the drop down or the text box, according to the is_static checkbox selection.
	// -----------------------------------------------------------------------------------------
	
	// Arrange the TH
	$('#externalapplicationparameter_set-group fieldset>table th:eq(3)').hide();
	$('#externalapplicationparameter_set-group fieldset>table th:eq(2)').width(320);
	$('#externalapplicationparameter_set-group fieldset>table th:eq(2)').addClass('required');
	
	// assign the function to the checkbox change event
	$('#externalapplicationparameter_set-group input:checkbox[id$="is_static"]').change(is_static_click);
	
	// initialize all rows according to the checkbox state
	$('#externalapplicationparameter_set-group input:checkbox[id$="is_static"]').each(is_static_click);
	
	$( "body" ).append('<div id="dialog" title="dbMotion Parameters"></div>');
	
	// Dialog that shows dbMotion Parameters details
	$( "#dialog" ).dialog({
      autoOpen: false,
      height: 540,
      width: 780
      
    });
    $( "#dialog" ).append($("#opener").attr("dlgtext"));
    
    $( "#opener" ).click(function() {
      $( "#dialog" ).dialog( "open" );
    });
	
})(django.jQuery);

function ShowDialog(html){
	var divDlg = '<div id="dialog" title="dbMotion Parameters"></div>';
}

// Show the correct TD according to the checkbox state
function is_static_click(e) {
            $(this).closest('tr').children('.field-static_value').toggle(this.checked);
            $(this).closest('tr').children('.field-dbm_param').toggle(!this.checked);
		};