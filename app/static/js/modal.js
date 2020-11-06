$('#formModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes
    
    var content = button.data('formcontent');
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-content').empty()
    loadContent(modal, content);
    //modal.find('.modal-title').text('New message to ' + recipient)
    //modal.find('.modal-body input').val(recipient)
});

function loadContent(modal, content) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            modal.find('.modal-content').html(this.responseText);
        }
    };
    http.open('GET', content, true);
    http.send()
}