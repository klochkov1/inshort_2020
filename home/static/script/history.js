$(function () {
  load_user_urls();
  
});
function load_user_urls() {
  $("#urls_container").load('/urls/my', function () {
    var History = function (elem) {
      this.elem = elem;
      var dropdownlink = this.elem.find('.dropdownlink');
      console.log(dropdownlink);
      dropdownlink.on(
        'click',
        { 
          elem: this.elem, 
        },
        this.dropdown);
    };

    History.prototype.dropdown = function (e) {
      var $el = e.data.elem,
        $this = $(this),
        $next = $this.next();
      console.log(5);
      $next.slideToggle();
      $this.parent().toggleClass('open');
        $el.find('.submenuItems').not($next).slideUp().parent().removeClass('open');
    }
    var history = new History($('.history-items'));
  });
}
