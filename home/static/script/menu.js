
window.onload = function () {
   var modal = document.querySelector(".modal");
   var btn = document.querySelector(".btn_modal_window");
   var span = document.querySelector(".close_modal_window");
   var el = document.getElementsByName('long_url');
   var long_url = document.getElementById('long_url');
   var btn_error = document.getElementsByName('long_url')[0];

   long_url.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
         event.preventDefault();
         if (el[0].value != "") {
            btn_error.style.border = null;
            modal.style.display = "block";
         } else {
            btn_error.style.borderBottom = "3px solid red";
         }
      }
   });
   btn.addEventListener('click', function () {
      if (el[0].value != "") {
         btn_error.style.border = null;
         modal.style.display = "block";
      } else {
         btn_error.style.borderBottom = "3px solid red";
      }
   })

   $.getJSON("/urls/generate", function (data) {
      $("#short_url").val(data['url'])
   });

   span.addEventListener('click', function () {
      modal.style.display = "none";
   })

   window.onclick = function (event) {
      if (event.target == modal) {
         modal.style.display = "none";
      }
   }

   //async check url availability
   $('#short_url').keyup(delay(function (e) {
      var $su = $("#short_url");
      var url = "/urls/check/";
      $.ajax({
         type: 'POST',
         dataType: 'json',
         contentType: 'application/json; charset=utf-8',
         url: url,
         data: JSON.stringify({ 'url': $su.val() }),
         success: function (xhr, statusText, err) {
            //xhr have is_valid - bool
            //xhr have status - string (tell what excectly is wrong)
            if (xhr.is_valid) {
               $("#short_url")[0].setCustomValidity("");
            }else{
               $("#short_url")[0].setCustomValidity(xhr.status);
            }
         },
         error: function (xhr, statusText, err) {
            console.log("connection error");
         }
      });
   }, 500));
}
function copyToClipboard(elem) {
   var ta = document.getElementById(elem);
   var range = document.createRange();
   range.selectNode(ta);
   window.getSelection().addRange(range);
   document.execCommand('copy');
   window.getSelection().removeAllRanges();
}

function delay(callback, ms) {
   var timer = 0;
   return function () {
      var context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
         callback.apply(context, args);
      }, ms || 0);
   };
}
