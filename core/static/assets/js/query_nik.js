var superQuery = `query ($nik: String!) {allTk(nik:$nik){
    dataTk{
        nama
    }
}}`

var reg = new RegExp('^\\d+$');

$("#id_NIK").focusout(function() {
    console.log($("#id_NIK").val())
    var nik = $(this).val()
    var VAL = $(this).val()
    console.log(nik)
    if((nik.length !== 11) || (!reg.test(VAL))){
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
                console.log(data)
                var dataNama = data['data']['allTk']
                if(dataNama.length != 0){
                    $("#id_simpan").attr("disabled", false);
                    var nama = dataNama[0]['dataTk']['nama']
                    var nik = dataNama[0]['dataTk']['nik']
                    
                    $("#id_hasil").val(nama)
                    $("#id_nik").attr("disabled",true).attr("value",nik)
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

$("#clear").click(function(){
    $("input").val("")
    $("#id_simpan").attr("disabled", false)
})