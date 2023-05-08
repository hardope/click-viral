function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function get(name){
    return document.getElementById(name);
}

function login(){
    let username = get("username").value();
    let password = get("password").value();
    let email = get("email").value();
    let details_message = get("details_message")

    if (username == "" && email == ""){
        details_message.text("Please enter a username or Email address");
    } else if (password == ""){
        details_message.text("Please enter a password");
    }
}