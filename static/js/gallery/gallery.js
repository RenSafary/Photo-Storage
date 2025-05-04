const ws = new WebSocket("ws://127.0.0.1:8000/new-folder/ws");

const token = document.cookie;

ws.onmessage = function(event) {
    const response = JSON.parse(event.data);
    if (response.status === "success") {
        document.getElementsByName("new_folder")[0].value = "";
        //ws.close();
    } else {
        alert(response.details);
    }
};

const form = document.getElementById("new_folder_form"); 
const button = document.getElementById("new_folder_button"); 

button.addEventListener('click', function() {
    form.style.visibility = "visible";
});

form.addEventListener('submit', function(event) {
    event.preventDefault();
    const folder_name = document.getElementsByName("new_folder")[0].value;
    
    const data = {
        new_folder: folder_name,
        access_token: token
    }
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
    } else {
        alert("WebSocket соединение не установлено");
    }
});