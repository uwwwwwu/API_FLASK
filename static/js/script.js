$(document).ready(() => {
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('value update', (data)=>{
        console.log(data["s_data"]);
        $("#rand-value").text(data["s_data"][0][0]);

        //$("#rand-value").text(data["s_data"][0][0]);
        //$("#rand-value1").text(data["s_data"][0][1]);
    })
});