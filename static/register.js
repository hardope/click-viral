function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function confirm(){
    let verify = document.getElementById('verify')
    let details = document.getElementById('details')
    let first_name = document.getElementById('first_name').value
    let last_name = document.getElementById('last_name').value
    let email = document.getElementById('email').value
    let username = document.getElementById('username').value
    let password = document.getElementById('password').value
    let confirm_password = document.getElementById('password_confirm').value
    let details_message = document.getElementById('details_message')

    if (first_name == "" || last_name == "" || email == "" || password == "" || confirm_password == "" || username == ""){
         details_message.innerHTML = "Please Fill in All fields"
    } else if (password != confirm_password) {
         details_message.innerHTML = "Password Does Not Match Confirmation"
    } else if (username.includes(" ")) {
         details_message.innerHTML = "Username cannot contain spaces"
    } else if (validateEmail(email) == false){
         details_message.innerHTML = "Invalid Email"
    } else{
         request_code(username, email);
    }
}
function confirm_otp(){
    let sign_up = document.getElementById('submit_block')
    let verify = document.getElementById('verify')
    let otp = document.getElementById("otp").value;
    let username = document.getElementById('username').value
    let password = document.getElementById('password').value
    let first_name = document.getElementById('first_name').value
    let last_name = document.getElementById('last_name').value
    let email = document.getElementById('email').value
    let verify_message = document.getElementById('verify_message')

    if (otp == ""){
         verify_message.innerHTML = "Please Provide Code"
    } else {
         check_otp(username, password, first_name, last_name, email, otp)
    }
}
function request_code(username, email) {
     let verify = document.getElementById('verify')
     let details = document.getElementById('details')
     let details_message = document.getElementById('details_message')
     let url = window.location.origin
     let request = new XMLHttpRequest();
     var formdata = new FormData()
     formdata.append("username", username)
     formdata.append("csrftoken", csrftoken)
     formdata.append("email", email)
     request.open("POST", url + "/request_code")
     request.setRequestHeader("X-CSRFToken", csrftoken);
     request.send(formdata)
     request.onload = () => {
          if (request.responseText == "0"){
               details.style.display = "none"
               verify.style.display = "block"
          } else if (request.responseText == "1"){
               details_message.innerHTML = "Username Is Unavailable"
          } else if (request.responseText == "2"){
               details_message.innerHTML = "Email Is In use by another account"
          }
          else {
               alert("An Error occurred")
          }
     }
}
function check_otp(username, password, first_name, last_name, email, otp){
     let verify = document.getElementById('verify')
     let verify_message = document.getElementById('verify_message')
     let url = window.location.origin
     let request = new XMLHttpRequest();
     let formdata = new FormData()
     formdata.append("username", username)
     formdata.append("password", password)
     formdata.append("first_name", first_name)
     formdata.append("last_name", last_name)
     formdata.append("email", email)
     formdata.append("otp", otp)
     request.open("POST", url + "/check_otp")
     request.setRequestHeader("X-CSRFToken", csrftoken);
     request.send(formdata)
     request.onload = () => {
          if (request.responseText == "0"){
               verify.style.display = "none"
               window.location.replace(url);
          }
          else if (request.responseText == "1"){
               verify_message.innerHTML = "Invalid Code"
          }
          else if (request.responseText == "2"){
               verify_message.innerHTML = "Code is expired"
          }
          else{
               alert("An Error occurred")
          }
     }
}