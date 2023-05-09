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
}