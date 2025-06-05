$(document).ready(function() {
    $('.sendTG').click(function(event) {
        event.preventDefault(); 
        sendData('telegram', $(this).closest('form'));
    });

    $('.sendWhatsApp').click(function(event) {
        event.preventDefault(); 
        sendData('whatsapp', $(this).closest('form')); 
    });

    function sendData(platform, form) {
        const user = form.find('input[name="user"]').val(); 
        const url = form.find('input[name="url"]').val(); 

        $.ajax({
            url: 'http://127.0.0.1:8080/gallery/api/share_file/', 
            type: 'POST',
            data: {
                user: user,
                url: url,
                platform: platform
            },
            success: function(response) {
                console.log('Server response:', response);
                window.open(response.shareURL, '_blank').focus();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
});