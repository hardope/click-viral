function toggle_edit(num){
    if (num == 1) {
        $('#view_profile').hide();
        $('#edit_profile').show();
    }
    else {
        $('#view_profile').show();
        $('#edit_profile').hide();
    }
}

function upload_image() {
    console.log('uploading image')
    var formData = new FormData();

    formData.append('image', $('#image_file')[0].files[0]);
    formData.append('username', username);
    formData.append('action', 'upload');

    $("#edit_profile_message").html("Uploading Your Profile photo...")
    $.ajax({
        url: window.location.origin + '/edit_profile',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(data) {
            // handle successful response
            $("#edit_profile_message").html("Profile photo uploaded successfully")
            $("#profile_image").attr("src", "/media/profile/" + username + data.image);
        },
        error: function(xhr, status, error) {
            alert("Unable To upload Your post, Please Check Your Internet Connection"); // handle error response
        }
    });
}