function update_sum(table, field, checkBoxField) {
    var sumRow = $('#'+table+'_set-SUM');

    var count = $(sumRow).parent().children('.has_original').length;

    var totalWidth = 0.0;
    for (var i = 0; i < count; i++)
    {
        var input = $('#id_' + table + '_set-' + i + '-' + field);

        var enabled = $('#id_' + table + '_set-' + i + '-' + checkBoxField);
        if ($(enabled).is(":checked")) {
            totalWidth += parseFloat($(input).val())            
        }
    }

    $(sumRow).children('.field-' + field).empty();

    $(sumRow).children('.field-' + field).append('<p>' + totalWidth.toFixed(2) + '</p>');
}

function add_sum_row(table, checkBoxField, nameField, sumFields) {
    var first = $('#'+table+'_set-0');

    if ($(first).length == 0)
    {
        return;
    }

    var siblings = $(first).parent().children('.has_original');
    var last = $(siblings).last();
    var copy = $(last).clone(true);

    $(copy).children().each(function () {
        if (!$(this).hasClass('original')) {
            $(this).empty();
        }
    });

    $(copy).removeClass('has_original');

    if ($(copy).hasClass('row1')) {
        $(copy).removeClass('row1');
        $(copy).addClass('row2');
    } else {
        $(copy).removeClass('row2');
        $(copy).addClass('row1');
    }

    $(copy).attr('id', table + '_set-SUM');

    $(copy).children('.field-' + nameField).append('<p>SUM</p>');

    $(last).removeClass('last-related');
    $(last).after(copy);

    $(sumFields).each(function(){
        update_sum(table, this, checkBoxField);
    });

    var count = $(copy).parent().children('.has_original').length;

    var totalWidth = 0;
    for (var i = 0; i < count; i++)
    {
        $(sumFields).each(function(){
            var field = this;

            var input = $('#id_' + table + '_set-' + i + '-' + field);
            input.bind('change paste keyup', function() {update_sum(table, field, checkBoxField)});

            var enabled = $('#id_' + table + '_set-' + i + '-' + checkBoxField);
            enabled.bind('change', function() {update_sum(table, field, checkBoxField)});
        });
    }
}
