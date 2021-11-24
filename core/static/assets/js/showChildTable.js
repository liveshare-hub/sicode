/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Full name:</td>'+
            '<td>'+d.name+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extension number:</td>'+
            '<td>'+d.extn+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}


$(document).ready(function() {
    var id = $("#klaim_id").val();
    var table = $("#tableKlaim")
    
    $("#tableKlaim tbody").on('click', 'td.dt-control', function(){
        var tr = $(this).closest('tr');
        console.log(tr)

        // if (row.child.isShown()){
        //     row.child.hide();
        //     tr.removeClass('shown')
        // }
        // else{
        //     $.ajax({
        //         type:'GET',
        //         url:`/detil/tk/${id}`,
        //         dataType:"json",
        //         success:function(data){
        //             console.log(data)
        //         }
        //     })
        // }
    })
})