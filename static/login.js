function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function load_login(){
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let email = document.getElementById("email").value;
    let details_message = document.getElementById("details_message")

    if (username == "" && email == ""){
        details_message.text("Please enter a username or Email address");
    } else if (password == ""){
        details_message.text("Please enter a password");
    }
}