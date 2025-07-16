$(document).ready(function() {
    $('.create-folder-btn').click(function() {
        $('.popup-create-folder').addClass('active');
        $('input[name="folder_name"]').focus();
    });

    $('.popup-create-folder').click(function(e) {
        if ($(e.target).hasClass('popup-create-folder')) {
            $(this).removeClass('active');
        }
    });

    $('#folderForm').submit(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: '/gallery/folders/creation',
            data: $(this).serialize(),
            success: function(response) {
                $('.popup-create-folder').removeClass('active');
                
                window.location.reload();
            },
            error: function(xhr) {
                alert('Error: ' + (xhr.responseJSON?.message || 'Failed to create folder'));
            }
        });
    });

    $(document).keyup(function(e) {
        if (e.key === "Escape") {
            $('.popup-create-folder').removeClass('active');
        }
    });
});