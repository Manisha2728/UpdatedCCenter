$(function(){

	
	$('#text_search').val(getUrlParameter('search'));
		

});


function checkSearch(){
	$('#text_search').val($.trim($('#text_search').val()));
	return $('#text_search').val().length > 0;
}
    

	
	