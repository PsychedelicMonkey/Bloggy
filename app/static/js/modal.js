$(document).ready(function() {
    $('#formModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var formAction = button.data('formaction') // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        modal.find('form').attr('action', formAction)
        modal.find('.modal-title').text('New message to ' + formAction)
        modal.find('.modal-body input').val(formAction)
    })
});