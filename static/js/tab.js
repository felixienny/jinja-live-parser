$(document).ready(function () {
    $('#save').click(function () {
        var title = $('#title').val();
        var template = $('#template').val();
        var values = $('#values').val();
        var tabId = $('#tab-id').val();
        console.log(tabId);

        $.post('/save', {
            title: title,
            template: template,
            values: values,
            tab_id: tabId
        }).done(function (response) {
            $('#message').html(response);
            window.location.reload();
        });
    });

    $('#add').click(function () {
        var title = $('#new_title').val();

        $.post('/save', {
            title: title,
            template: 'Fill in the template',
            values: 'dummy: 1',
        }).done(function (response) {
            $('#message').html(response);
            window.location.reload();
        });
    });

    $('.display-tab').click(function () {
        var tabId = $(this).data('tab-id');

        $.post('/get-tab', {
            tab_id: tabId
        }).done(function (response) {
            var tab = JSON.parse(response);
            $('#title').val(tab.title);
            $('#template').val(tab.template);
            $('#values').val(tab.values);
            $('#tab-id').val(tabId);
        });
    });


    $('.delete-tab').click(function () {
        var tabId = $(this).data('tab-id');

        $.post('/del-tab', {
            tab_id: tabId
        }).done(function (response) {
            $('#message').html(response);
            window.location.reload();
        });
    });

});
