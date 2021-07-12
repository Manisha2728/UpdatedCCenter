$(function(){
	
    // bug in Django. Empty field labels dont hide the ':'.
    // note: only set .text(), not hide, for proper aligning
    $("label").filter(function () { return $(this).html() == ":"; }).text("");
    
    // tbener Jan 2017 - fix bug - ST-2059 CCenter history is not saved properly for some objects
    // We use to disable inputs in different cases. A disabled input is not passed in Submit and Django interprates
    //   it as a changed field. The result is unnecessary entries in history.
    $("form").submit(function()
	{
	    $("input:disabled").prop("disabled", false);
	    return true;
	});
    
    
    ///////////////////////
    // Services to restart
    ///////////////////////

    $('.services_to_restart_tag').click(function(){
    	// fieldset section header
		$(this).closest('h2').siblings('h2 ~ .services_to_restart_content').fadeToggle();
		// inline header
		$(this).closest('h2').siblings('.services_to_restart_container').children('.services_to_restart_content').fadeToggle();
	});
	
	$('.services_to_restart_content > .inline-deletelink').click(function( ){
		$(this).closest('.services_to_restart_content').fadeOut("slow"); 
	});
    

});


function ActivateChangedEvent(){
		changesMade = false;
    	saving = false;
    
        $('#content-main form').submit(function(e) {
            saving = true;
        });

        $('#content-main input[type!="checkbox"]').change(function(e) {
            $(this).addClass("dbmotion-changed");
            changesMade = true;
        });

        $('#content-main input[type="checkbox"]').change(function(e) {
            var label = $("label[for='"+$(this).attr('id')+"']").addClass("dbmotion-changed");

            changesMade = true;
        });

        $('#content-main td>input[type="checkbox"]').change(function(e) {
            $(this).parent().closest('tr').addClass('dbmotion-changed');

            changesMade = true;
        });

        $('#content-main select').change(function(e) {
            $(this).addClass("dbmotion-changed");

            changesMade = true;
        });

        $('#content-main input:radio').change(function(e) {
            $(this).parent().addClass("dbmotion-changed");

            changesMade = true;
        });
        
        $('#content-main input:file').change(function(e) {
            $("label[for='"+$(this).attr('id')+"']").addClass("dbmotion-changed");

            changesMade = true;
        });
        
        $('#content-main textarea').change(function(e) {
            $(this).addClass("dbmotion-changed");

            changesMade = true;
		});
		
		$('#content-main .sortable').on( "sortstop", function( event, ui ) {
			$(this).addClass("dbmotion-changed");
			changesMade = true;
		});

        $(window).on('beforeunload', function(){
            if (changesMade && !saving) {
                return 'You have made changes you haven\'t saved!';
            }
        });
	
}

function afterTabularAddAnother(row){
	// KI - existing inputs will be handled twice
	ActivateChangedEvent();
	
	// see externalapps\instance_properties.js for implementation example
	if (typeof(bindRow) == "function")
		bindRow(row);
}

//////////////////////////

/// the original function "showAddAnotherPopup" is in:
/// "C:\Python27\Lib\site-packages\django\contrib\admin\static\admin\js\admin\RelatedObjectLookups.js"
/// Using the "showEditPopup" function will result in the following "dismissEditPopup"
function showEditPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^edit_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href;
    if (href == '') return false;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1&_popupex=1';
    } else {
        href  += '&_popup=1&_popupex=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

/// the original function "dismissAddAnotherPopup" is in:
/// "C:\Python27\Lib\site-packages\django\contrib\admin\static\admin\js\admin\RelatedObjectLookups.js"
/// This function will cause the parent window to refresh when closing the popup window.
function dismissEditPopup(win, objId, newRepr) {
    // objId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.

	win.opener.location.reload();
	// * Uncomment the following block instead, for a message Refreshing...
    //var container = $("#container", win.opener.document);
    //$(container).append('<div class="center">Refreshing...</div>');
    //window.setTimeout(function(){win.opener.location.reload();},100);
    
    
    
    try{
	    objId = html_unescape(objId);
	    newRepr = html_unescape(newRepr);
	    var name = windowname_to_id(win.name);
	    
	    if (name){
		    var elem = document.getElementById(name);
		    
		    if (elem) {
		    	try {
				    name = elem.prop('tagName').toUpperCase();
				}
				catch(err) {
				    name = '';
				}
		        if (name == 'SELECT') {
		        	// todo: update information if needed
		        	//$(elem).click();
		            
		        } else if (name == 'INPUT') {
		            // probably nothing to do here
		        }
		    } 
	    }
    }
    finally{
    	win.close();
    }
}

/*
 * A disabled input will not be submitted.
 * This function creates a hidden (or invisible) cloned input to hold the value.
 * 
 * Checkbox: a disabled checkbox turns the value in Django to false. Replacing it by a Hidden Input does the same.
 * 			 This solution cloning to invisible checkbox which keeps the value.
 * 
 * Note: make sure to use this function to disable any Input element that might need to hold data.
 * 		 Extend this function as needed.
 * 
 * tbener  Feb 16, 2016
 */
function disable_input(input){
	switch($(input).attr("type")){
		case "checkbox":
			if ($( input ).prop( "checked" )){
				var new_input = $(input).clone().hide();
				$(input).after(new_input);
			}
			// Fall-Through to disable original input
		default:
			$(input).prop("disabled", true);
	}
}

function grayedOut(input, isGrayedOut){
	if (isGrayedOut)
	{
		input.prop("readonly", true);
		input.css("background-color", "#EBEBE4");
		input.css("color", "#AAA");
	}
	else
	{
		input.prop("readonly", false);
		input.css("background-color", "white");
		input.css("color", "black");
	}
}
