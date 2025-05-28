import { closePopup, showError, currentFileToDelete, currentDeleteButton } from './popup.js';

export async function confirmDelete() {
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

export function initDeleteHandler() {
    document.getElementById('confirmDeleteBtn').onclick = confirmDelete;
}