function submitLike(form) {
    $(form).submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var action = form.attr('action');
        var submitBtn = $('input[type=submit]', this);
        
        $.ajax({
            type: 'POST',
            url: action,
            data: form.serialize(),
            success: function(response) {
                var arr = JSON.parse(JSON.stringify(response));
                console.log(arr);
                form.attr('action', arr['action']);
                submitBtn.val(arr['btnLabel']);
                submitBtn.removeClass('btn-success');
                submitBtn.removeClass('btn-danger');
                submitBtn.addClass(arr['btnClass']);
            },
            error: function(response) {
                alert('An error occured submitting your like');
            }
        });
    });
}