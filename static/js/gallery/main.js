import { initPopupHandlers, openImagePopup, showDeletePopup } from './popup.js';
import { initDeleteHandler } from './delete.js';
import { initFileUpload } from './upload.js';

document.addEventListener('DOMContentLoaded', () => {
    initPopupHandlers();
    initDeleteHandler();
    initFileUpload();
    
    window.openImagePopup = openImagePopup;
    window.showDeletePopup = showDeletePopup;
});