function toggleTagForm() {
    const tagForm = document.getElementById('new_tag_form');
    tagForm.style.display = tagForm.style.display === 'none' || tagForm.style.display === '' ? 'flex' : 'none';
}

function sendMessageTag(event) {
    event.preventDefault();

    const websocket = new WebSocket("ws://127.0.0.1:8000/new-tag/ws");
    const name = document.getElementsByName("new_tag_name")[0].value;
    const token = document.cookie;

    websocket.onopen = function() {
        websocket.send(JSON.stringify({
            name: name,
            access_token: token
        }));
    };

    websocket.onmessage = function(event) {
        const response = JSON.parse(event.data);
        if (response.status === "success") {
            document.getElementsByName("new_tag_name")[0].value = "";
            websocket.close();
            window.location.reload();
        } else {
            console.alert(response.detail);
            websocket.close();
        }
    };

    websocket.onerror = function(error) {
        alert("Connection error");
        websocket.close();
    };
}