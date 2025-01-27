$(document).ready(function () {
    $('#clear').click(function () {
        $('#template').val('');
        $('#render').val('');
        $('#values').val('');
        $('#render').html('');
    });

    $('#convert').click(function () {
        var input_type = $('input[name="type"]:checked').val();

        $.post('/convert', {
            template: $('#template').val(),
            values: $('#values').val(),
            type: input_type,
        }).done(function (response) {
            $('#render').html(response);
        });
    });
});
