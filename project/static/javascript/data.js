$(document).ready(function() {
    let filename = localStorage.getItem("filename");
    $("#data_name").text("File selected: "+filename);
    let width = $("#slider").width();
    let csv_length = 0;
    let current_data = [];
    let element_order = [];
    let graph_div = 'graph';
    let difference = 10;
    $.ajax({
        url: '/data-length/',
        data: {"filename": filename},
        success: function(result) {
            csv_length = result;
            $(function() {
            var mySlider =  $("#slider").slider();
               mySlider
                .slider({
                    orientation: "horizontal",
                    max: csv_length,
                    min: 1});
               mySlider
                .on("slideStop", function(event, ui) {
                    //console.log(ui);
                    end_value = mySlider.slider('getValue');
                    if (end_value - difference < 2) { // first line is headers
                        end_value = difference + 2;
                    }
                    start_value = end_value - difference; // get the other side of values -- eventually want to make this modifiable too
                    let t4 = performance.now();
                    $.ajax({
                        url: '/data-range/',
                        data: "start=" + start_value + "&end=" + end_value+"&filename="+filename,
                        success: function(current_data) {
                            console.log("Call to ajax took " + (performance.now() - t4) + " milliseconds.");
                            set_sidebar(current_data); //set sidebar to exactly where the slider is
                            let children = document.getElementById("graphs").children;
                            for (let i = 0; i < children.length; i++) {
                                let tableChild = children[i];
                                let t0 = performance.now();
                                update_graph(current_data, tableChild.getAttribute("num"));
                                console.log("Call to update_graph took " + (performance.now() - t0) + " milliseconds.")
                            }
                        }
                    });
                });
                $.ajax({
                    url: '/data-range/',
                    data: "start=" + 1 + "&end=" + difference+"&filename="+filename,
                    success: function(result) {
                        //console.log(result);
                        set_sidebar_init(result);
                    }
                });

                //.width(width - $(".sidenav").width() - 50);

            });
        }
    });

    function init_graph(input_data, data_slot) {
        data = reformat_all_data(input_data, data_slot);
        element_order = input_data[0];
        console.log(data);
        title_data =  {title: element_order[data_slot]+' at ' + data[0].x[1]}
        Plotly.newPlot(graph_div + data_slot, data, title_data);
    }

    function make_graph_div(name, num) {
        newdiv = document.createElement("div");
        $(newdiv).attr('id', name);
        $(newdiv).attr('num', num);
        $("#graphs").append(newdiv);
    }

    function update_graph(input_data, data_slot) {
        data_update = reformat_all_data(input_data, data_slot);
        range = get_range_of_array(input_data, data_slot);
        console.log(range);
        range_update = {
            title: element_order[data_slot]+' at ' + data_update[0].x[0], // updates the title
            xaxis: {autorange: true},
            yaxis: {autorange: true}
        };
        //console.log(range_update);
        Plotly.animate(div = graph_div + data_slot, {
            data: data_update,
            traces: [0],
            /* With a bit of work, you can list any other traces you
                            want to update too (e.g. make a for loop over trace++ and set
                            update[trace] at each iteration) */

        },
        range_update).then(function(){
        console.log(graph_div + data_slot);
        Plotly.relayout( graph_div + data_slot, {
            'xaxis.autorange': true,
            'yaxis.autorange': true
        });

        });

    }

    function get_range_of_array(data, position) {
        array = [];
        for (let i = 0; i < data.length; i++) {
            array[i] = data[i][position];
        }
        return [Array.min(array), Array.max(array)];
    }

    function reformat_all_data(data, position) { //this will take the data from the api and put it into the plotly.js graph data format
        let data_type = [{
            x: [],
            y: [],
            type: 'scatter'
        }];
        let i = 0;
        if (data[0][0] == 'timestamp') {
            i = 1;
        } //if the first line is the headers, skip it
        for (; i < data.length; i++) {
            data_type[0].x[i] = reformat_date(data[i][0]);
            data_type[0].y[i] = parseFloat(data[i][position]);
        }
        return data_type;
    }

    function reformat_date(date) { //this converts dates to a plotly.js friendly format
        date = date.split(":");
        return (date[0] + '-' + date[1] + '-' + date[2] + ' ' + date[3] + ':' + date[4] + ":" + date[5])
    } // needs to be 2013-10-04 22:23:00

    Array.min = function(array) {
        return Math.min.apply(Math, array);
    };

    Array.max = function(array) {
        return Math.max.apply(Math, array);
    };

    function set_sidebar_init(data_array) {
        element_order = data_array[0];
        //console.log(data_array);
        for (let i = 0; i < data_array[0].length; i++) {
            $('#' + element_order[i]).text(element_order[i] + ': ' + Math.round(data_array[1][i] * 100) / 100);
            $('#' + element_order[i]).attr('num', i);
            if(i >= 1){
                $('#'+element_order[i]).click(function(element) {
                    if($(this).css("color") === "rgb(168, 219, 146)"){
                    $(this).css("background","#AA3939");
                    $(this).css("color","#FFAAAA");
                    }
                    else{
                    $(this).css("background","#4E9231");
                    $(this).css("color","#A8DB92");
                    }
                    attribute_clicked(element.currentTarget.getAttribute("num"), data_array);
                });
            }
        }
        $("button")
            .button( {
                text: true
            } )
            .css("background","#AA3939")
            .css("color","#FFAAAA")
            .css("padding","5px 10px")
            .css("margin","3px 2px")
            .css("border","none");
    }

    function set_sidebar(data_array) {
        for (let i = 0; i < data_array[0].length; i++) {
            $('#' + element_order[i]).text(element_order[i] + ': ' + Math.round(data_array[1][i] * 100) / 100);
        }
    }

    function attribute_clicked(attribute, data_array) {
        if ($('#graph' + attribute).length !== 0) {
            Plotly.purge('graph' + attribute);
            $('#graph' + attribute).remove();
        } else {
            make_graph_div('graph' + attribute, attribute);
            init_graph(data_array, attribute);
        }
    }

    window.onresize = function() {
        let children = document.getElementById("graphs").children;
        for (let i = 0; i < children.length; i++) {
            Plotly.Plots.resize(children[i]);
        }
        let width = $(window).width();
        $("#slider").width(width - $(".sidenav").width() - 50);
    };



    /*$(document).keydown(function(e) {
        switch (e.which) {
            case 37: // left
                // Get the previous data element from the server calculate how many entries there are and divide that by the
                // size of the slider space to see how many steps to take.
                break;

            case 38: // up
                break;

            case 39: // right
                // get next data value
                $.ajax({
                    url: '/data-recent/',
                    success: function(result) {
                        process_ajax_result(result);
                    }
                });
                break;

            case 40: // down
                break;

            default:
                return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    });*/

});