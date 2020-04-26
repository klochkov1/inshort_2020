var modal = document.querySelector(".modal");
var btn = document.querySelector(".btn_modal_window");
console.log(btn);
var span = document.querySelector(".close_modal_window");
var button = document.getElementById('userButton');
button.addEventListener('click', function () {
  //нашли наш контейнер
  var ta = document.getElementById('cont'); 
  //производим его выделение
  var range = document.createRange();
  range.selectNode(ta); 
  window.getSelection().addRange(range); 
 
  //пытаемся скопировать текст в буфер обмена
  try { 
    document.execCommand('copy'); 
  } catch(err) { 
    console.log('Can`t copy, boss'); 
  } 
  //очистим выделение текста, чтобы пользователь "не парился"
  window.getSelection().removeAllRanges();
});
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