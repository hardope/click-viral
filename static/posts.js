let url = window.location.origin
let c_blocks = []

function close_comment() {
    $('#comment_block_' + c_blocks[c_blocks.length - 1]).remove();
    c_blocks.splice(c_blocks.length - 1);
    if (c_blocks.length > 0){
        $('#comment_block_' + c_blocks[c_blocks.length - 1]).show();
    } else {
        close_all();
    }
}

function submit_comment (id){
    var formData = new FormData(); // create new FormData object
    
    // add text data to FormData object
    var article = $('#comment_article_' + id).val();
    formData.append('article', article);

    // add file data to FormData object
    var media = $('#comment_media_' + id)[0].files[0];
    formData.append('media', media);

    // send AJAX request to Django app
    $("#upload_message").html("Uploading Your Post Please wait...")
    $.ajax({
        url: window.location.origin + '/comment/' + id,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(data) {
            // handle successful response
            add_post(data.id, "#comment_posts_" + id)
        },
        error: function(xhr, status, error) {
            alert("Unable To upload Your post, Please Check Your Internet Connection"); // handle error response
        }
    });
}

function view_comment(id){
    $('#main').hide();
    $('#comment_block').show();
    if (c_blocks.length > 0){
        last = c_blocks[c_blocks.length - 1];
        $('#comment_block_' + last).hide();
    }
    c_blocks.push(id);
    new_block = '<div id="comment_block_' + id + '"><button onclick="close_comment()" style="font-size: 60px; color: black; border: 0ch; margin-bottom: 2%; border-radius: 10px 10px 10px 10px;  width: 200px; height: 50px; margin-left:60px;">Cancel</button></div>';
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

            var upload_comment = '<div id="new_comment_form_' + post.id + '"><center><h1>New Comment</h1><center><b id="message"></b></center><textarea id="comment_article_' + post.id + '" maxlength="1000" style="width:500px; padding: 10px; height: 200px; border-radius: 10px;"></textarea><input type="file" id="comment_media_' + post.id + '" name="media" accept="image/*,video/mp4" value="" hidden><div id="label_cont"><label for="media" id="media_label">Upload Media &#128206;</label></div><button onclick=submit_comment("' + post.id + '") id="button" data-mdb-ripple-color="dark" style="font-size: 60px; color: black; border: 0ch; margin-bottom: 2%; border-radius: 10px 10px 10px 10px;  width: 200px; height: 50px;">Comment</button></center></div>'
            $('#comment_block_' + id).append(upload_comment)

            var comments_posts = '<div id="comment_posts_' + post.id + '"></div>'

            console.log(data.comments.length)

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
                comments_posts+=(postElement)
                $('#comment_block_' + id).append(comments_posts)
            }
        },
        error: function(xhr, status, error) {
            console.log(error); // handle error response
        }
    });
}

$(document).ready(function(){
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