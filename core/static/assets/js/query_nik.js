var superQuery = `query ($nik: String!) {allTk(nik:$nik){
    nama
    id
}}`

var reg = new RegExp('^\\d+$');

$("#id_NIK").focusout(function() {
    var nik = $(this).val()
    var VAL = $(this).val()
    if((nik.length !== 16) || (!reg.test(VAL))){
        $("#id_hasil").val("FORMAT NIK SALAH!")
    }else{
        $.ajax({
            method:"POST",
            url:"https://sicode.id/graphql",
            contentType:"application/json",
            data: JSON.stringify({
                query:superQuery,
                variables: {"nik":nik}
            }),
            dataType:"json",
            success:function(data){
                var dataNama = data['data']['allTk']
                if(dataNama.length != 0){
                    $("#id_simpan").attr("disabled", false);
                    var nama = dataNama[0]['nama']
                    var nik = dataNama[0]['nik']
                    var id = dataNama[0]['id']
                    
                    $("#id_hasil").val(nama)
                    $("#id_pk").val(id)
                    $("#id_NIK").attr("disabled",true).attr("value",nik)
                }else{
                    $("#id_hasil").val("NIK TIDAK DITEMUKAN")
                    $("#id_simpan").attr("disabled", true)
                    
                }
            },
            error:function(err){
                console.log(err)
                $("#id_nama").val("Format KPJ SALAH!!!")
                $("#id_simpan").attr("disabled", true)
            }
        })
    }
});

function SimpanData() {
    var data = new FormData()
    data.append("nik", $("#id_nik").val())
    data.append("tgl_keps", $("#id_tgl_keps").val())
    data.append("tgl_na", $("#id_tgl_na").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())

    $.ajax({
        method:"POST",
        url:'/tambah/kpj/ajax',
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            $("input").val("")
            $("#id_nik").attr("disabled", false)
            $(".card-body").prepend("<div class='alert alert-success' role='alert'>KPJ Berhasil di Simpan</div>")
            // console.log(data)
        },
        error:function(err){
            console.log(err)
        }
    })
}


$("#clear").click(function(){
    $("input").val("")
    $("#id_NIK").attr("disabled", false)
    $("#id_simpan").attr("disabled", false)
})