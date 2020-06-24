var active_app = document.getElementsByClassName('m-app-button-clicked')[0];
var application = active_app.children[1].text

var gesture_type = "L1";
var SelectedText = "";
var selectOpt = "";
var touchId = "";
var isRun = false;
// 클릭 이벤트가 발생한 부분을 타케팅하여 ajax이벤트 발생
$( "body" ).click(function( event ) {
    var gesture = $(event.target).parent()[0];
    gesture = gesture.toString();
    if (gesture.charAt(0) == 'h') {
        if (parseInt(gesture.split('L')[1]) < 9) {
            gesture_type = gesture.split('#')[1];
            touchId = ['#field-' + gesture_type.split('L')[1] + '_7',
              '#field-' + gesture_type.split('L')[1] + '_3',
              '#field-' + gesture_type.split('L')[1] + '_2'];
            for (var i = 0; i < 3; i++){
                $(touchId[i]).empty();
                $(touchId[i]).append($("<option>Not Selected</option>"))
            }
            $.ajax({
                type: 'POST',
                url: '/m2-app-getData',
                data: {
                    'gesture_data': gesture_type,
                    'active_app' : application
                    },
                success: function(cmd_group) {
                    cmd_names = cmd_group.list_of_data;
                    for(var i = 0; i < 3; i++){
                        for(var j = 0; j < cmd_names.length; j++){
                            if (cmd_names[j].indexOf('_') == -1){
                                var option = $("<option>"+cmd_names[j]+"</option>");
                            } else {
                                c_t = cmd_names[j].split('_t')[1]
                                c_n = cmd_names[j].split('_t')[0]
                                if ((i+2).toString() == c_t){
                                    var option = $("<option selected>"+c_n+"</option>");
                                } else {
                                    var option = $("<option disabled>"+c_n+"</option>");
                                }
                            }
                            $(touchId[i]).append(option);
                        }
                    }
            }});
            event.preventDefault();
        }
    }
});


var s_id = '#field-1_7';
$(s_id).on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});

$('#field-2_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-3_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-4_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-5_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-6_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-7_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-8_7').on('change', function () {
    touchId = 'touch2'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-1_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-2_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-3_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-4_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-5_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-6_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-7_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-8_3').on('change', function () {
    touchId = 'touch3'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-1_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-2_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-3_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-4_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-5_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-6_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-7_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});
$('#field-8_2').on('change', function () {
    touchId = 'touch4'
    SelectedText = $('option:selected',this).text();
    $.ajax({
        type: 'POST',
        url: '/m2-app-data',
        data: {
            'gesture_data': gesture_type,
            'touch_data' : touchId,
            'command' : SelectedText,
            'active_app' : application
            },
        success: function(result) {
    }});
    event.preventDefault();
});