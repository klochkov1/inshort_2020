/* скрипт по загрузке истории */
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
      var el = e.data.elem;
      var next = $(this).next();
        next.slideToggle();
        el.find('.submenuItems').not(next).slideUp().removeClass('open');
    }
    var history = new History($('.history-items'));
  });
}
