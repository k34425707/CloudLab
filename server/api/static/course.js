//新增課程
function do_addCourse() {
    var token = document.cookie.split(";" )[0];
    var currentCookie = token.split("=")[1];

    $.ajax({
        type: 'POST',
        url: '/api/course',
        headers: {
            'Authorization': 'Bearer ' + currentCookie,
            'Content-Type' : 'application/json' 
        },
        data: JSON.stringify({
            courseName: $('#course').val()
        }),
        success: function(response){
            if (response.success == 't'){
                location.reload();
            }else{
                alert(response.message);
            }
        }
    })
}