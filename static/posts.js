$(document).ready(function(){
    let url = window.location.origin
    let request = new XMLHttpRequest();
    request.open("GET", url + "/fetch_posts")
    request.send()
    request.onload = () => {
        var posts = JSON.parse(request.response);
        for (var i = 0; i < posts.length; i++) {
            var post = posts[i];
            var nameContainer = '<div class="name_container"><a class="a" href="/profile/' + post.name + '" style="display: inline-flex"><img src="/static/favicon.ico" style="width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 0px"><div style="margin-left: 10px; margin-top: 30px;">' + post.name + '</div></a><div style="margin-top: -10px; margin-left: 30px; font-size 1px !important;">' + post.created_at;
            if (post.name == username) {
                nameContainer += '<button ' + 'onclick=edit_post("' + post.id + '")' + ' style="background-color: lightblue;border: none; margin-left: 90%; width: 40px; height:40px; border-radius: 20px; margin-bottom: 10px;" type="submit">✏️</button>';
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
            
            var postElement = '<div id="' + 'post_' + post.id + '">' + (nameContainer + article + media + container) + '</div>'
            $('#body').append(postElement)
            }
    }
})

function edit_post(id){
    $("#main").hide()
    $('#edit_post').show()
    let url = window.location.origin
    let request = new XMLHttpRequest();
    request.open("GET", url + "/get_post/" + id)
    request.send()
    request.onload = () => {
        if (request.status === 200) {
            var post = JSON.parse(request.response)[0];
            // check if the post has media and display it in the DOM
            if (post.media !== "empty") {
                if (post.media === "mp4") {
                    $('#post_media').html(`<video src="/media/posts/${post.id}.mp4" controls loop preload="auto"></video>`);
                } else {
                    $('#post_media').html(`<a href="/media/posts/${post.id}.${post.media}"><img src="/media/posts/${post.id}.${post.media}"></a>`);
                }
                $('#post_media').show();
            } else {
                $('#post_media').hide();
            }

            // check if the post is editable and display the appropriate form
            if (post.editable) {
                $('#edit_article').val(post.raw_article);
                $('#edit_article').attr('readonly', false);
                $('#edit_message').html('<b>Edit Post</b>');
                $('#submit_post').show();
                $('#submit_post').click( function() {
                    var formData = new FormData();
                    formData.append("post", $('#edit_article').val())
                    $.ajax({
                        url: window.location.origin + '/edit_post/' + id,
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        headers: {
                            "X-CSRFToken": csrftoken
                        },
                        success: function(data) {
                            // handle successful response
                            console.log(data);
                            $("#main").show();
                        },
                        error: function(xhr, status, error) {
                            console.log(error); // handle error response
                        }
                    });
                });
            } else {
                $('#edit_article').val(post.raw_article);
                $('#edit_article').attr('readonly', true);
                $('#edit_message').html('<b>Editing Period Has Elapsed</b>');
                $('#submit_post').hide();
            }

            // display the delete post button and prompt
            $('#delete-btn').show();
            $('#delete-btn').click(function() {
                $('#confirm').show();
            });
            $('#confirm .btn-yes').click(function() {
                let request = new XMLHttpRequest();
                request.open("GET", url + "/delete" + id)
                request.send()
            });
            $('#confirm .btn-no').click(function() {
                $('#confirm').hide();
            });
        } else{
            $("#edit_post").hide();
            $("#main").show();
            alert("An error occurred. Please try again")
        }
    }
}