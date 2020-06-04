/* скрипт по открытию окна для добавление url */
window.onload = function () {
   var modal = document.querySelector(".window");
   var btn = document.querySelector(".btn_modal_window");
   var long_url = document.getElementById('long_url');
   //open modal window when Enter pressed
   long_url.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
         event.preventDefault();
         if (event.target.checkValidity()) {
            modal.style.display = "block";
         }
      }
   });
   /* добавление  ошибки,
     потому что при типе кнопке button пропадает возможность валидации с фронта */
   btn.addEventListener('click', function (e) {
      var inp = document.getElementById('long_url');
      if (inp.checkValidity()) {
         modal.style.display = "block";
      }
      else {
         inp.reportValidity();
      }
   })
   $.getJSON("/urls/generate", function (data) {
      $("#short_url").val(data['url'])
   });
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
            } else {
               $("#short_url")[0].setCustomValidity(xhr.status);
            }
         },
         error: function (xhr, statusText, err) {
            console.log("connection error");
         }
      });
   }, 500));
}
/* на копирование url */
function copyToClipboard(elem) {
   var element = document.getElementById(elem);
   var new_range = document.createRange();
   new_range.selectNode(element);
   window.getSelection().addRange(new_range);
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
