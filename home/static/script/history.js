$(function () {
  load_user_urls();
});

function load_user_urls() {
  $("#urls_container").load('/urls/my', function () {
    var Accordion = function (el, multiple) {
      this.el = el || {};
      this.multiple = multiple || false;

      var dropdownlink = this.el.find('.dropdownlink');
      console.log(dropdownlink);
      dropdownlink.on('click',
        { el: this.el, multiple: this.multiple },
        this.dropdown);
    };

    Accordion.prototype.dropdown = function (e) {
      var $el = e.data.el,
        $this = $(this),
        $next = $this.next();
      console.log(5);
      $next.slideToggle();
      $this.parent().toggleClass('open');
      if (!e.data.multiple) {
        $el.find('.submenuItems').not($next).slideUp().parent().removeClass('open');
      }
    }
    var accordion = new Accordion($('.accordion-menu'), false);
  });
}