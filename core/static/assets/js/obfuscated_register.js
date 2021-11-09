var namaNpp = ``


$(document).ready(function() {
  $("div input#id_hasil_npp").hide();
  
  $("#id_npp").on("focusout", function(event){
    $(this).val($(this).val().toUpperCase());
    event.preventDefault();
    $("div input#id_hasil_npp").show();
    
    var value = $(this).val().toUpperCase();
    $.ajax({
      type:'GET',
      url:`/accounts/api/perusahaan?search=${value}`,
      async: true,
      success:function(data){
        if(data.length > 0) {
          
          $("#id_hasil_npp").val(data[0]['nama']).attr("value",`${data[0]['nama']}`)
          $("#id_no_npp").attr("value",`${data[0]['id']}`)
          
        }
        else{
          $("#id_hasil_npp").val("NPP Tidak Ditemukan!!!")
          $("#id_no_npp").attr("value",null)
        }
      },
      error: function(xhr, status, error){
        var err = JSON.parse(xhr.responseText);
        
        alert(err)
      }
    });
  
  $(document).on('submit', '#id_form',function(e){
    e.preventDefault();
    
    $.ajax({
      type:'POST',
      url:"/accounts/register/ajax",
      async:true,
      data: {
        username:$("#id_username").val(),
        email:$("#id_email").val(),
        password1:$("#id_password1").val(),
        password2:$("#id_password2").val(),
        no_npp:$("#id_no_npp").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        dataType: "json",
      },
      success: function(data){
        
        $("p.text-muted").html(data.msg);
        $("input.form-control").val("");
        $("div input#id_hasil_npp").hide();
      },
      error:function(err){
        console.log(err)
      }
    });
  });
});
})
