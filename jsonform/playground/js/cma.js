$('document').ready(function () {
    $.ajax({
        url: 'http://10.2.180.22:5100/data/1',
        dataType: 'json'
    }).done(function (code) {
        $.extend(code, 
            {onSubmit: function (errors, values) {
                
                var action = $('#form').attr('action');

                jQuery.support.cors = true;
                $.ajax({
                  type: 'POST',
                  url: action,
                  data: JSON.stringify(values),
                    contentType: 'application/json; charset=UTF-8',
                    dataType: 'json'
                });
                
                return false;
        }});

        $('#form').jsonForm(code);
        
    }).fail(function (code) {
        $('#result').html('Sorry, I could not retrieve the example!');
    });
});
