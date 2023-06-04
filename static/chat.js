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
    setInterval(function (){
        if (tabs.length == 0 || chat_counts == {} || tabs[0] == "users") {
            return;
        }
        else{
            for (let user of tabs) {
                let url = window.location.origin
                if (chat_counts[user] == undefined){
                    return;
                }
    
                let request = new XMLHttpRequest();
                request.open("GET", `${url}/get_messages/${user}-${chat_counts[user]}`);
                request.send();
                request.onload = () => {
                    if (request.status === 200) {
                        let body = $('#tab_' + user + ' #body');
                        for (let obj of JSON.parse(request.response)) {
                            chat_counts[user] += 1;
                            if (obj.sender === username ) {
                                var tag = `<p class="from-me margin-b_none" style="font-size: 20px;">${obj.message}</p>`
                                body.append(tag);
                                var date = `<small class="from-me margin-b_none" style="text-align: right; font-size: 15px !important">${obj.created_at}</small>`
                                body.append(date)
                            } else {
                                var tag = `<p class="from-them" style="font-size: 20px;">${obj.message}</p>`
                                body.append(tag);
                                var date = `<small class="from-them" style="font-size: 15px !important">${obj.created_at}</small>`
                                body.append(date)
                            }
                            window.scrollTo(0, 10000);
                        }
                    }
                }
            }
        }
    }, 1000)

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
    <div class="div" style="display: inline_flex;">
        <textarea type="text" id="message" autocomplete="off" autofocus></textarea>
        <button type="submit" id="send_message" onclick="send_message('${element}')">Send</button>
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
                    var date = `<small class="from-me margin-b_none" style="text-align: right; font-size: 15px !important">${obj.created_at}</small>`
                    body.append(date)
                } else {
                    var tag = `<p class="from-them" style="font-size: 20px;">${obj.message}</p>`
                    body.append(tag);
                    var date = `<small class="from-them" style="font-size: 15px !important">${obj.created_at}</small>`
                    body.append(date)
                }
            }
            window.scrollTo(0, 10000);
        }
    }
}

function send_message(user){
    $(`#tab_${user} #send_message`).prop("disabled",true);
    let message = $(`#tab_${user} #message`).val();
    if (message == ''){
        return;
    }
    let formData = new FormData();
    formData.append('message', message);
    formData.append('recipient', user);
    $.ajax({
        url: window.location.origin + '/send_message',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(data) {
            $(`#tab_${user} #message`).val('');
            $(`#tab_${user} #send_message`).prop("disabled",false);
        },
        error: function(xhr, status, error) {
            alert("Error, Please Check Your Internet Connection"); // handle error response
        } 
    });
}