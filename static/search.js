$(document).ready(function() {
    $('#search').keyup(function() {
        var value = $(this).val();
        if (value.length > 0) {
            FormData = new FormData();
            FormData.append('search', value);
            $.ajax({
                url: `${window.location.origin}/search`,
                type: 'GET',
                data: FormData,
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
