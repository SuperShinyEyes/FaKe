<script type="text/javascript">
function ajax_get_update()
    {
       $.get(url, function(results){
          //get the parts of the result you want to update. Just select the needed parts of the response
          var table = $("table", results);
          var span = $("span.step-links", results);

          //update the ajax_table_result with the return value
          $('#ajax_table_result').html(table);
          $('.step-links').html(span);
        }, "html");
    }

//bind the corresponding links in your document to the ajax get function
$( document ).ready( function() {
    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #prev' )[0].href);
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #next' )[0].href);
        ajax_get_update();

    });
});

//since the links are reloaded we have to bind the links again
//to the actions
$( document ).ajaxStop( function() {
    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #prev' )[0].href);
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #next' )[0].href);
        ajax_get_update();
    });
});
</script>
