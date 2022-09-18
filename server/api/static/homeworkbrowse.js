var token = document.cookie.split(";" )[0];
var currentCookie = token.split("=")[1];
//新增作業
function do_addHomework() {
    $.ajax({
        type: 'POST',
        url: '/api/homework',
        headers: {
            'Authorization': 'Bearer ' + currentCookie,
            'Content-Type' : 'application/json' 
        },
        data: JSON.stringify({
            homeworkInfo: $('#homeworkInfo').val(),
            homeworkName: $('#homeworkName').val(),
            courseName: $('#courseName').text().split(":" )[1]
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
//新增學生
function do_addMember() {
    let formData = new FormData();
    formData.append('file', document.getElementById('csvFile').files[0]);
    formData.append('courseName', $('#courseName').text().split(":" )[1]);

    $.ajax({
        type: 'POST',
        url: '/api/member',
        headers: {
            'Authorization': 'Bearer ' + currentCookie
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){
            if (response.success=='t') {
                location.reload();
            }
            else {
                alert(response.message);
            }
        }
    })
}

//顯示新增作業視窗
function show_Newhomework_Dialog() {
    document.getElementsByClassName('dialog')[0].showModal();
}
//提交新增作業內容
function summit_NewHomework() {
    do_addHomework();
    document.getElementsByClassName('dialog')[0].close();
    location.reload();
}
//關閉新增作業視窗
function newhomework_Close() {
    location.reload();
}

//顯示新增學生視窗
function show_Member_Dialog() {
    document.getElementById('members').showModal();
}
//提交新增學生內容
function summit_Member() {
    do_addMember();
}
//關閉新增學生視窗
function member_Close() {
    document.getElementById('members').close();
}
//刪除學生
function delete_member(userID) {
    $.ajax({
        url:"/api/member",
        method:"delete",
        headers: {
            'Authorization': 'Bearer ' + currentCookie,
        },
        data:{
            courseName: $('#courseName').text().split(":")[1],
            userID:userID
        },
        success:function (response){
            var select="member_"+userID;
            document.getElementById(select).innerHTML=""

        }
    })
}
//解散課程
function delete_Course_Check() {
    var dccMessage = confirm("確定要解散課程 ? ");
    if (dccMessage==true) {
        $.ajax({
            type: 'delete',
            url: '/api/course',
            headers: {
                'Authorization': 'Bearer ' + currentCookie,
                "content-Type":"application/json"
            },
            data: JSON.stringify({
                courseName: $('#courseName').text().split(":")[1]
            }),
            success: function(response) {
                if (response.success == 't'){
                    alert("解散成功");
                    window.location.href = '/course';
                }
                else {
                    alert("解散失敗");
                }
            }
        })
    }
    else {
        
    }
}