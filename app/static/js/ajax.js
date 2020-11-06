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