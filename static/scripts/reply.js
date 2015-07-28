
// $(".confirm-delete").confirm();

// $(".confirm-delete").confirm({
//
//     title:"Delete confirmation",
//     text: "This is very dangerous, you shouldn't do it! Are you really really sure?",
//     confirm: function(button) {
//         button.fadeOut(2000).fadeIn(2000);
//         alert("You just confirmed.");
//     },
//     cancel: function(button) {
//         button.fadeOut(2000).fadeIn(2000);
//         alert("You aborted the operation.");
//     },
//     confirmButton: "Yes I am",
//     cancelButton: "No"
// });

function ajax_get_update(item)
{
  $.get(url, function(results){
    //get the parts of the result you want to update. Just select the needed parts of the response
    // var reply_form = $("#reply_form", results);
    var reply_form = $("form.post-comment", results);
    // console.log(reply_form);
    var parentTag = $( item).parent().get( 0 ).tagName;
    //update the ajax_table_result with the return value
    $( item).parent().html(reply_form);
  }, "html");
}

$(document).on('click', '.reply', function(e) {
  console.log("Debuggin...");
    e.preventDefault();
    // url = ($( '.comment-reply-link' )[0].href);
    url = $(this).find("a").attr('href');
    // url = "http://127.0.0.1:8000/rango/reply_form"
    console.log(url);
    ajax_get_update(this);
});
