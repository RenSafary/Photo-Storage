function sendMessage(event) {
    event.preventDefault();

    const ws = new WebSocket("ws://127.0.0.1:8000/sign-in/ws");
    const form = event.target;
    const statusElement = document.getElementById("auth-status");
    
    ws.onopen = function() {
        form.querySelector('button').textContent = "Try Again";
        form.onsubmit = function(e) {
            e.preventDefault();
            const username = document.getElementsByName("username")[0].value;
            const password = document.getElementsByName("password")[0].value;
            ws.send(JSON.stringify({username, password}));
        };
        
        form.dispatchEvent(new Event('submit'));
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        if (response.status === "success") {
            document.cookie = `access_token=${response.token}; path=/; secure`;
            window.location.href = "/gallery/";
        } else {
            statusElement.textContent = response.detail;
            statusElement.style.color = "red";
        }
    };

    ws.onerror = function(error) {
        statusElement.textContent = "Connection error";
        statusElement.style.color = "red";
    };

    ws.onclose = function() {
        statusElement.textContent = "Connection closed";
    };
}