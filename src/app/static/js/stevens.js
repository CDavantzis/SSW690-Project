function toogleSidebar() {
  $('#stev-sidebar').toggleClass('stev-hide');
  $('#stev-sidebar').toggleClass('stev-show');
  $('#stev-toggle-content-blk').toggleClass('stev-hide');
  $('#stev-toggle-content-blk').toggleClass('stev-show');
}

(function(window) {

  var document = window.document;

  $(document).ready(function() {
    $('#stev-calendar').height($(window).height() - $('#stev-header').height() - $('#stev-content-nav').height() - ($('#calendar').height() -  $('#calendar .fc-scroller').height()) - 3);
    $('#courses-tree').height($(window).height() - $('#stev-header').height() - $('#stev-sidebar-nav-blk').height() - $('#stev-sidebar-ctrl').height() - 3); //1 - border 1px, input border 1px
  });

  $(document).ready(function() {
    $(window).resize(function() {
      $('#stev-calendar').height($(window).height() - $('#stev-header').height() - $('#stev-content-nav').height() - ($('#calendar').height() -  $('#calendar .fc-scroller').height()) - 3);
      $('#courses-tree').height($(window).height() - $('#stev-header').height() - $('#stev-sidebar-nav-blk').height() - $('#stev-sidebar-ctrl').height() - 3); //1 - border 1px, input border 1px
    }).resize();
  });

}(window));
