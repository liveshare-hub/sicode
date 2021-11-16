var superQuery = `query ($kpj: String!) {allKpjs(noKpj:$kpj){
    dataTk{
        nama
    }
}}`


$("#id_kpj").focusout(function() {
    var kpj = $(this).val()
    if(kpj.length !== 11){
        $("#id_nama").val("FORMAT KPJ SALAH!")
    }else if(typeof kpj != 'undefined'){
        $("#id_nama").val("KPJ TIDAK DITEMUKAN!")
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
                $(this).attr("disabled", true);
                var nama = data['data']['allKpjs'][0]['dataTk']['nama']
                $("#id_nama").val(nama)
    
            },
            error:function(err){
                console.log(err)
                $("#id_nama").val("Format KPJ SALAH!!!")
            }
        })
    }
});
// console.log(kpj)