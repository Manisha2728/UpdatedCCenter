
$(document).ready(function () {
    current_app_key = $('input#id_app_key').val();
    if(current_app_key == 'cva')
    {
        $('input#id_app_name').prop('disabled', true);
        $('input#id_LogoFile').prop('disabled', true);
        $('input#id_launch_url').prop('disabled', true);
        $('input#id_is_user_alias_required').prop('disabled', true);
        $('input#id_is_window_resizable').prop('disabled', true);
        $('input#id_window_default_width_size').prop('disabled', true);
        $('input#id_window_minimal_width_size').prop('disabled', true);
        $('input#id_window_default_height_size').prop('disabled', true);
        $('input#id_window_minimal_height_size').prop('disabled', true);

    }
});