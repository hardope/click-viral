$(document).ready(function() {
    $('#search').keyup(function() {
        $('#body_block').hide();
        $('#search_result').show();
        var value = $(this).val();
        if (value.length > 0) {
            formData = new FormData();
            formData.append('search', value);
            $.ajax({
                url: `${window.location.origin}/search`,
                type: 'POST',
                data: formData,
                dataType: 'text',
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(data) {
                    for (let obj of JSON.parse(data)) {
                        /* Display Users */
                        var v_cont = document.createElement('div')
                        v_cont.setAttribute('class', 'v_cont')
                        var name_link = document.createElement('a')
                        name_link.setAttribute('style', 'display: inline-flex;')
                        pic = document.createElement('img')
                        pic.setAttribute('src', '/static/favicon.ico')
                        pic.setAttribute('style', 'width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 30px')
                        name_link.append(pic)
                        var name = document.createElement('div');
                        name.setAttribute('class', 'p')
                        name.textContent = obj;
                        name_link.setAttribute('href', "/profile/" + obj)
                        name.setAttribute('style', 'margin-left: 10px; margin-top: 30px;')
                        name_link.append(name)
                        v_cont.append(name_link)
                        $('#search_result').append(v_cont)
        
                        a+=1
                    }
                    /* If there are no matches */
                    if (a == 0) {
                        $('#search_result').html('<p style="text-align: center; margin-top: 100px><b>No Match</b></p>');
                    }
                }
            });
            console.log("Done")
        } else {
            $('#search_result').hide();
            $('#search_result').empty();
            $('#body_block').show();
        }
    });
});
