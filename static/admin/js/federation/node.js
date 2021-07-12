/// This JS is used for both Node List page and Node Setting page (same admin)

$(function(){
	
	if ($('#changelist').length) {
		//	NODE LIST
		
		// cancel the "banded rows" design
		$('tr', 'table#result_list').removeClass().addClass('row2');
		// highlight local node
		$("img[alt='True']", 'td.field-is_local').closest('tr').removeClass().addClass('row-highlight');
		// remove "False" icon from isLocal
		$("img[alt='False']", 'td.field-is_local').remove();

		// remove "False" icon from "Patient List retrieves from 
		$("img[alt='False']", 'td.field-pl_active').remove();
		
		var html = '<input type="button" value="Apply" id="apply_changes" class="apply" onclick="applyChanges(this);" />' +
					'<span style="margin-left:16px;" id="txt_result"></span>';
		
		$('#changelist').after(html);
		
		$('#changelist').css('width', 'auto');
	}
	else {
		// NODE EDIT
		
		$('select[name=request_from]')
			.change(function() { setGroupHref($('select[name=request_from]')); });
		setGroupHref($('select[name=request_from]'));
	
		$('select[name=response_to]')
			.change(function() { setGroupHref($('select[name=response_to]')); });
		setGroupHref($('select[name=response_to]'));
	
		/// the original function "dismissAddAnotherPopup" is in:
		/// "C:\Python27-11\Lib\site-packages\django\contrib\admin\static\admin\js\admin\RelatedObjectLookups.js"
		/// This function will handle the second dropdown object when closing the popup window.
		window.ORIGINAL_dismissAddAnotherPopup = window.dismissAddAnotherPopup;
        window.dismissAddAnotherPopup = function(win, newId, newRepr) {
        	// add the new group to the other select (without selecting it)
        	var name = windowname_to_id(win.name)=="id_response_to" ? "id_request_from" : "id_response_to";
            var elem = document.getElementById(name);
            var o;
            if (elem) {
                var elemName = elem.nodeName.toUpperCase();
                if (elemName == 'SELECT') {
                    o = new Option(newRepr, newId);
                    elem.options[elem.options.length] = o;
                }
            }
            
            ORIGINAL_dismissAddAnotherPopup(win, newId, newRepr);
        };
        
        window.dismissEditPopup = function(win, newId, newRepr) {
        	// set the editted item
        	var name = windowname_to_id(win.name);
            var elem = document.getElementById(name);
            var opt_val;
            if (elem) {
            	$(elem).find("option:selected").text(newRepr);
            	opt_val = $(elem).find("option:selected").val();
            }
            
            // handle the other dropdown
            name = name=="id_response_to" ? "id_request_from" : "id_response_to";
            elem = document.getElementById(name);
            if (elem) {
            	$(elem).find("option[value='" + opt_val + "']").text(newRepr);
            }
            
            win.close();
        };
	}
});


function applyChanges(obj){
	$("#txt_result").html('');
	$(obj).prop('disabled', true);
	$.ajax({
		cache: false,
	    url: '/federation/apply/',
	    type: 'get', //this is the default though, you don't actually need to always mention it
	    success: function(data) {
	    	$("#txt_result").html(data);
	    	$(obj).prop('disabled', false);
	    },
	    failure: function(data) {
	        $("#txt_result").html(data);
	    }
	});
}

function setGroupHref(input){
	selectName = $(input).attr('name');
	selectValue = $(input).val();
	a = $('a#edit_id_' + selectName);
	a.removeAttr('href');
	if (selectValue != -1 && selectValue != 0)	// Not <None> or <All>
	{
		a.attr('href', a.attr('href_base').replace('{0}', selectValue));
	}
}


