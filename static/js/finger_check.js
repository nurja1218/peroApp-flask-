function serial_start(ct) {
    $.ajax({
        type: 'POST',
        url: '/f1_a',
        data: {
            't_data': ct
            },
        success: function(trans_data) {
            touch_data = trans_data.list_of_data;
            if (touch_data[0]) {
                if (ct == 'index') {
                    location.href = "http://localhost:2045/f1-1"
                } else if (ct == 'middle') {
                    location.href = "http://localhost:2045/f1-2"
                } else if (ct == 'ringAndlittle') {
                    location.href = "http://localhost:2045/f1-3"
                } else if (ct == 'little') {
                    location.href = "http://localhost:2045/c2"
                }
            } else {
                if (touch_data[1]) {
//                    document.getElementById("alert_btn").click()
                }
                serial_start(ct)
            }
        }
    });
    event.preventDefault();
}