function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function login(){
    let username = $.get("#username").val();
    let password = $.get("#password").val();
    let email = $.get("#email").val();
    let details_message = $.get("#details_message")

    if (username == "" && email == ""){
        details_message.text("Please enter a username or Email address");
    } else if (password == ""){
        details_message.text("Please enter a password");
    }
}