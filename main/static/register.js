function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function request_code(username, email) {
    let verify = $('#verify');
    let details = $('#details');
    let details_message = $('#details_message');
    let url = window.location.origin;
    let formdata = new FormData();
    formdata.append('username', username);
    formdata.append('csrftoken', csrftoken);
    formdata.append('email', email);

    $.ajax({
        url: url + '/request_code',
        type: 'POST',
        data: formdata,
        dataType: 'text',
        contentType: false,
        processData: false,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(responseText) {
            if (responseText == '0') {
                details.hide();
                verify.show();
            } else if (responseText == '1') {
                details_message.html('Username Is Unavailable');
                $('#auth').css('background-color', 'red')
            } else if (responseText == '2') {
                details_message.html('Email Is In use by another account');
                $('#auth').css('background-color', 'red')
            } else {
                alert('An Error occurred');
            }
        }
    });
}

function confirm() {
    $('#details_message').html('Loading...');
    let verify = $('#verify');
    let details = $('#details');
    let first_name = $('#first_name').val();
    let last_name = $('#last_name').val();
    let email = $('#email').val();
    let username = $('#username').val();
    let password = $('#password').val();
    let confirm_password = $('#password_confirm').val();
    let details_message = $('#details_message');

    if (first_name == '' || last_name == '' || email == '' || password == '' || confirm_password == '' || username == '') {
        details_message.html('Please Fill in All fields');
        $('#auth').css('background-color', 'red')
    } else if (password != confirm_password) {
        details_message.html('Password Does Not Match Confirmation');
        $('#auth').css('background-color', 'red')
    } else if (username.includes(' ')) {
        details_message.html('Username cannot contain spaces');
        $('#auth').css('background-color', 'red')
    } else if (validateEmail(email) == false) {
        details_message.html('Invalid Email');
        $('#auth').css('background-color', 'red')
    } else {
        request_code(username, email);
    }
}
function confirm_otp() {
    $('#verify_message').html('Loading...');
    let sign_up = $('#submit_block');
    let verify = $('#verify');
    let otp = $('#otp').val();
    let username = $('#username').val();
    let password = $('#password').val();
    let first_name = $('#first_name').val();
    let last_name = $('#last_name').val();
    let email = $('#email').val();
    let verify_message = $('#verify_message');

    if (otp == "") {
        verify_message.html("Please Provide Code");
    } else {
        $.ajax({
            type: "POST",
            url: window.location.origin + "/check_otp",
            headers: {"X-CSRFToken": csrftoken},
            data: {username: username, password: password, first_name: first_name, last_name: last_name, email: email, otp: otp},
            success: function(response) {
                if (response == "0") {
                    verify.hide();
                    window.location.replace(window.location.origin);
                } else if (response == "1") {
                    verify_message.html("Invalid Code");
                    $('#verify_otp').css('background-color', 'red')
                } else if (response == "2") {
                    verify_message.html("Code is expired");
                    $('#verify_otp').css('background-color', 'red')
                } else {
                    alert("An Error occurred");
                }
            },
            error: function() {
                alert("An Error occurred");
            }
        });
    }
}
