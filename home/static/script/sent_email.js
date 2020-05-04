$('#short_url').keyup(delay(function (e) {
    var $su = $("#short_url");
    var url = "/FAQ";
    $.ajax({
       type: 'POST',
       dataType: 'json',
       contentType: 'application/json; charset=utf-8',
       url: url,
       data: JSON.stringify({ 'message': $su.val() }),
       success: function (xhr, statusText, err) {
          //xhr have is_valid - bool
          //xhr have status - string (tell what excectly is wrong)
          if (!xhr.status) {
            console.log('Dont sent');
          } 
       },
       error: function (xhr, statusText, err) {
          console.log("Don't work");
       }
    });
 }, 500));
