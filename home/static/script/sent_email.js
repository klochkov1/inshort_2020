
$('#sent_email').click(delay(function (e) {
   console.log(5);
   
    var su = document.getElementById('sent_messege');
    if(su.checkValidity())
    {
    var url = "/FAQ/";
    console.log(su);
    console.log('good');
    $.ajax({
       type: 'POST',
       dataType: 'json',
       contentType: 'application/json; charset=utf-8',
       url: url,
       data: JSON.stringify({ 'message': su.value }),
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
   }else{
      su.reportValidity();
   }
 }, 500));
