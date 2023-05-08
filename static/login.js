function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function $(name){
    return document.getElementById(name);
}

function login(){
    let username = $("username").value();
    let password = $("password").value();
    let email = $("email").value();
    let details_message = $("details_message")

    if (username == "" && email == ""){
        details_message.text("Please enter a username or Email address");
    } else if (password == ""){
        details_message.text("Please enter a password");
    }
}