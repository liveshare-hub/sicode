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
                $(this).attr("disabled", true);
                var dataNama = data['data']['allKpjs']
                console.log(dataNama)
            },
            error:function(err){
                console.log(err)
                $("#id_nama").val("Format KPJ SALAH!!!")
            }
        })
    }
});
// console.log(kpj)