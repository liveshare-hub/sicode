/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Paklaring:</td>'+
            '<td>'+d['data'][0]+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extension number:</td>'+
            '<td>'+d['data']+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}


$(document).ready(function() {
    var id = $("#klaim_id").val();
    var table = $("#tableKlaim").DataTable({
        "ajax":`{% url 'detil-tk-ajax' ${id} %}`,
        "columns":[
            {
                "data":null
            },
            {
                "data":"klaim__parklaring",
                "data":"klaim__parklaring"
            }
        ],
        "order":[[1, 'asc']]

    });

    $("#tableKlaim tbody").on('click', 'td.details-control', function(){
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    })
})