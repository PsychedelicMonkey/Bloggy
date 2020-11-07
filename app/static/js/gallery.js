function viewPhoto(photos) {
    photos.forEach(photo => {
        photo.addEventListener('mouseover', function() {
            photo.style.cursor = 'pointer';
            photo.childNodes[1].style.opacity = 0.8;
        });

        photo.addEventListener('mouseout', function() {
            photo.childNodes[1].style.opacity = 1;
        });

        photo.childNodes[1].addEventListener('click', function() {
            console.log(photo.childNodes[1]);
        });
    });
}

function photoActions(photos) {
    photos.forEach(photo => {
        photo.addEventListener('mouseover', function () {
            if (photo.childNodes[3] != null) {
                photo.childNodes[3].style.display = 'block';
            }
        });

        photo.addEventListener('mouseout', function () {
            if (photo.childNodes[3] != null) {
                photo.childNodes[3].style.display = 'none';
            }
        });
    });
}
