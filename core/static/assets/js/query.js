var superQuery = `query ($kpj: String!) {allKpjs(noKpj:$kpj){
    noKpj
    tglKeps
    tglNa
    isAktif
    dataTk{
        nama
    }
}}`


$("#id_kpj").focusout(function() {
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
            console.log(data)
        },
        error:function(err){
            console.log(err)
        }
    })
})
// console.log(kpj)