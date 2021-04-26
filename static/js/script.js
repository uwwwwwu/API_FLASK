$(document).ready(() => {
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('value update', (data)=>{

        console.log(data["s_data"]);
        console.log(data["s_f_data"]);
        console.log(data["etc_data_CB"]);

        //var e = data['s_data'];
        var e = data['etc_data_JJ'];

        var fadeInFadeOut = (i) => {
            var getElement = (i) => {
                if(i==e.length){
                    i = 0;
                }
                var element = 
                    '<div class="item">'+
                    '<h3 id="com-name" style="color: black;">' + e[i][0] + '</h3>' +
                    '<h6 id="com-value" style="color: black;">' + e[i][1] + '<br></h6>' +
                    '<h6 id="com-value" style="color: black;">' + e[i][2] + '<br></h6>' +
                    '<h6 id="com-value" style="color: black;">' + e[i][3] + '<br></h6>' +
                    '</div>';
                return element;
            };
            setTimeout(()=>{
                $('#block-2').html(getElement(i)).fadeIn(5000,() => {
                        fadeInFadeOut(i+1);
                });
            }, 8000);
        };
        fadeInFadeOut(0);
    })
});