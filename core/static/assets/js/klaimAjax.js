$(document).ready(function() {
    $("#id_simpan").on("submit",function(){
    //    uploadFile()
       $.ajax({
           method:"POST",
           url:'/klaim/tambah/ajax',
           data:{
               'tipe_klaim':$("#id_tipe_klaim").val(),
               'sebab_klaim':$("#id_sebab_klaim").val(),
               'parklaring': $("#id_parklaring")[0].files[0],
               'no_rek_tk':$("#id_no_rek_tk")[0].files[0],
               'kpj':$("#id_kpj").val(),
               'csrfmiddlewaretoken':$("input[name='csrfmiddlewaretoken']").val()
           },
           contentType:"json",
           success:function(data){
               console.log(data)
           },
           errors:function(err){
               console.log(err)
           }
       })
    })
})

function uploadFile() {
    var data = new FormData()
    data.append("parklaring", $("#id_parklaring")[0].files[0])
    // data.append("surat_meninggal", $("#id_surat_meinggal")[0].files[0])
    // data.append("ktp_ahli_waris", $("#id_ktp_ahli_waris")[0].files[0])
    // data.append("kk_baru", $("#id_kk_baru")[0].files[0])
    // data.append("no_rek_waris", $("#id_no_rek_waris")[0].files[0])
    // data.append("form_I", $("#id_form_I")[0].files[0])
    // data.append("kronologis", $("#id_kronologis")[0].files[0])
    // data.append("ktp_saksi", $("#id_ktp_saksi")[0].files[0])
    // data.append("absen_1", $("#id_absen_1")[0].files[0])
    // data.append("surat_pernyataan", $("#id_surat_pernyataan")[0].files[0])
    // data.append("form_II", $("#id_form_II")[0].files[0])
    // data.append("absensi_2", $("#id_absensi_2")[0].files[0]) 
    // data.append("no_rek_perusahaan", $("#id_no_rek_perusahaan")[0].files[0])
    data.append("no_rek_tk", $("#id_no_rek_tk")[0].files[0])
    // data.append("slip_gaji", $("#id_slip_gaji")[0].files[0])
    data.append("kpj", $("#id_kpj").val())
    data.append("tipe_klaim", $("#id_tipe_klaim").val())
    data.append("sebab_klaim", $("#id_sebab_klaim").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    // console.log($("#id_parklaring")[0].files[0])
    $.ajax({
        method:"POST",
        url:'/klaim/tambah/ajax',
        contentType:false,
        data:data,
        processData:false,
        success:function(res){
            console.log(res)
        },
        errors:function(err){
            console.log(err)
        }
    })
}