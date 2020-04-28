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
      if (el[0].value != "") {
         btn_error.style.border = null;
         modal.style.display = "block";
      } else {
         btn_error.style.borderBottom = "3px solid red";
      }
   }

   span.addEventListener('click', function () {
      modal.style.display = "none";
   });

   window.onclick = function (event) {
      if (event.target == modal) {
         modal.style.display = "none";
      }
   }
}

function copyToClipboard(elem) {
   var ta = document.getElementById(elem);
   var range = document.createRange();
   range.selectNode(ta);
   window.getSelection().addRange(range);
   document.execCommand('copy');
   window.getSelection().removeAllRanges();
}