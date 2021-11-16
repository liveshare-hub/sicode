var superQuery = `query ($kpj: String!) {allKpjs(noKpj:$kpj){
    dataTk{
        nama
    }
}}`

function tc(func, msg){
    msg = msg || "Handler Exception"
    return function(e) {
        try{
            return func(e)
        }
        catch (exc){
            $("#id_nama").val("FORMAT KPJ SALAH!!!");
            throw exc;
        }
    }
}

$("#id_kpj").focusout(tc(function(e) {
    var kpj = $(this).val()
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
}, "FORMAT KPJ SALAH"));
// console.log(kpj)