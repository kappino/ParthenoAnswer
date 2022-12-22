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
        url: '/render_query_table',
        data: {
            title: $("#title").val(),
            subject: $("#subject").val()
        },
        success: (data) => {
            $(jQueryTableIndex).html(data);
        },
        error: function(error) {
            console.log("Here is the error res: " + JSON.stringify(error));
        }
    })
}