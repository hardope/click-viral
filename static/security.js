function verify_user(){
    var password = $('#verify_password').val();
    if (password == ""){
        $('#verify_message').html("Please enter your password")
        return;
    }
    else{
        $('#verify_message').html('Loading ...')
        let formdata = new FormData();
        formdata.append('password', password);
        formdata.append('action', 'verify');
        formdata.append('csrftoken', csrftoken);

        $.ajax({
            url: window.location.origin + '/security',
            type: 'POST',
            data: formdata,
            dataType: 'text',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(responseText) {
                $('#verify').hide();
                $('#details').show();
            },
            error: function(responseText) {
                $('#verify_message').html("Incorrect Password")
            }
        });
    }
}

function update_details(detail){
    console.log($(`#${detail}`).val())
}