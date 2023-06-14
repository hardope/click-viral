function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

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
                data = JSON.parse(data);
                if (data.response){
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
        if ($(`#${detail}`).val() == "email"){
            $(`#message`).html("Email is the same")
            return;
        }
        return;
    }
    $('#message').html('Loading ...')
    let formdata = new FormData();
    formdata.append('action', `change_${detail}`);
    formdata.append(detail, $(`#${detail}`).val());
    if (detail == "password"){
        formdata.append('confirm_password', $('#confirm_password').val());
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
        success: function(data) {
            if (detail == "email"){
                $('#verify_message').html("Please check your email for a verification code")
                $('#details').hide();
                $('#verify').show();
                return;
            }
            data = JSON.parse(data)
            $('#message').html(data.response)
        },
        error: function(responseText) {
            $('#message').html(responseText)
        }
    });
}