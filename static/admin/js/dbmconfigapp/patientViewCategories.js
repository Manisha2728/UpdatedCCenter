$(document).ready(function () {
    categoriesproperties_fields_disabled('pvcategoriesproperties', 'DELETE');
    AddWatchToEllement("#id_prefetchsettingsmodel_set-0-enable_prefetch");
    AddWatchToEllement("#id_carequalityintegrationsettingsmodel_set-0-enable_carequality_integration");
    

    if (!$('#id_carequalityintegrationsettingsmodel_set-0-enable_carequality_integration').prop('checked'))
    {
            $('#carequalityintegrationsettingsmodel_set-group :input').prop("disabled", true);
            $('#id_carequalityintegrationsettingsmodel_set-0-enable_carequality_integration').prop("disabled", false);
            $('#participantbaselinelistmodel_set-group :input').prop("disabled", true);
            $('#participantlistbasedpaamodel_set-group :input').prop("disabled", true);
            $('#prefetchsettingsmodel_set-group :input').prop("disabled", true);
            $("label[for*='api_url']").removeClass("required");
			$("label[for*='api_subscription_key']").removeClass("required"); 
            RemoveAllReqierements();
    }
    else if(!$('#id_prefetchsettingsmodel_set-0-enable_prefetch').prop('checked'))
    {
        $('#id_prefetchsettingsmodel_set-0-api_url').prop("disabled", true);
        $('#id_prefetchsettingsmodel_set-0-api_subscription_key').prop("disabled", true);
        $("label[for*='api_url']").removeClass("required");
		$("label[for*='api_subscription_key']").removeClass("required"); 
        AddReqierements();
    }
    else{
        $("label[for*='api_url']").removeClass("required");
		$("label[for*='api_subscription_key']").removeClass("required"); 
        AddReqierements();
    }

    $('#id_carequalityintegrationsettingsmodel_set-0-enable_carequality_integration').change(function(){
        
		if ($(this).prop('checked'))
		{
	
            $('#id_prefetchsettingsmodel_set-0-enable_prefetch').prop("disabled", false);
            $('#carequalityintegrationsettingsmodel_set-group :input').prop("disabled", false);
            $('#participantbaselinelistmodel_set-group :input').prop("disabled", false);
            $('#participantlistbasedpaamodel_set-group :input').prop("disabled", false);
            $('#prefetchsettingsmodel_set-group :input').prop("disabled", false);
            AddReqierements();
           
           
		}
		else
		{
			$('#carequalityintegrationsettingsmodel_set-group :input').prop("disabled", true);
            $('#id_carequalityintegrationsettingsmodel_set-0-enable_carequality_integration').prop("disabled", false);
            $('#participantbaselinelistmodel_set-group :input').prop("disabled", true);
            $('#participantlistbasedpaamodel_set-group :input').prop("disabled", true);
            $('#prefetchsettingsmodel_set-group :input').prop("disabled", true);
            RemoveAllReqierements();
           
		}
	});
    
    $('#id_prefetchsettingsmodel_set-0-enable_prefetch').change(function(){
        
        if ($(this).prop('checked') && !$(this).prop('disabled'))
        {   
            $('#id_prefetchsettingsmodel_set-0-api_url').prop("disabled",false);
            $('#id_prefetchsettingsmodel_set-0-api_subscription_key').prop("disabled", false);
            $("label[for*='api_url']").addClass("required");
			$("label[for*='api_subscription_key']").addClass("required");      

        }
        else
        {
            $('#id_prefetchsettingsmodel_set-0-api_url').prop("disabled", true);
            $('#id_prefetchsettingsmodel_set-0-api_subscription_key').prop("disabled", true);
            $("label[for*='api_url']").removeClass("required");
			$("label[for*='api_subscription_key']").removeClass("required");   
        
        }
    });
});

function AddWatchToEllement(id) {

    $(id ).change(function() {
      
      });
}

function RemoveAllReqierements() {

    $("label[for*='home_community_id']").removeClass("required"); 
    $("label[for*='certificate_thumptrint']").removeClass("required"); 
    $("label[for*='patient_discovery_endpoint']").removeClass("required"); 
    $("label[for*='find_documents_endpoint']").removeClass("required"); 
    $("label[for*='retrieve_document_endpoint']").removeClass("required"); 
    /* $("img[title*='Carequality participant name.']").parent().removeClass("required")     
    $("img[title*='Carequality participant OID.']").parent().removeClass("required")     
    $("img[title*='Patient Assigning Authority OID as displayed in CCenter under EMPI- Assigning Authority.']").parent().removeClass("required") */     
        
}

function AddReqierements() {

    $("label[for*='home_community_id']").addClass("required"); 
    $("label[for*='certificate_thumptrint']").addClass("required"); 
    $("label[for*='patient_discovery_endpoint']").addClass("required"); 
    $("label[for*='find_documents_endpoint']").addClass("required"); 
    $("label[for*='retrieve_document_endpoint']").addClass("required"); 

    //Change requieremnts in tables
    /* $("img[title*='Carequality participant name.']").parent().addClass("required")
    $("img[title*='Carequality participant OID.']").parent().addClass("required")
    $("img[title*='Patient Assigning Authority OID as displayed in CCenter under EMPI- Assigning Authority.']").parent().addClass("required") */
}
