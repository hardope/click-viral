$(document).ready(function() {
    $('#search').keyup(function() {
        var value = $(this).val();
        if (value.length > 0) {
            formData = new FormData();
            formData.append('search', value);
            console.log(formData)
            $.ajax({
                url: `${window.location.origin}/search`,
                type: 'GET',
                data: formData,
                dataType: 'text',
                contentType: false,
                processData: false,
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
