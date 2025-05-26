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

    const fileInput = document.getElementById('fileInput');
        const previewContainer = document.getElementById('previewContainer');
        const filesToUpload = [];
        
        fileInput.addEventListener('change', function(e) {
            previewContainer.innerHTML = '';
            filesToUpload.length = 0;
            
            Array.from(e.target.files).forEach(file => {
                filesToUpload.push(file);
                createPreview(file);
            });
        });
        
        function createPreview(file) {
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
            fileName.textContent = file.name.length > 15 ? file.name.substring(0, 12) + '...' : file.name;
            
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                previewItem.appendChild(img);
            } else if (file.type.startsWith('video/')) {
                const video = document.createElement('video');
                video.src = URL.createObjectURL(file);
                previewItem.appendChild(video);
            }
            
            previewItem.appendChild(removeBtn);
            previewItem.appendChild(fileName);
            previewContainer.appendChild(previewItem);
        }
        
        function removeFile(fileToRemove, previewElement) {
            const index = filesToUpload.findIndex(file => file === fileToRemove);
            if (index !== -1) {
                filesToUpload.splice(index, 1);
                URL.revokeObjectURL(previewElement.querySelector('img, video').src);
                previewElement.remove();
                updateFileInput();
            }
        }
        
        function updateFileInput() {
            const dataTransfer = new DataTransfer();
            filesToUpload.forEach(file => dataTransfer.items.add(file));
            fileInput.files = dataTransfer.files;
            
            if (filesToUpload.length === 0) {
                previewContainer.style.display = 'none';
            } else {
                previewContainer.style.display = 'flex';
            }
        }