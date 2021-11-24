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
        "ajax":$.ajax({
            type:'GET',
            url:`/ajax/tk/${id}`,
            dataType:"json",
            success:function(res){
                console.log(res)
            }
        }),
        "columns":[
            {
                "data":res['data'][0]['klaim__parklaring'],
                "data":res['data'][0]['klaim__no_rek_tk']
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