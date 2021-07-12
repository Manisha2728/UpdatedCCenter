
$(function () {
	$('#id_patientsearchdisplayoptions_set-0-display_user_attestation').click(function(){
		grayedOut($('#id_patientsearchdisplayoptions_set-0-attestation_text'), ($(this).prop('checked')==false));
	});
	
});

$(function(){
	$('#id_patientsearchdisplayoptions_set-0-attestation_text').show(function(){
		grayedOut($(this), ($('#id_patientsearchdisplayoptions_set-0-display_user_attestation').prop('checked')==false))
	});
});

$(document).ready(function () {
	$("#searchresultgrid_set-group tr").each(function () {
		var currentId = $(this).attr('id');

        // Three rows of Patient Name, DOD (Age) and Address fields are non removeable 
        if (currentId == "searchresultgrid_set-0"){			
			var dropdown = $(this).find('td').eq(2);
			var dropdownbox = dropdown.find('select');
			dropdownbox.attr("disabled", true);
			
            var deletelable = $(this).find('td').eq(4);
            var box = deletelable.find('input:checkbox');
            box.attr("disabled", true);
		}
		if (currentId == "searchresultgrid_set-1"){
			var dropdown = $(this).find('td').eq(2);
			var dropdownbox = dropdown.find('select');
			dropdownbox.attr("disabled", true);
			
            var deletelable = $(this).find('td').eq(4);
            var box = deletelable.find('input:checkbox');
            box.attr("disabled", true);
		}
		if (currentId == "searchresultgrid_set-2"){
			var dropdown = $(this).find('td').eq(2);
			var dropdownbox = dropdown.find('select');
			dropdownbox.attr("disabled", true);
			
            var deletelable = $(this).find('td').eq(4);
            var box = deletelable.find('input:checkbox');
            box.attr("disabled", true);
		}
		if (currentId == "searchresultgrid_set-3") {
			var dropdown = $(this).find('td').eq(2);
			var dropdownbox = dropdown.find('select');
			dropdownbox.attr("disabled", true);
			
            var deletelable = $(this).find('td').eq(4);
            var box = deletelable.find('input:checkbox');
            box.attr("disabled", true);
        }
	});
});

$(document).ready(function () {
	$("#id_searchresultgrid_set-0-label").after("<span style='color:#808080; font-family:sans-serif; font-style:italic; font-size:09pt;'>&nbsp; <b>Default: Patient Name</b> </span>")
	$("#id_searchresultgrid_set-1-label").after("<span style='color:#808080; font-family:sans-serif; font-style:italic; font-size:09pt;'>&nbsp; <b>Default: DOB (Age)</b></span>")
	$("#id_searchresultgrid_set-2-label").after("<span style='color:#808080; font-family:sans-serif; font-style:italic; font-size:09pt;'>&nbsp; <b>Default: Address</b> </span>")
	$("#id_searchresultgrid_set-3-label").after("<span style='color:#808080; font-family:sans-serif; font-style:italic; font-size:09pt;'>&nbsp; <b>Default: System</b> </span>")
});

$(document).ready(function () {
  var referrer = document.URL;
  if(referrer.indexOf("popup=1") === -1){
    $("#ehragentmeasurementproperties_set-group table th:nth-child(3)").hide()
    $("#ehragentmeasurementproperties_set-group table td:nth-child(4)").hide()
  }
});