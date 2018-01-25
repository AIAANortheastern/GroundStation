$(document).ready(function () {

    var width = $( window ).width();

    $.ajax({url: '/data-recent/', success: function(result){
        process_ajax_result(result);
    }});

    $( function() {
        $( "#slider" ).slider({
            orientation: "horizontal",
            max: 1000,
            min: 0
        }).width(width - $(".sidenav").width() - 50);
  } );

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