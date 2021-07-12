$(function(){
	var restartdbMotionAlert = '<div><p class="alertnote">After making a change in the configuration of Unmanaged Users, Security service must be restarted for the change to be applied.</p>'
	$('#changelist').before(restartdbMotionAlert);
					
	$('#changelist').css('width', 'auto');
		
});