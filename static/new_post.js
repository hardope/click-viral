function validate(){
    if($("#media").value != "") {
          let label = $("#media_label")
          label.css('background-color', 'green');
    }
}
function new_post() {
    $('#body').css('display', 'none');
    $('#create_post').css('display', 'block');
}


$(document).ready(function() {
    $('#new_post_form').submit(function(e) {
        e.preventDefault(); // prevent default form submission
    
        var formData = new FormData(); // create new FormData object
    
        // add text data to FormData object
        var article = $('#article').val();
        formData.append('article', article);
    
        // add file data to FormData object
        var media = $('#media')[0].files[0];
        formData.append('media', media);

        console.log(article);
    
        // send AJAX request to Django app
        $.ajax({
            url: window.location.origin + '/new_post',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(data) {
                console.log(data); // handle successful response
                $("#create_post").style.display = "none";
                $("#body").style.display = "block";
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText); // handle error response
            }
        });
    });
  });
  