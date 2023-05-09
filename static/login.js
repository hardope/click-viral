function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function load_login(){
    let username = $("#username").val();
    let password = $("#password").val();
    let email = $("#email").val();
    let details_message = $("#details_message")

    if (username == "" && email == ""){
        details_message.text("Please enter a username or Email address");
    } else if (password == ""){
        details_message.text("Please enter a password");
    }
    
    details_message.text("Logging You In...");
    
    let url = window.location.origin
    let request = new XMLHttpRequest();
    var formdata = new FormData()
    formdata.append("username", username)
    formdata.append("email", email)
    formdata.append("password", password)
    request.open("POST", url + "/login")
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.send(formdata)
    request.onload = () => {
        if (request.responseText == "0"){
            window.location.replace(url)
        }
        else if (request.responseText == "1"){
            details_message.text("Invalid Username or Password")
        }
        else if (request.responseText == "2"){
            details_message.text("Invalid")
        }
    }
}