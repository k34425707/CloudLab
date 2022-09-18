//登入
function do_login() {
    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {
            uId: $('#username'). val(),
            uPassword: $("#password"). val()
        },
        success: function(response) {
            console.log(response);
            if (response.success == 't'){
                document.cookie = ("access_token_cookie=" + response.jwt_token);
                window.location.href = '/remote';
            }
            else {
                alert("登入失敗");
            }
        }
    })
}

//登出
function do_logout() {
    document.cookie = "access_token_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = '/'
}

//更改密碼
function password_Change_Check() {
    var pccMessage = confirm("確定要更改密碼 ? ");
    if (pccMessage==true) {
        $.ajax({
            method:"POST",
            url:"/api/resetpassword",
            headers:{
                "Authorization":"Bearer "+currentCookie
            },
            success: function(response){
                alert("go to check email!")
            }
        })
    }
    else {

    }
}