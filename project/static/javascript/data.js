$(document).ready(function () {

    var width = $( window ).width();
    var csv_length = 0;
    current_data = []
    $.ajax({url: '/data-length/', success: function(result){
        csv_length = result;
        $( function() {
            $( "#slider" ).slider({
                orientation: "horizontal",
                max: csv_length,
                min: 1,
                slide: function(event, ui) {
                    start_value = ui.value -10; // get the other side of values -- eventually want to make this modifiable too
                    $.ajax({url: '/data-range/',data: "start="+start_value+"&end="+ui.value , success: function(result){
                        current_data = result;
                        set_sidebar(current_data[0]);
                    }});
                }
            }).width(width - $(".sidenav").width() - 50);
         } );
    }});

    function set_sidebar(data_array){
    $("#altitude").text("Altitude: "+data_array[1])
    $("#pressure").text("Pressure: "+data_array[2])
    $("#temperature").text("Temperature: "+data_array[3])
    $("#gyrox").text(data_array[4])
    $("#gyroy").text(data_array[5])
    $("#gyroz").text(data_array[6])
    $("#magx").text(data_array[7])
    $("#magy").text(data_array[8])
    $("#magz").text(data_array[9])
    $("#rhall").text(data_array[10])

    //$("#longitude").value = data_array
    //$("#latitude").value = data_array

    //$("#accx").value = data_array
    //$("#accy").value = data_array
    //$("#accz").value = data_array
    }

    function get_data(result, start, stop){

    }

    function process_ajax_result(result){
        console.log(result);
        keys = Object.keys(result);
        keys.forEach(function(element) {
            if(element === 'timestamp') {
                $('#' + element).text(result[element])
            }
            else if(element === 'slider_pos') {
                $('#slider').slider('value', result[element])
            }
            else {
                var index = $('#' + element).text().indexOf(':');
                var substr = $('#' + element).text().substring(0, index + 1)
                $('#' + element).text(substr + ' ' + result[element])
            }
        });
    }

  $(document).keydown(function(e) {
    switch(e.which) {
        case 37: // left
        // Get the previous data element from the server calculate how many entries there are and divide that by the
        // size of the slider space to see how many steps to take.
        break;

        case 38: // up
        break;

        case 39: // right
        // get next data value
        $.ajax({url: '/data-recent/', success: function(result){
            process_ajax_result(result);
        }});
        break;

        case 40: // down
        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});

});