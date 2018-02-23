$(document).ready(function() {
    $('#to_data').click(function(element) {
        var url = "";
        $(location).attr('href',window.location.href+url);
    });
    $('#add_csv').click(function(element) {
        var url = "data-main";
        $(location).attr('href',window.location.href+url);
    });
    $('#more_info').click(function(element) {
        var url = "https://github.com/AIAANortheastern/GroundStation";
        $(location).attr('href',url);
    });
});
