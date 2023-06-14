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
            success: function(data) {
                if (data.success == "Verified"){
                    $('#verify').hide();
                    $('#details').show();
                } else {
                    $('#verify_message').html("Incorrect Password")
                }
            },
            error: function(responseText) {
                $('#verify_message').html("Incorrect Password")
            }
        });
    }
}

function update_details(detail){
    if ($(`#${detail}`).val() == "") {
        $(`#message`).html("Please enter your " + detail)
        return;
    }
    if (detail == "email"){
        if (!validateEmail($(`#${detail}`).val())){
            $(`#message`).html("Please enter a valid email")
            return;
        }
        $('#details').hide();
        return;
    }
    console.log("Here")
    $('#message').html('Loading ...')
    let formdata = new FormData();
    formdata.append('action', `change_${detail}`);
    formdata.append(detail, $(`#${detail}`).val());
    if (detail == "password"){
        formdata.append('confirm_password', $('confirm_password').val());
    }
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
            $('#message').html(`Updated ${detail} successfully`)
        },
        error: function(responseText) {
            console.log(responseText);
            $('#message').html(responseText)
        }
    });
}