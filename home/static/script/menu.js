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

document.getElementById("copyButton").addEventListener("click", function() {
  copyToClipboard(document.getElementById("copyTarget"));
});

function copyToClipboard(elem) {
  var targetId = "_hiddenCopyText_";
  var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
  var origSelectionStart, origSelectionEnd;
  if (isInput) {

      target = elem;
      origSelectionStart = elem.selectionStart;
      origSelectionEnd = elem.selectionEnd;
  } else {

      target = document.getElementById(targetId);
      if (!target) {
          var target = document.createElement("textarea");
          target.style.position = "absolute";
          target.style.left = "-9999px";
          target.style.top = "0";
          target.id = targetId;
          document.body.appendChild(target);
      }
      target.textContent = elem.textContent;
  }
  
  target.focus();
  target.setSelectionRange(0, target.value.length);
  

  var succeed;
  try {
      succeed = document.execCommand("copy");
  } catch(e) {
      succeed = false;
  }
  return succeed;
}