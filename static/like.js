/* Get the count of likes on input */

function get_int(input){
    console.log("INTEGER")
    console.log(input.slice(0,-1))
    return parseInt(input.slice(0,-1));
}

/* Like or unlike post */
function like(input){
    let box = document.getElementById(input)

    console.log(box.getAttribute('value'))
    if (box.getAttribute('value') == "true" || box.getAttribute('value') == "True") {
        box.innerHTML = (get_int(box.textContent) - 1) + " 🖤"
        box.setAttribute('value', "false")
        let url = window.location.origin
        let request = new XMLHttpRequest();
        let body = document.querySelector('#body');
        request.open("GET", url + "/unlike/" + input);
        request.send();

    } else {
        box.setAttribute('value', "true")
        box.innerHTML = (get_int(box.textContent) + 1) + " ❤️"
        let url = window.location.origin
        let request = new XMLHttpRequest();
        let body = document.querySelector('#body');
        request.open("GET", url + "/like/" + input);
        request.send();

    }
}