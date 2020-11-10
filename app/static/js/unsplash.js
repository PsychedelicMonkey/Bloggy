function loadUnsplashForm() {
    $('#unsplash-form').submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');

        var submit = $('input[type=submit]', this);
        var loading = form.find('.btn-loading');

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            beforeSend: function() {
                submit.prop('disabled', true);
                submit.hide();
                loading.show();
            },
            complete: function() {
                loading.hide();
                submit.prop('disabled', false);
                submit.show();
            },
            success: function(data) {
                $('#unsplashModal').find('.modal-body').empty()
                $('#unsplashModal').find('.modal-body').html(data)
                $('#unsplashModal').modal('show');
            }
        });
    });
}

function submit(form, refreshUrl) {
    $(form).submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');

        var submit = $('input[type=submit]', this);
        var loading = form.find('.btn-loading');
        
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            beforeSend: function() {
                submit.prop('disabled', true);
                submit.hide();
                loading.show();
            },
            complete: function() {
                loading.hide();
                submit.show();

                // Refresh the page
                $('#gallery').empty();
                $('#gallery').load(refreshUrl);
            },
            success: function(data) {
                alert(data); // TODO: change to toast
            }
        });
    });
}