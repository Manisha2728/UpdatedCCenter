/// This file is referenced by dbmModelAdmin, which is the base of all configuration pages in dbmconfigapp
/// file: admin\dbm_ModelAdmin.py

$(function(){
	$('#id_ehragentclinicaldomainsproperties_set-0-attention_searching_option').click(function(){
		if ($(this).val() == "4" || $(this).val() == "6")
		{
			$('#id_ehragentclinicaldomainsproperties_set-0-attention_searching_time').prop("value", "0");
			$('#id_ehragentclinicaldomainsproperties_set-0-attention_searching_time').prop("disabled", true);
		}
		else
		{
			$('#id_ehragentclinicaldomainsproperties_set-0-attention_searching_time').prop("disabled", false);
		}
	}).click();
	
});

$(function(){
	$("select[id$='default_searching_option']").click(function(){
		var dropId = $(this).attr("id");
		var textId = dropId.replace("_option", "_time");
		if ($(this).val() == "4")
		{
			$("#" + textId).prop("value", "0");
			$("#" + textId).prop("disabled", true);
		}
		else
		{
			$("#" + textId).prop("disabled", false);
		}
	}).click();
	
});
