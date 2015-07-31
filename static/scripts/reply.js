// This is for Asynchronous reply forms.
function ajax_get_update(item)
{
  $.get(url, function(results){
    //get the parts of the result you want to update. Just select the needed parts of the response

    var reply_form = $("form.post-comment", results);
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
    console.log(url);
    ajax_get_update(this);
});
