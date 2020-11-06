function photoActions(photos) {
    for (let i = 0; i < photos.length; i++) {
        photos.forEach(photo => {
            photo.addEventListener('mouseover', function() {
                photo.childNodes[3].style.display = 'block';
            });
    
            photo.addEventListener('mouseout', function() {
                photo.childNodes[3].style.display = 'none';
            });
        });
    }
}
