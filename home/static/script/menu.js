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
         display_modal_window();
      }
   });

   btn.addEventListener('click', function () {
      display_modal_window();
   });

   function display_modal_window() {
      console.log(el[0]);
      long_url.reportValidity();
      if (long_url.checkValidity()) {
         if (el[0].value != "") {
            btn_error.style.border = null;
            modal.style.display = "block";
         } else {
            btn_error.style.borderBottom = "3px solid red";
         }
      }
   }

   $.getJSON("/urls/generate", function (data) {
      $("#short_url").val(data['url'])
   });

   span.addEventListener('click', function () {
      modal.style.display = "none";
   });

   window.onclick = function (event) {
      if (event.target == modal) {
         modal.style.display = "none";
      }
   }

   //async check url availability
   $('#short_url').keyup(delay(function (e) {
      var $su = $("#short_url");
      var url = "/" + $su.val();
      $.ajax({
         type: "GET",
         url: url,
         data: {},
         error: function (xhr, statusText, err) {
            // if response code 404 than url is free
            if (xhr.status == 404) {
               $("#short_url")[0].setCustomValidity("");
            }
            else {
               $("#short_url")[0].setCustomValidity("Це скорочення вже зайняте");
            }
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


//delay funcktion runs callback after n ms
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