/// This file is referenced by externalapps\admin.py - EhrAdmin

$(function(){
	$('select[name=deployment_type]').click(function(){
        $('div.field-detection_launch_title').toggle($(this).val() != 'Web');
	    $('div.field-detection_window_class').toggle($(this).val() != 'Web');
		$('div.field-detection_title').toggle($(this).val() != 'Web');
		$('div.field-detection_follow_focused_window').toggle($(this).val() != 'Web');
		$('div.field-detection_version').toggle($(this).val() == 'Local');
		$('div.field-detection_exe').toggle($(this).val() == 'Local');
		$('div.field-detection_url').toggle($(this).val() == 'Web');
		$('div.field-prevent_detected_window_topmost').toggle($(this).val() != 'Web');
		
	}).click();
	
	initPreview();
	
});


/*
 
 EHR Agent Positioning Preview Functions 
-------------------------------------------*/

$(document).keypress(function(e) {
    if(e.which == 13) {
    	if (isPreviewActive()){
    		e.preventDefault();
    	 	updateAgentByFields();
    	}
    }
});

var updating = false;
var offsetx = 0;
var offsety = 0;
var divOrgFields;
var divFields;

function initPreview(){
	// copy fields to ehr window
	divOrgFields = $('div.form-row.field-position_app_corner > div.field-box');
	divFields = divOrgFields.clone();
	divFields.appendTo('#preview_fields')
		.find('label')
		.removeClass('required')
		.addClass('aligned');
		
		
	// set inputs event handlers
 	$('#preview_wrapper').find('select, input[type="text"], input[type="checkbox"]').off()
 		.each(function() {
 			$(this).attr('name', 'preview_' + $(this).attr('name'));
 	});
 	
	divFields.find('select')
		.change(function(){
			updateFieldsByAgent();
			showCorners();
		});
		
	divFields.find('input[type="text"]')
		.change(function(){updateAgentByFields();});
		
	$('#preview_close').click(function(){ endPreview(false); });
	$('#preview_ok, #preview_apply').click(copyToPage);
	$('#preview_ok, #preview_cancel').click(endPreview);
	
	$('#preview_snap').change(function(e) {$('#preview_agent').draggable( "option", "snap", this.checked );});
	
	
	$('#preview_ehr').draggable({
		start: updateOffset(),
		drag: function( event, ui ) {
			$('#preview_agent').css({
				top: ui.offset.top + offsety,
				left: ui.offset.left + offsetx
			});
		}
	});
	
	$('#preview_agent').draggable({
		
		drag: function( event, ui ) {
			updateFieldsByAgent();
		},
		stop: function( event, ui ) {
			
			updateFieldsByAgent();
		},
		snapTolerance: 8
	}); 
	
	$('#preview_ehr').css({
		top: 150,
		left: 250
		});
		
	$('#preview_wrapper').show();
	updateAgentByFields();
	$('#preview_wrapper').hide();
	
	addCoreners();
	
	
	
}

function showCorners(){
	$('.corner').hide();
	
	$('#preview_ehr .' + $(divFields).find('select[name*=position_app_corner]').val()).show();
	$('#preview_agent .' + $(divFields).find('select[name*=position_agent_corner]').val()).show();
	
	
}


function addCoreners(){
	$(divFields).find('select[name*=position_app_corner] option').each(function(){
		$('.draggable').append('<div class="corner ' + $(this).val() + '"/>');
	});
	box_shadow_value = '{h}4px {v}4px 4px blue';
	$('.LeftTop').css('box-shadow', box_shadow_value.replace('{h}', '-').replace('{v}', '-'));
	$('.RightTop').css('box-shadow', box_shadow_value.replace('{h}', '').replace('{v}', '-'));
	$('.LeftBottom').css('box-shadow', box_shadow_value.replace('{h}', '-').replace('{v}', ''));
	$('.RightBottom').css('box-shadow', box_shadow_value.replace('{h}', '').replace('{v}', ''));
	
	showCorners();
	$('#preview_close').zIndex(99);
}

function startPreview(){
	$('#preview_wrapper').fadeIn();
	copyValus(divOrgFields, divFields);
	updateAgentByFields();
}

function copyToPage(){
	copyValus(divFields, divOrgFields);
	divOrgFields.find('select, input[type="text"]').addClass("dbmotion-changed");
	changesMade = true;
}

function endPreview(save){
	if (save == true) copyToPage();
	$('#preview_wrapper').fadeOut();
}

function isPreviewActive(){
	return $('#preview_wrapper').css('display') == 'inline';
}

function togglePreview(save){
	isPreviewActive() ? endPreview(save) : startPreview();
}

function updateOffset() {
    if ($('#preview_agent').position() != null && $('#preview_ehr').position() != null)
    {
        offsetx = parseInt($('#preview_agent').position().left - $('#preview_ehr').position().left);
        offsety = parseInt($('#preview_agent').position().top - $('#preview_ehr').position().top);
    }
}

function setAgentPosition(x, y){
	$('#preview_agent').animate({
		top: y,
		left: x,
	}).css({
		top: y,
		left: x,
	});
	updateOffset();
}

function updateFieldsByAgent(){
	if (updating) return;
	updating = true;
	
	appCorner = $(divFields).find('select[name*=position_app_corner]').val();
	agentCorner = $(divFields).find('select[name*=position_agent_corner]').val();
	
	updateOffset();
	x = offsetx;
	y = offsety;
	
	if (appCorner.indexOf('Right') > -1){
		x -= $('#preview_ehr').outerWidth();
	}
	if (appCorner.indexOf('Bottom') > -1){
		y -= $('#preview_ehr').outerHeight();
	}
	if (agentCorner.indexOf('Right') > -1){
		x += $('#preview_agent').outerWidth();
	}
	if (agentCorner.indexOf('Bottom') > -1){
		y += $('#preview_agent').outerHeight();
	}
	
	$(divFields).find('input[name*=position_offset_x]').val(x);
	$(divFields).find('input[name*=position_offset_y]').val(y);
	
	updating = false;
}

function updateAgentByFields(){
	if (updating) return;
	updating = true;
	
	appCorner = $(divFields).find('select[name*=position_app_corner]').val();
	agentCorner = $(divFields).find('select[name*=position_agent_corner]').val();
	
	if (appCorner != null && agentCorner != null && $('#preview_ehr').position() != null) {
	    x = parseInt($(divFields).find('input[name*=position_offset_x]').val()) + $('#preview_ehr').position().left;
	    y = parseInt($(divFields).find('input[name*=position_offset_y]').val()) + $('#preview_ehr').position().top;

	    if (appCorner.indexOf('Right') > -1) {
	        x += $('#preview_ehr').outerWidth();
	    }
	    if (appCorner.indexOf('Bottom') > -1) {
	        y += $('#preview_ehr').outerHeight();
	    }
	    if (agentCorner.indexOf('Right') > -1) {
	        x -= $('#preview_agent').outerWidth();
	    }
	    if (agentCorner.indexOf('Bottom') > -1) {
	        y -= $('#preview_agent').outerHeight();
	    }

	    setAgentPosition(x, y);
	}
	
	updating = false;
}

function copyValus(from_element, to_element){
	to_element.find("input, select").each(function(){
		$(this).val(from_element.find("#" + $(this).attr("id")).val());
	});
}
