$(function(){
	var viaset = document.getElementById('via_set-0');
	viaset.style.display="none";
	var type = $('select[name=via_set-0-empi_type]').val();
	if (type != "Initiate")
	{
		show_hide_column(9, false);
		show_hide_column(10, false);
		show_hide_column(11, false);
		document.getElementById('dbmotionsystem_set-group').style.display="none";
		document.getElementById('system_type_help').style.display="none";
	}
	if (type != "PDQ")
	{
		show_hide_column(12, false);
		show_hide_column(13, false);
	}
	
	
	// if($('input[id=id_ccdawithoutadtsystems_set-0-load_ccda_without_adt_sources]').is(":checked"))
		// $('#dbmotionsystem_set-group table :input').slice(1).removeAttr('disabled');
	// else
		// $('#dbmotionsystem_set-group table :input').slice(1).attr('disabled', 'true');
// 	
	// $('input[id=id_ccdawithoutadtsystems_set-0-load_ccda_without_adt_sources]').click(function(){
		// if ($(this).is(":checked"))
		// {
			// $('#dbmotionsystem_set-group table :input').slice(1).removeAttr('disabled');
		// }
		// else
		// {
			// $('#dbmotionsystem_set-group table :input').slice(1).attr('disabled', 'true');
		// }
	// });
// 	

    $("#ccdawithoutadtsystems_set-group").addClass("ui-helper-hidden");
    $("#dbmotionsystem_set-group").addClass("ui-helper-hidden");

	var firstRow = $('#authoritysystems_set-0');
    var count = $(firstRow).parent().children('.has_original').length;
	// Disable Is Default System field if Display For Search is not checked
	for (var i = 0; i <= count; i++)
    {
    	// On loading page
        var displayForSearch = $('#id_authoritysystems_set-' + i + '-display_for_search');
        var isDefault = $('#' + displayForSearch.attr('id').replace("-display_for_search","-is_default"));
        if(displayForSearch.prop("checked") == true)
        	isDefault.attr("disabled", false);
        else
        {
        	isDefault.attr("disabled", true);
        	isDefault.prop("checked", false);
        }
        
        // On click Display For Search checkbox
        displayForSearch.click(function(){
        	var isDefaultCheckbox = '#' + $(this).attr('id').replace("-display_for_search","-is_default");
	        if($(this).prop("checked") == true)
	        	$(isDefaultCheckbox).attr("disabled", false);
	        else
	        {
	        	$(isDefaultCheckbox).attr("disabled", true);
	        	$(isDefaultCheckbox).prop("checked", false);
	        }
        });
        
        // Allow only one Is Default System checkbox to be checked
        isDefault.click(function(){
	        if($(this).prop("checked") == true)
	        {
	        	for (var j = 0; j <= count; j++)
			    {
			    	var id = 'id_authoritysystems_set-' + j + '-is_default';
			    	if (id != $(this).attr('id'))
			    	{
			    		$('#id_authoritysystems_set-' + j + '-is_default').prop("checked", false);
			    	}
			    }
	        }
        });
         var select = $('#id_authoritysystems_set-' + i + '-system_type');
        select.click(function(){
        	var segment = '#' + $(this).attr('id').replace("-system_type","-segment_name");
        	var attribute = '#' + $(this).attr('id').replace("-system_type","-attribute_code");
	        if($(this).val().indexOf("MPIID") > -1 || $(this).val() == "Real" )
	        {
	        	$(segment).attr("disabled", true);
	        	$(segment).val("");
	        	$(attribute).attr("disabled", true);
	        	$(attribute).val("");
	        	
	        }
	        else
	        {
	        	$(segment).attr("disabled", false);
	        	$(attribute).attr("disabled", false);	
	        }
        }).click();
    }
});

 function show_hide_column(col_no, do_show) {

    var stl;
    if (do_show) stl = 'block';
    else         stl = 'none';

    var tbl  = document.getElementsByTagName('table')[0];
    var rows = tbl.rows;

    for (var row=0; row<rows.length;row++) {
      var cels = rows[row].getElementsByTagName('td');
      if( cels.length > col_no)
      	cels[col_no].style.display=stl;
      var heds = rows[row].getElementsByTagName('th');
      if( heds.length > col_no)
      	heds[col_no-1].style.display=stl;
    }
  }
  
function show_hide_help_extension(btn)
{
	if(btn.value == 'Show')
	{
		btn.value = 'Hide';
		document.getElementById('help_extension').style.display = 'block';
	}
	else
	{
		btn.value = 'Show';
		document.getElementById('help_extension').style.display = 'none';    	
	}
}
