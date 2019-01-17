$(document).ready(function(){
    $.ajax({
        url: '/available-files',
        success: function(result) {
            let total_string = '<div class="dropdown"> <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown button</button><div class="dropdown-menu" aria-labelledby="dropdownMenuButton">';
            for (let index = 0; index < result.length; index++) {
                total_string +='<a class="dropdown-item" id='+index+' href="#">'+ result[index] +'</a>';
            }
            total_string += "</div></div>";
            $("#file-list").after(total_string);
            for (let index = 0; index < result.length; index++) {
                $("#"+index).click(function(){
                    localStorage.setItem("filename", result[index]);
                });
            }
        }
    });
});
