var modal = document.querySelector(".modal");
var btn = document.querySelector(".btn_modal_window");
console.log(btn);
var span = document.querySelector(".close_modal_window");


console.log(btn);
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