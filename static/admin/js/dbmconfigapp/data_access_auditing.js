function apply(obj) {
    $("#msg").html('Please wait...');
    $(obj).prop('disabled', true);

    $.get('/apply_data_access_auditing/', '',
        function (data) {
            $("#msg").html(data);
        })
        .fail(function (o, status, msg) {
            $("#msg").html('Unexpected error occurred');
        })
        .always(function () {
            $(obj).prop('disabled', false);
        });

}