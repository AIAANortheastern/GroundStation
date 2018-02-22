$(document).ready(function() {

    var width = $(window).width();
    var csv_length = 0;
    current_data = [];
    var element_order = [];
    var graph_div = 'graph';
    $.ajax({
        url: '/data-length/',
        success: function(result) {
            csv_length = result;
            $(function() {
                $("#slider").slider({
                    orientation: "horizontal",
                    max: csv_length,
                    min: 1,
                    create: function(event, ui) {
                        $.ajax({
                            url: '/data-range/',
                            data: "start=" + 1 + "&end=" + 10,
                            success: function(result) {
                                //console.log(result);
                                set_sidebar_init(result);
                            }
                        })
                    },
                    stop: function(event, ui) {
                        difference = 10;
                        end_value = ui.value;
                        if (end_value - difference < 2) { // first line is headers
                            end_value = difference + 2;
                        }
                        start_value = end_value - difference; // get the other side of values -- eventually want to make this modifiable too
                        var t4 = performance.now();
                        $.ajax({
                            url: '/data-range/',
                            data: "start=" + start_value + "&end=" + end_value,
                            success: function(current_data) {
                            console.log("Call to ajax took " + (performance.now() - t4) + " milliseconds.")
                                set_sidebar(current_data); //set sidebar to exactly where the slider is
                                var children = document.getElementById("graphs").children;
                                for (var i = 0; i < children.length; i++) {
                                    var tableChild = children[i];
                                    var t0 = performance.now();
                                    update_graph(current_data, tableChild.getAttribute("num"));
                                    var t1 = performance.now();
                                    console.log("Call to update_graph took " + (t1 - t0) + " milliseconds.")
                                }
                            }
                        });
                    }
                }).width(width - $(".sidenav").width() - 50);
            });
        }
    });

    function init_graph(input_data, data_slot) {
        data = reformat_all_data(input_data, data_slot);
        Plotly.newPlot(graph_div + data_slot, data);
    }

    function make_graph_div(name, num) {
        newdiv = document.createElement("div");
        $(newdiv).attr('id', name);
        $(newdiv).attr('num', num);
        //console.log(name);
        //console.log($("#graphs").append(newdiv));
    }

    function update_graph(input_data, data_slot) {
        data_update = reformat_all_data(input_data, data_slot);
        range = get_range_of_array(input_data, data_slot);
        range_update = {
            title: 'Data at ' + data_update[0].x[0], // updates the title
            'xaxis.range': [reformat_date(input_data[0][0]), reformat_date(input_data[input_data.length - 1][0])], // updates the xaxis range
            'yaxis.range': [range[0], range[1]] // updates the end of the yaxis range
        };
        //console.log(range_update);
        Plotly.animate(div = graph_div + data_slot, {
            data: data_update,
            traces: [0],
            /* With a bit of work, you can list any other traces you
                            want to update too (e.g. make a for loop over trace++ and set
                            update[trace] at each iteration) */
            layout: range_update
        }, {
            // These 2 make sure the plot updates as quickly as possible:
            transition: {
                duration: 0
            },
            frame: {
                duration: 0,
                redraw: false
            }
        });
    }

    function get_range_of_array(data, position) {
        array = [];
        for (var i = 0; i < data.length; i++) {
            array[i] = data[i][position];
        }
        return [Array.min(array), Array.max(array)];
    }

    function reformat_all_data(data, position) { //this will take the data from the api and put it into the plotly.js graph data format
        var data_type = [{
            x: [],
            y: [],
            type: 'scatter'
        }];
        var i = 0;
        if (data[0][0] == 'timestamp') {
            i = 1
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
        for (var i = 0; i < data_array[0].length; i++) {
            $('#' + element_order[i]).text(element_order[i] + ': ' + Math.round(data_array[1][i] * 100) / 100);
            $('#' + element_order[i]).attr('num', i);
            if(i >=1){
                $('#'+element_order[i]).click(function(element) {
                    attribute_clicked(element.currentTarget.getAttribute("num"), data_array);
                });
            }
        }
    }

    function set_sidebar(data_array) {
        for (var i = 0; i < data_array[0].length; i++) {
            $('#' + element_order[i]).text(element_order[i] + ': ' + Math.round(data_array[1][i] * 100) / 100);
        }
    }

    function attribute_clicked(attribute, data_array) {
        if ($('#graph' + attribute).length !== 0) {
            Plotly.purge('graph' + attribute);
            $('#graph' + attribute).remove();
        } else {
            //console.log(attribute);
            make_graph_div('graph' + attribute, attribute);
            init_graph(data_array, attribute);
        }
    }

    window.onresize = function() {
        var children = document.getElementById("graphs").children;
        for (var i = 0; i < children.length; i++) {
            Plotly.Plots.resize(children[i]);
        }
        var width = $(window).width();
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