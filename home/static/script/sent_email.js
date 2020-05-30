$('#sent_email').click(delay(function (e) {
    var $su = $("#body_messege");
    var url = "/FAQ";
    console.log('good');
    $.ajax({
       type: 'POST',
       dataType: 'json',
       contentType: 'application/json; charset=utf-8',
       url: url,
       data: JSON.stringify({ 'message': "jira" }),
       success: function (xhr, statusText, err) {
         console.log('good');
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
