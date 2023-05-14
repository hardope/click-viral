function validate(){
    if($("#media").value != "") {
          let label = $("#media_label")
          label.css('background-color', 'green');
    }
}

function new_post() {
    $('#main').hide();
    $('#create_post').show();
}

function add_post(id) {
    console.log("Adding Post")
    let url = window.location.origin
    let request = new XMLHttpRequest();
    request.open("GET", url + "/get_post/" + id)
    request.send()
    request.onload = () => {
        var posts = JSON.parse(request.response);
        for (var i = 0; i < posts.length; i++) {
            var post = posts[i];
            var nameContainer = '<div class="name_container"><a class="a" href="/profile/' + post.name + '" style="display: inline-flex"><img src="/static/favicon.ico" style="width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 0px"><div style="margin-left: 10px; margin-top: 30px;">' + post.name + '</div></a><div style="margin-top: -10px; margin-left: 30px; font-size 1px !important;">' + post.created_at;
            if (post.name == username) {
                nameContainer += '<a href="edit_post/' + post.id + '"><button style="background-color: lightblue;border: none; margin-left: 90%; width: 40px; height:40px; border-radius: 20px; margin-bottom: 10px;" type="submit">✏️</button></a>';
            } else if (post.edited == true) {
                nameContainer += '<button style="background-color: lightblue;border: none; margin-left: 80%; width: 100px; height:40px; border-radius: 15px; margin-bottom: 10px;" type="submit">Edited</button>';
            }
            nameContainer += '</div></div>';

            var article = '<div class="div"><div>';
            for (var j = 0; j < post.article.length; j++) {
                var element = post.article[j];
                article += '<' + element.tag + '>' + element.text + '</' + element.tag + '>';
            }
            article += '</div></div>';

            var media = '';
            if (post.media != "empty") {
                if (post.media == "mp4") {
                    media += '<video src="/media/posts/' + post.id + '.mp4" controls loop preload="auto"></video>';
                } else {
                    media += '<a href="/media/posts/' + post.id + '.' + post.media + '"><img src="/media/posts/' + post.id + '.' + post.media + '"></a>';
                }
            }

            var container = '<div class="container">';
            if (post.like_value == "True") {
                container += '<p class="react" value="' + post.like_value + '" id="' + post.id + '" onclick="like(\'' + post.id + '\')">' + post.likes + ' ❤️</p>';
            } else {
                container += '<p class="react" value="' + post.like_value + '" id="' + post.id + '" onclick="like(\'' + post.id + '\')">' + post.likes + ' 🖤</p>';
            }
            container += '<a href="/comment/' + post.id + '"><p class="comment">' + post.comments + ' 💬</p></a><p class="v_like" onclick="view_likes(\'' + post.id + '\')">📊</p></div>';

            var postElement = nameContainer + article + media + container;
            $('#body').prepend(postElement)
            }
    }
}


$(document).ready(function() {
    $('#new_post_form').submit(function(e) {
        e.preventDefault(); // prevent default form submission
    
        var formData = new FormData(); // create new FormData object
    
        // add text data to FormData object
        var article = $('#article').val();
        formData.append('article', article);
    
        // add file data to FormData object
        var media = $('#media')[0].files[0];
        formData.append('media', media);
    
        // send AJAX request to Django app
        $("#upload_message").html("Uploading Your File Please wait...")
        $.ajax({
            url: window.location.origin + '/new_post',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(data) {
                // handle successful response
                $("#create_post").hide();
                $("#main").show();
                add_post(data)
            },
            error: function(xhr, status, error) {
                console.log("Unable To upload Your FIle, Please Check Your Internet Connection"); // handle error response
            }
        });
    });
  });
  