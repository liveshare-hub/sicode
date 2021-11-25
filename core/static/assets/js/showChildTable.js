/* Formatting function for row details - modify as you need */
var myData;
function GetData(datas) {
    return $.ajax({
        url:`/ajax/tk/${datas}`,
        type:'GET',
        success:function(data){
            myData = data
        }
        
        
    })
}

function format ( d ) {
    // `d` is the original data object for the row
    var items = GetData(d)
    console.log(items['myData'])
    return (
        
        '<table cellpadding="5" cellspacing="0" style="padding-left:50px;">'+
        '<tr>'+
        '<td>Paklaring:</td>'+
        '<td>'+'</td>'+
        '</tr>'+
        '</table>'
        
    )
    
}
//     return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
//         '<tr>'+
//             '<td>Paklaring:</td>'+
//             '<td>'+d.klaim__parklaring+'</td>'+
//         '</tr>'+
//         '<tr>'+
//             '<td>Extension number:</td>'+
//             '<td>'+d['data']+'</td>'+
//         '</tr>'+
//         '<tr>'+
//             '<td>Extra info:</td>'+
//             '<td>And any further details here (images etc)...</td>'+
//         '</tr>'+
//     '</table>';
// }


$(document).ready(function() {
    
    var table = $("#tableKlaim").DataTable({});

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
            row.child( format(tr.data('child-value')) ).show();
            tr.addClass('shown');
        }
    })
})