let currentFileToDelete = null;
    let currentDeleteButton = null;
    
    function openImagePopup(imageUrl) {
        const popupImg = document.getElementById('popupImage');
        popupImg.src = imageUrl;
        document.getElementById('imagePopup').style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    function showDeletePopup(filePath, button) {
        currentFileToDelete = filePath;
        currentDeleteButton = button;
        document.getElementById('deletePopup').style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        document.getElementById('confirmDeleteBtn').onclick = confirmDelete;
    }
    
    async function confirmDelete() {
        if (!currentFileToDelete) return;
        
        try {
            const formData = new FormData();
            formData.append('file_path', currentFileToDelete);
            
            const response = await fetch('/delete/', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                currentDeleteButton.closest('.file-item').remove();
                
                if (!document.querySelector('.file-item')) {
                    document.querySelector('.files').innerHTML = 
                        '<p class="empty-message">There are no photos or videos in this folder yet.</p>';
                }
            } else {
                showError('Error deleting file');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred');
        } finally {
            closePopup('deletePopup');
            currentFileToDelete = null;
            currentDeleteButton = null;
        }
    }
    
    function closePopup(popupId, event) {
        if (event) event.stopPropagation();
        document.getElementById(popupId).style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    function showError(message) {
        alert(message);
    }
    
    document.getElementById('imagePopup').addEventListener('click', function(e) {
        if (e.target === this) closePopup('imagePopup');
    });
    
    document.getElementById('deletePopup').addEventListener('click', function(e) {
        if (e.target === this) closePopup('deletePopup');
    });