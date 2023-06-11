$(document).ready(function() {
    $('#search').keyup(function() {
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
                    console.log(data);
                }
            });
            console.log("Done")
        } else {
            console.log("Empty")
        }
    });
});
