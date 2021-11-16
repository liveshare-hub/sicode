var superQuery = `query ($kpj: String!) {allKpjs(noKpj:$kpj){
    dataTk{
        nama
        nik
    }
}}`


$("#id_kpj").focusout(function() {
    var kpj = $(this).val()
    if(kpj.length !== 11){
        $("#id_nama").val("FORMAT KPJ SALAH!")
    }else{
        $.ajax({
            method:"POST",
            url:"https://sicode.id/graphql",
            contentType:"application/json",
            data: JSON.stringify({
                query:superQuery,
                variables: {"kpj":kpj}
            }),
            success:function(data){
                var dataNama = data['data']['allKpjs']
                if(dataNama.length != 0){
                    // $("#id_kpj").attr("disabled", true);
                    var nama = dataNama[0]['dataTk']['nama']
                    var nik = dataNama[0]['dataTk']['nik']
                    $("#id_nama").val(nama)
                    $("#id_nik").val(nik)
                }else{
                    $("#id_nama").val("KPJ TIDAK DITEMUKAN")
                    $("#id_nik").val("KPJ TIDAK DITEMUKAN")
                }
            },
            error:function(err){
                console.log(err)
                $("#id_nama").val("Format KPJ SALAH!!!")
            }
        })
    }
});
// console.log(kpj)