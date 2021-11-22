$(document).ready(function() {
    $("#id_simpan").on("click",function(){
       uploadFile()
    })
})

function uploadFile() {
    var data = new FormData()
    data.append("parklaring", $("#id_parklaring")[0].files[0])
    data.append("no_rek_tk", $("#id_no_rek_tk")[0].files[0])
    data.append("kpj", $("#id_kpj").val())
    data.append("tipe_klaim", $("#id_tipe_klaim").val())
    data.append("sebab_klaim", $("#id_sebab_klaim").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    // console.log($("#id_parklaring")[0].files[0])
    $.ajax({
        method:"POST",
        url:'/klaim/tambah/ajax',
        contentType:"json",
        data:data,
        success:function(res){
            console.log(res)
        },
        errors:function(err){
            console.log(err)
        }
    })
}