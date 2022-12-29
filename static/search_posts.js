$(document).ready(function () {
    renderQueryTableInElement('#table');
    $('#search').submit(function (e) {
        e.preventDefault();
        renderQueryTableInElement('#table');
    });
});
 
function renderQueryTableInElement(jQueryTableIndex) {
    $.ajax({
        type: 'GET',
        url: '/search',
        data: {
            search: $("#search").val(),
            id_search: $("#id_search").val()
        },
        success: (data) => {
            $(jQueryTableIndex).html(data);
        },
        error: function(error) {
            console.log("Here is the error res: " + JSON.stringify(error));
        }
    })
}