$(document).ready(function(){
    let url = window.location.origin
    let request = new XMLHttpRequest();
    request.open("GET", url + "/get_chats")
    request.send()
    request.onload = () => {
        var chats = JSON.parse(request.response);
        for (let chat of chats){
            var users = 
            `<div style="display: inline-flex;">
                <img src="/static/favicon.ico" class="profile_pic">
                <h2 class="recipient_name" onclick="open_chat(this.textContent)">${chat}</h2>
            </div><br>`
            $('#list').append(users);
        }
        if (tabs[0] == "users"){
            tabs = [];
        }
        if (tabs.length > 0) {
            open_chat(tabs[0], "force");
        }
    }
    setInterval(refresh(chat_counts), 1000)

});

function open_chat(element, priority="none"){
    $('#list').hide();
    $('#tabs').show();
    if ($.inArray(element, tabs) > -1 & priority == "none"){
        $(`#tab_${element}`).show();
        return;
    }

    tabs.push(element);
    var tab = `<div class="tabs" id="tab_${element}">
    <div style="display: inline-flex">
        <img src="/static/favicon.ico" class="profile_pic">
        <h2 class="recipient_name">${element}</h2>
        <button class="cancel_button" onclick="close_chat()">Close</button>
    </div>
    <div id="body" class="imessage">

    </div>
        <form id="form">
            <div class="div">
                <input type="text" id="message" autocomplete="off" autofocus>
                <button type="submit" id="send_message">Send</button>
            </div>
        </form>
    </div>
</div>`

    $('#tabs').append(tab);
    load_chat(element);

}

function close_chat(){
    $('.tabs').hide();
    $('#tabs').hide();
    $('#list').show();
}

function load_chat(user){
    let url = window.location.origin

    let request = new XMLHttpRequest();
    request.open("GET", `${url}/get_messages/${user}-0`);
    request.send();
    request.onload = () => {
        chat_counts[user] = JSON.parse(request.response).length;
        if (request.status === 200) {
            let body = $('#tab_' + user + ' #body');
            for (let obj of JSON.parse(request.response)) {
                if (obj.sender === username ) {
                    var tag = `<p class="from-me margin-b_none" style="font-size: 20px;">${obj.message}</p>`
                    body.append(tag);
                } else {
                        var tag = `<p class="from-them" style="font-size: 20px;">${obj.message}</p>`
                        body.append(tag);
                }
                var date = `<small style="text-align: right; font-size: 15px !important"></small>`
                body.append(date)
            }
            window.scrollTo(0, 10000);
        }
    }
}
function refresh(chat_counts){
    if (Object.keys(chat_counts).length == 0){
        return;
    }
    for (let user of tabs) {
        let url = window.location.origin

        let request = new XMLHttpRequest();
        request.open("GET", `${url}/get_messages/${user}-${chat_counts[user]}`);
        request.send();
        request.onload = () => {
            chat_counts[user] = JSON.parse(request.response).length;
            if (request.status === 200) {
                let body = document.querySelector('#tab_' + user + ' #body');
                for (let obj of JSON.parse(request.response)) {
                    if (obj.sender === username ) {
                        var tag = `<p class="from-me margin-b_none" style="font-size: 20px;">${obj.message}</p>`
                        body.append(tag);
                    } else {
                            var tag = `<p class="from-them" style="font-size: 20px;">${obj.message}</p>`
                            body.append(tag);
                    }
                    var date = `<small style="text-align: right; font-size: 15px !important"></small>`
                    body.append(date)
                }
                window.scrollTo(0, 10000);
            }
        }
    }
}