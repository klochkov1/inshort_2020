$(function () {
  var Accordion = function (el, multiple) {
    this.el = el || {};
    this.multiple = multiple || false;

    var dropdownlink = this.el.find('.dropdownlink');
    dropdownlink.on('click',
      { el: this.el, multiple: this.multiple },
      this.dropdown);
  };

  Accordion.prototype.dropdown = function (e) {
    var $el = e.data.el,
      $this = $(this),
      $next = $this.next();

    $next.slideToggle();
    $this.parent().toggleClass('open');

    if (!e.data.multiple) {
      $el.find('.submenuItems').not($next).slideUp().parent().removeClass('open');
    }
  }
  var accordion = new Accordion($('.accordion-menu'), false);
  
  load_user_urls()
});
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

function load_user_urls() {
  $("#urls_container").load('/urls/my')
}