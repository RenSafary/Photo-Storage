const ws = new WebSocket("ws://127.0.0.1:8000/sign-in/ws");

ws.onmessage = function(event) {
    const response = JSON.parse(event.data);
    
    if (response.status === "success") {
        window.location.href = "/";
    } else {
        alert(response.detail);
    }
};

function sendMessage(event) {
    event.preventDefault();
    
    const username = document.getElementsByName("username")[0].value;
    const password = document.getElementsByName("password")[0].value;
    
    const data = {
        username: username,
        password: password
    };
    
    ws.send(JSON.stringify(data));
    
    document.getElementsByName("username")[0].value = '';
    document.getElementsByName("password")[0].value = '';
}