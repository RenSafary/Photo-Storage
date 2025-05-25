function sendMessage(event){
    event.preventDefault();

    const ws = new WebSocket("ws://127.0.0.1:8000/find-tag/ws");

    const tag = document.getElementById("search_tag").value;
    const token = document.cookie;
    
    ws.onopen = function(){
        ws.send(JSON.stringify({
            tag: tag,
            token: token
        }));
    };

    ws.onmessage = function(event){
        const response = JSON.parse(event.data);
        if (response.status === "success"){
            alert("success")
            document.getElementById("search_tag").value = "";
        }
        else{
            alert(response.detail);
            ws.close();
        }
    };

    ws.onError = function(error){
        alert("Connection error");
        if (ws) ws.close();
    };
};