function ajaxDumpIntoElement(url, element) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $(element).html(this.responseText);
        }
    }
    http.open('GET', url, true);
    http.send();
}

function loadGallery(url, element) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $(element).html(this.responseText);

            let photos = document.querySelectorAll('.photo-wrapper');
            viewPhoto(photos);
            photoActions(photos);
        }
    }
    http.open('GET', url, true);
    http.send();
}