export let currentFileToDelete = null;
export let currentDeleteButton = null;

export function openImagePopup(imageUrl) {
    const popupImg = document.getElementById('popupImage');
    popupImg.src = imageUrl;
    document.getElementById('imagePopup').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

export function showDeletePopup(filePath, button) {
    currentFileToDelete = filePath;
    currentDeleteButton = button;
    document.getElementById('deletePopup').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

export function closePopup(popupId, event) {
    if (event) event.stopPropagation();
    document.getElementById(popupId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

export function showError(message) {
    alert(message);
}

export function initPopupHandlers() {
    document.getElementById('imagePopup').addEventListener('click', function(e) {
        if (e.target === this) closePopup('imagePopup');
    });
    
    document.getElementById('deletePopup').addEventListener('click', function(e) {
        if (e.target === this) closePopup('deletePopup');
    });
}