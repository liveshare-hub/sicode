var superQuery = `query ($nik: Int!) {allKpjs(nik:$nik){
    dataTk{
        nama
    }
}}`

var reg = new RegExp('^\\d+$');

$("#id_kpj").focusout(function() {
    var nik = $(this).val()
    var VAL = $(this).val()
    if((kpj.length !== 11) || (!reg.test(VAL))){
        $("#id_hasil").val("FORMAT KPJ SALAH!")
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
                var dataNama = data['data']['allKpjs']
                if(dataNama.length != 0){
                    $("#id_simpan").attr("disabled", false);
                    var nama = dataNama[0]['dataTk']['nama']
                    var nik = dataNama[0]['dataTk']['nik']
                    
                    $("#id_nama").val(nama)
                    $("#id_nik").val(nik.replaceAt(4,"*"))
                    $("#id_kpj").attr("disabled",true).attr("value",kpj)
                }else{
                    $("#id_nama").val("KPJ TIDAK DITEMUKAN")
                    $("#id_nik").val("KPJ TIDAK DITEMUKAN")
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
    $("select").val("")
    $("#id_kpj").attr("disabled", false)
    $("#id_simpan").attr("disabled", false)
})

String.prototype.replaceAt=function(index, char) {
    var a = this.split("");
    for(; index < a.length; index++){
        a[index] = char;
        
        return a.join("");
    }
}
// console.log(kpj)