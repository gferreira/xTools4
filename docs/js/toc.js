$(function(){
  $('#markdown-toc').click(function(e){
    $(this).children('li').toggle();
    $(this).toggleClass('toc-collapse');
  });
  $("#markdown-toc li").click(function(e){
    e.stopPropagation();
  });
});
// add header links
// $(document).ready(function () {
//   $("h2, h3, h4, h5, h6").each(function() {
//     el = $(this)
//     id = el.attr('id')
//     icon = '<span></span>'
//     if (id) {
//       el.append($("<a />").addClass("header-link").attr("href", "#" + id).html(icon));
//     }
//   })
//   // initialize tooltips
//   var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//   var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//     return new bootstrap.Tooltip(tooltipTriggerEl)
//   })
// })
