export function initFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const filesToUpload = [];
    
    fileInput.addEventListener('change', function(e) {
        previewContainer.innerHTML = '';
        filesToUpload.length = 0;
        
        Array.from(e.target.files).forEach(file => {
            filesToUpload.push(file);
            createPreview(file, previewContainer, filesToUpload);
        });
    });
    
    function createPreview(file, container, filesArray) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn';
        removeBtn.innerHTML = '×';
        removeBtn.onclick = (e) => {
            e.stopPropagation();
            removeFile(file, previewItem, filesArray, fileInput, container);
        };
        
        const fileName = document.createElement('div');
        fileName.className = 'file-name';
        fileName.textContent = file.name.length > 15 ? 
            file.name.substring(0, 12) + '...' : file.name;
        
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
        container.appendChild(previewItem);
    }
    
    function removeFile(fileToRemove, previewElement, filesArray, input, container) {
        const index = filesArray.findIndex(file => file === fileToRemove);
        if (index !== -1) {
            filesArray.splice(index, 1);
            URL.revokeObjectURL(previewElement.querySelector('img, video').src);
            previewElement.remove();
            updateFileInput(filesArray, input, container);
        }
    }
    
    function updateFileInput(filesArray, input, container) {
        const dataTransfer = new DataTransfer();
        filesArray.forEach(file => dataTransfer.items.add(file));
        input.files = dataTransfer.files;
        container.style.display = filesArray.length === 0 ? 'none' : 'flex';
    }
}