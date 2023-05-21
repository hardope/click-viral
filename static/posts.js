let url = window.location.origin

let c_blocks = localStorage.getItem("comment_blocks");

function view_comment(id){
    c_blocks.append(id);
    console.log(c_blocks);
    localStorage.setItem("comment_blocks", c_blocks);
    $('#main').hide();
    $('#comment_block').show();
    if (c_blocks.length > 0){
        last = c_blocks.pop();
        $('#comment_block_' + last).hide();
    }
    new_block = '<div id="comment_block_' + id + '"></div>';
    $('#comment_block').append(new_block);
    $.ajax({
        url: window.location.origin + '/comment/' + id,
        type: 'GET',
        data: {},
        processData: false,
        contentType: false,
        success: function(data) {
            // handle successful response
            var post = data.post;
            var nameContainer = '<div class="name_container"><a class="a" href="/profile/' + post.name + '" style="display: inline-flex"><img src="/static/favicon.ico" style="width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 0px"><div style="margin-left: 10px; margin-top: 30px;">' + post.name + '</div></a><div style="margin-top: -10px; margin-left: 30px; font-size 1px !important;">' + post.created_at;
            if (post.name == username) {
                nameContainer += '<button ' + 'onclick=edit_post("' + post.id + '")' + ' style="background-color: lightblue;border: none; margin-left: 90%; width: 40px; height:40px; border-radius: 20px; margin-bottom: 10px;" type="submit">✏️</button>';
            } else if (post.edited == true) {
                nameContainer += '<button style="background-color: lightblue;border: none; margin-left: 80%; width: 100px; height:40px; border-radius: 15px; margin-bottom: 10px;" type="submit">Edited</button>';
            }
            nameContainer += '</div></div>';

            var article = '<div class="div" id="article_' + post.id + '"><div>';
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

            var postElement = '<div id="' + 'post_' + post.id + '">' + (nameContainer + article + media) + '</div>'
            $('#comment_block_' + id).append(postElement)

            var upload_comment = '<form><center><h1>New Comment</h1><textarea name="comment" maxlength="1000" style="width:500px; padding: 10px; height: 200px; border-radius: 10px;"></textarea><input type="file" id="media" onchange="validate()" name="media" accept="image/*,video/mp4" value="" hidden><div id="label_cont"><label for="media" id="media_label">Upload Media &#128206;</label></div><button  type="submit" id="button" data-mdb-ripple-color="dark" style="font-size: 60px; color: black; border: 0ch; margin-bottom: 2%; border-radius: 10px 10px 10px 10px;  width: 200px; height: 50px;">Comment</button></center></form>'
            $('#comment_block_' + id).append(upload_comment)

            for (var i = 0; i < data.comments.length; i++) {
                var post = data.comments[i];
                var nameContainer = '<div class="name_container"><a class="a" href="/profile/' + post.name + '" style="display: inline-flex"><img src="/static/favicon.ico" style="width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 0px"><div style="margin-left: 10px; margin-top: 30px;">' + post.name + '</div></a><div style="margin-top: -10px; margin-left: 30px; font-size 1px !important;">' + post.created_at;
                if (post.name == username) {
                    nameContainer += '<button ' + 'onclick=edit_post("' + post.id + '")' + ' style="background-color: lightblue;border: none; margin-left: 90%; width: 40px; height:40px; border-radius: 20px; margin-bottom: 10px;" type="submit">✏️</button>';
                } else if (post.edited == true) {
                    nameContainer += '<button style="background-color: lightblue;border: none; margin-left: 80%; width: 100px; height:40px; border-radius: 15px; margin-bottom: 10px;" type="submit">Edited</button>';
                }
                nameContainer += '</div></div>';

                var article = '<div class="div" id="article_' + post.id + '"><div>';
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
                container += '<p class="comment" onclick=view_comment("'+ post.id  + '")' + '>' + post.comments + ' 💬</p><p class="v_like" onclick="view_likes(\'' + post.id + '\')">📊</p></div>';

                var postElement = '<div id="' + 'post_' + post.id + '">' + (nameContainer + article + media + container) + '</div>'
                $('#comment_block_' + id).append(postElement)
            }
        },
        error: function(xhr, status, error) {
            console.log(error); // handle error response
        }
    });
}

$(document).ready(function(){
    localStorage.setItem("comment_blocks", Array());
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

            var article = '<div class="div" id="article_' + post.id + '"><div>';
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
            container += '<p class="comment" onclick=view_comment("'+ post.id  + '")' + '>' + post.comments + ' 💬</p><p class="v_like" onclick="view_likes(\'' + post.id + '\')">📊</p></div>';
            
            var postElement = '<div id="' + 'post_' + post.id + '">' + (nameContainer + article + media + container) + '</div>'
            $('#body').append(postElement)
            }
    }
})

function delete_post(id){
    let request = new XMLHttpRequest();
    request.open("GET", url + "/delete/" + id)
    request.send()
    $('#post_' + id).remove();
    $('#confirm').hide();
    close_all();
}
function upload_edited(id){
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
            data = JSON.parse(data);
            let new_article = data.article;
            var article = '';
            for (var j = 0; j < new_article.length; j++) {
                var element = new_article[j];
                article += '<' + element.tag + '>' + element.text + '</' + element.tag + '>';
            }
            article += '</div></div>';
            $('#article_' + id).html(article);
            close_all();
        },
        error: function(xhr, status, error) {
            console.log(error); // handle error response
        }
    });
}

function edit_post(id){
    $("#main").hide()
    $('#edit_post').show()
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
                $('#submit_post').off('onclick');
                $('#submit_post').attr('onclick', 'upload_edited("' + id + '")');
            } else {
                $('#edit_article').val(post.raw_article);
                $('#edit_article').attr('readonly', true);
                $('#edit_message').html('<b>Editing Period Has Elapsed</b>');
                $('#submit_post').hide();
            }

            // display the delete post button and prompt
            $('#delete-btn').click(function() {
                $('#confirm').show();
            });
            $('#confirm #btn-yes').off('onclick')
            $('#confirm #btn-yes').attr('onclick', 'delete_post("' + id + '")');
            $('#confirm #btn-no').click(function() {
                $('#confirm').hide();
            });
        } else{
            $("#edit_post").hide();
            $("#main").show();
            alert("An error occurred. Please try again")
        }
    }
}