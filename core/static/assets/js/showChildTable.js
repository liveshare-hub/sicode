/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Paklaring:</td>'+
            '<td>'+d['data']+'</td>'+
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
    var table = $("#tableKlaim").DataTable({});

    $("#tableKlaim tbody").on('click', 'td.details-control', function(){
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        $.ajax({
            type:'GET',
            url:`/ajax/tk/${id}`,
            dataType:"json",
            success:function(data){
                console.log(data)
                if (row.child.isShown()){
                    row.child.hide();
                    tr.removeClass('shown')
                }
                else{
                  row.child(format(row.data('child-value'))).show();
                  tr.addClass('shown');
                }
            }
        })
        
    })
})