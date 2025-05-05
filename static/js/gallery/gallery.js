let ws = null;

const form = document.getElementById("new_folder_form");
const button = document.getElementById("new_folder_button");

button.addEventListener('click', function() {
    form.style.visibility = form.style.visibility === 'visible' ? 'hidden' : 'visible';
});

function sendMessage(event) {
    event.preventDefault();
    
    ws = new WebSocket("ws://127.0.0.1:8000/new-folder/ws");
    
    const folder_name = document.getElementsByName("new_folder")[0].value;
    const token = document.cookie;
    
    ws.onopen = function() {
        ws.send(JSON.stringify({
            new_folder: folder_name,
            access_token: token
        }));
    };
    
    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        if (response.status === "success") {
            document.getElementsByName("new_folder")[0].value = "";
            ws.close();
            window.location.reload(); 
        } else {
            alert(response.details);
            ws.close();
        }
    };
    
    ws.onerror = function(error) {
        alert("Connection error");
        if (ws) ws.close();
    };
}