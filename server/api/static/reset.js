function reset_password(user){
    $.ajax({
        method:"POST",
        url:"api/do_resetPassword",
        headers:{
            "Authorization":"Bearer "+document.location.search.split("=")[1]
        },
        data:{
            userID:user["userID"],
            userName:user["userName"],
            newPassword:$("#newPassword").val()
        },
        success: function (response){
            if(response.success=="t"){
                alert(response.message);
                window.location.href="/";
            }else{
                alert(response.message);
            }
        }
    }

    )
}