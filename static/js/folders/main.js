import { initPopupHandlers, openImagePopup, showDeletePopup } from './popup.js';
import { initDeleteHandler } from './delete.js';

document.addEventListener('DOMContentLoaded', () => {
    initPopupHandlers();
    initDeleteHandler();
    
    window.openImagePopup = openImagePopup;
    window.showDeletePopup = showDeletePopup;
});