// Execute the follow / unfollow function when submitted
function followForm(form, button) {
    $(form).submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var action = form.attr('action');

        $.ajax({
            type: 'POST',
            url: action,
            data: form.serialize(),
            success: function(response) {
                var changes = JSON.parse(JSON.stringify(response));
                console.log(changes);
                form.attr('action', changes['route']);
                $(button).val(changes['btnLabel']);
                $('#pills-followers-tab').text(changes['newCount']);
            },
            error: function(response) {
                alert('An unknown error occurred');
            }
        });
    });
}