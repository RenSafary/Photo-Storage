function sendMessage(event) {
    event.preventDefault();

    const ws = new WebSocket("ws://127.0.0.1:8000/sign-up/ws");

    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const repeat_pass = document.getElementById("repeat_pass").value;

    ws.onopen = function() {
        ws.send(JSON.stringify({
            email: email,
            username: username,
            password: password,
            repeat_pass: repeat_pass
        }));
    };

    ws.onmessage = function(event) {
        const response = JSON.parse(event.data);
        
        if (response.status === "success") {
            document.cookie = `access_token=${response.token}; path="/"; secure`;
            window.location.href = "/Photo-Storage";
        } else {
            alert(response.detail);
        }
    };

    ws.onerror = function(error) {
        alert("Connection error. Please try again.");
        console.error("WebSocket error:", error);
    };
}