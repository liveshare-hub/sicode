var superQuery = `query ($kpj: String!) {allKpjs(noKpj:$kpj){
    dataTk{
        nama
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
                    $(this).attr(disabled, true);
                    var nama = dataNama[0]['dataTk']['nama']
                    $("#id_nama").val(nama)
                }else{
                    $(this).attr("disabled", false);
                    $("#id_nama").val("KPJ TIDAK DITEMUKAN")
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