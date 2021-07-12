/// This file is referenced by dbmModelAdmin, which is the base of all configuration pages in dbmconfigapp
/// file: admin\dbm_ModelAdmin.py

$(function(){
	
	// NOTE: The following commented hide() commands are covered in the templates.
	//		 Leave it as a reference if need to handle the inline headers when using the original templates.
	// hide default admin headers for inline models
	// we use section headers
	//$('.inline-group > h2').hide();		// removed in 'admin/edit_inline/stacked_no_header.html'
    //$('.inline-group > .inline-related > h3').hide();		// commented in 'admin/edit_inline/stacked.html'
    
    // hide sections that contain 'HiddenSection' in the title
    // used for manipulated fields that need to be in the form but should be hidden from the user
    $("h2:contains('HiddenSection')").parent().hide();
    
	
	// set ehr agent\categories\external documents- opened by default checkbox to disable
	$('#id_ehragentcategoriesproperties_set-13-category_opened').attr("disabled", true);
	
	// set ehr agent categories "Categories Displayed in Encounter Details Page" checkbox to disable for unused categories
	$('#id_ehragentcategoriesproperties_set-0-show_in_encounter_details').attr("disabled", true);	//Encounters
	$('#id_ehragentcategoriesproperties_set-1-show_in_encounter_details').attr("disabled", true);	//Problems
	$('#id_ehragentcategoriesproperties_set-2-show_in_encounter_details').attr("disabled", true);	//Past Medical History
	$('#id_ehragentcategoriesproperties_set-4-show_in_encounter_details').attr("disabled", true);	//Allergies
	$('#id_ehragentcategoriesproperties_set-6-show_in_encounter_details').attr("disabled", true);	//Measurements
	$('#id_ehragentcategoriesproperties_set-9-show_in_encounter_details').attr("disabled", true);	//Immunizations
	$('#id_ehragentcategoriesproperties_set-13-show_in_encounter_details').attr("disabled", true);	//External Documents
	$('#id_ehragentcategoriesproperties_set-2-0-show_in_encounter_details').attr("disabled", true);	//Population Memberships
	$('#id_ehragentcategoriesproperties_set-2-1-show_in_encounter_details').attr("disabled", true);	//Alerts
	$('#id_ehragentcategoriesproperties_set-2-2-show_in_encounter_details').attr("disabled", true);	//Tasks

    $('ul[name^="horizontalsortable_"]').sortable({
    	axis		 : "x",
        revert       : true,
        stop         : function(event,ui){
            var input = $(event.target).next("input");
            var value = $(event.target).sortable("toArray").join('|');
            $(input).val(value);
        }
     });
    
     $('ul[name^="horizontalsortable_"]').disableSelection();	
     

});



