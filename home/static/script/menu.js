var modal = document.querySelector(".modal");
var btn = document.querySelector(".btn_modal_window");

var span = document.querySelector(".close_modal_window");

btn.addEventListener('click', function () {
   modal.style.display = "block";
})

span.addEventListener('click', function () {
   modal.style.display = "none";
})

window.onclick = function (event) {
   if (event.target == modal) {
       modal.style.display = "none";
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