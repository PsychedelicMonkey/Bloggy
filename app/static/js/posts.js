function updatePostLikes(button, action, target) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let post = JSON.parse(this.responseText);
            console.log(this.responseText);
            changeButton(button, action, post['id'], post['likes']);
        }
    }
    http.open('POST', target, true);
    http.send();
}

function changeButton(button, action, id, count) {
    if (action == "like") {
        button.classList.remove('btn-success');
        button.classList.add('btn-danger');
        button.innerHTML = 'Unlike (' + count + ')';
        button.dataset.action = 'unlike';
        button.dataset.target = '/unlike/' + id;
    }
    else if (action == "unlike") {
        button.classList.remove('btn-danger');
        button.classList.add('btn-success');
        button.innerHTML = 'Like (' + count + ')';
        button.dataset.action = 'like';
        button.dataset.target = '/like/' + id;
    }
}