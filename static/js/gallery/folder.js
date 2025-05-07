let currentFileToDelete = null;
let currentDeleteButton = null;

// Image popup functions
function openImagePopup(imageUrl) {
    const popupImg = document.getElementById('popupImage');
    popupImg.src = imageUrl;
    document.getElementById('imagePopup').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Delete confirmation functions
function showDeletePopup(filePath, button) {
    currentFileToDelete = filePath;
    currentDeleteButton = button;
    document.getElementById('deletePopup').style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Clear previous event listeners to avoid duplicates
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    confirmBtn.onclick = confirmDelete;
}

async function confirmDelete() {
    if (!currentFileToDelete) return;
    
    try {
        const response = await fetch('/delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Добавляем CSRF-токен
            },
            body: JSON.stringify({ file_path: currentFileToDelete })
        });
        
        if (response.ok) {
            const fileItem = currentDeleteButton.closest('.file-item');
            if (fileItem) {
                fileItem.remove();
                
                // Check if any files remain
                if (!document.querySelector('.file-item')) {
                    document.querySelector('.files').innerHTML = 
                        '<p class="empty-message">There are no photos or videos in this folder yet.</p>';
                }
            }
        } else {
            const errorData = await response.json();
            showError(errorData.detail || 'Error deleting file');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred while deleting the file');
    } finally {
        closePopup('deletePopup');
        currentFileToDelete = null;
        currentDeleteButton = null;
    }
}

// Helper function to get cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function closePopup(popupId, event) {
    if (event) event.stopPropagation();
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function showError(message) {
    // Consider using a more user-friendly notification system
    alert(message);
}

// Event listeners for popup backgrounds
document.getElementById('imagePopup')?.addEventListener('click', function(e) {
    if (e.target === this) closePopup('imagePopup');
});

document.getElementById('deletePopup')?.addEventListener('click', function(e) {
    if (e.target === this) closePopup('deletePopup');
});

// File upload and preview functionality
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const filesToUpload = [];

fileInput?.addEventListener('change', function(e) {
    previewContainer.innerHTML = '';
    filesToUpload.length = 0;
    
    Array.from(e.target.files).forEach(file => {
        filesToUpload.push(file);
        createPreview(file);
    });
    
    updateFileInput();
});

function createPreview(file) {
    if (!file) return;
    
    const previewItem = document.createElement('div');
    previewItem.className = 'preview-item';
    
    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '×';
    removeBtn.onclick = (e) => {
        e.stopPropagation();
        removeFile(file, previewItem);
    };
    
    const fileName = document.createElement('div');
    fileName.className = 'file-name';
    fileName.textContent = truncateFileName(file.name, 15);
    
    const mediaElement = file.type.startsWith('image/') 
        ? document.createElement('img')
        : file.type.startsWith('video/') 
            ? document.createElement('video')
            : null;
    
    if (mediaElement) {
        mediaElement.src = URL.createObjectURL(file);
        previewItem.appendChild(mediaElement);
    } else {
        const fileIcon = document.createElement('div');
        fileIcon.className = 'file-icon';
        fileIcon.textContent = getFileIcon(file.name);
        previewItem.appendChild(fileIcon);
    }
    
    previewItem.appendChild(removeBtn);
    previewItem.appendChild(fileName);
    previewContainer.appendChild(previewItem);
}

function truncateFileName(name, maxLength) {
    return name.length > maxLength 
        ? name.substring(0, maxLength - 3) + '...' 
        : name;
}

function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    return ext === 'pdf' ? '📄' : '📁';
}

function removeFile(fileToRemove, previewElement) {
    if (!fileToRemove || !previewElement) return;
    
    const index = filesToUpload.findIndex(file => file === fileToRemove);
    if (index !== -1) {
        const mediaElement = previewElement.querySelector('img, video');
        if (mediaElement) URL.revokeObjectURL(mediaElement.src);
        
        filesToUpload.splice(index, 1);
        previewElement.remove();
        updateFileInput();
    }
}

function updateFileInput() {
    const dataTransfer = new DataTransfer();
    filesToUpload.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
    
    previewContainer.style.display = filesToUpload.length > 0 ? 'flex' : 'none';
}