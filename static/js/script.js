$(document).ready(() => {
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('value update', (data)=>{
        //var ee = {{s_data}};
        //console.log(ee);

        console.log(data["s_data"]);
        
        //$("#rand-value").text(data["s_data"][0][0]);
        //$("#rand-value").text(data["s_data"][0][0]);
        //$("#rand-value1").text(data["s_data"][0][1]);

        // var element = '';
        // $('#block-2').empty();

        // data["s_data"].forEach(e => {
        //     var newElement = 
        //         '<div class="item">'+
        //         '<h3 id="com-name" style="color: black;">' + e[0] + '</h3>' +
        //         '<h6 id="com-value" style="color: black;">' + e[1] + '<br></h6>' +
        //         '<h6 id="com-value" style="color: black;">' + e[2] + '<br></h6>' +
        //         '<h6 id="com-value" style="color: black;">' + e[3] + '<br></h6>' +
        //         '</div>';
        //     // element += newElement;
        //     $('#block-2').fadeOut().append(element).delay(800).fadeIn();
        // });
        // $('#block-2').html(element);
        // $('#block-2 > .item').each(function(){
        //     $(this).fadeOut().next().delay(800).fadeIn();
        // });
        var e = data['s_data'];
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