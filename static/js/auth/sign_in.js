function sendMessage(event) {
    event.preventDefault();

    const ws = new WebSocket("ws://127.0.0.1:8000/sign-in/ws");
    
    const username = document.getElementsByName("username")[0].value;
    const password = document.getElementsByName("password")[0].value;
    
    const data = {
        username: username,
        password: password
    };
    
    ws.onopen = function() {
        ws.send(JSON.stringify(data));
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        if (response.status === "success") {
            document.cookie = `access_token=${response.token}; path=/; secure`;
            window.location.href = "/gallery/";
            ws.close();
        } else {
            alert(response.detail);
        }
    };
}