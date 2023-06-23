function find_account(){
    var username = $('#username').val()
    var email = $('#email').val()
    var message = $('#message')

    if (username == email == ""){
        message.html("Please enter a username or Email address");
    }

    message.html("Loading...");

    var url = window.location.origin;
    var formdata = new FormData();
    formdata.append("username", username);
    formdata.append("email", email);
    formdata.append("action", "find_account");
    $.ajax({
        type: "POST",
        url: url + "/forgot_password",
        data: formdata,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(data) {
            if (data.success){
                $('#find').hide();
                $('#verify').show();
            }
            else{
                message.html(data.error);
            }
        }
    });
}

function verify_forgot_password(){
    var email = $('#email').val();
    var password = $('#password').val();
    confirm_password = $('#confirm_password').val();
    var otp = $('#otp').val();
    var message = $('#message');
    if (password != confirm_password){
        message.html("Passwords do not match");
        return;
    }
    if (password.length < 8){
        message.html("Password must be at least 8 characters long");
        return;
    }
    message.html("Loading...");
    var url = window.location.origin;
    var formdata = new FormData();
    formdata.append("otp", otp);
    formdata.append("password", password);
    formdata.append("email", email);
    formdata.append("action", "verify_otp");
    $.ajax({
        type: "POST",
        url: url + "/forgot_password",
        data: formdata,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(data) {
            if (data.success){
                window.location.replace(url + "/");
            }
            else{
                message.html(data.error);
            }
        }
    });
}