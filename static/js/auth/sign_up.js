function sendMessage(event) {
    event.preventDefault();

    const ws = new WebSocket("ws://127.0.0.1:8000/sign-up/ws");

    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    ws.onopen = function() {
        ws.send(JSON.stringify({
            email: email,
            username: username,
            password: password
        }));
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        
        if (response.status === "success") {
            window.location.href = "/";
        } else {
            alert(response.detail);
        }
        ws.close();
    };

    ws.onerror = function(error) {
        alert("Connection error. Please try again.");
        console.error("WebSocket error:", error);
    };

    document.getElementById("email").value = "";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}