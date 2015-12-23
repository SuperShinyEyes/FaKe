function ajax_get_update()
{
  $.get(url, function(results){
    //get the parts of the result you want to update. Just select the needed parts of the response
    var table = $("table", results);
    var page = $(".pagination", results);

    //update the ajax_table_result with the return value
    $('table').html(table);
    console.log("table:", table);
    $('.pagination').html(page);
  }, "html");
}

$(document).on('click', '#previous_page', function(e) {
  console.log("Debuggin...");
    e.preventDefault();
    url = ($( '#previous_page' )[0].href);
    ajax_get_update();
});

$(document).on('click', '#next_page', function(e) {
  console.log("Debuggin...");
    e.preventDefault();
    url = ($( '#next_page' )[0].href);
    ajax_get_update();
});
