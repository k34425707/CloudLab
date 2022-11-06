//獲取cookie
var token = document.cookie.split(";" )[0];
var currentCookie = token.split("=")[1];
//sof上傳 - 視覺變化
function do_sofupload() {
    $("#sofupload").empty();
    $("#sofupload").append(SofUploadForm);
}
//監聽sof檔是否上傳
document.getElementById("soffile").addEventListener("change", function() {
    do_sofupload();
})
//pgv上傳 - 視覺變化
function do_pgvupload() {
    $("#pgvupload").empty();
    $("#pgvupload").append(PgvUploadForm);
}
//監聽pgv檔是否上傳
document.getElementById("pgvfile").addEventListener("change", function() {
    console.log(this.value);
    do_pgvupload();
})
//送出上傳內容
function do_pay() {
    let formData = new FormData();
    if( document.getElementById('soffile').files[0] && document.getElementById('pgvfile').files[0]){
    formData.append('sofFile', document.getElementById('soffile').files[0]);
    formData.append('pgvFile', document.getElementById('pgvfile').files[0]);
    formData.append('workType', 0);
    formData.append('sequential',document.querySelector('input[name="sequential"]:checked').value)
    document.getElementById("law").innerHTML="<button class='btn btn-primary' style='color: black; background-color: white; border-color: white;' type='button' disabled><span class='spinner-border spinner-border-sm' style='color: black;' role='status' aria-hidden='true'></span> 燒錄中...</button>"
    document.getElementById("sof").innerHTML="<th><a href='/getfile/sof' download>sof載點</a></th>"
    document.getElementById("pgv").innerHTML="<th><a href='/getfile/pgv' download>pgv載點</a></th>"
    $.ajax({
        type: 'POST',
        url: '/api/ProgrammingRequest',
        headers: {
            'Authorization': 'Bearer ' + currentCookie
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            renewLAW()
        }
    })
}else{
    alert("請將檔案上傳完整")
}
}

function renewLAW(){
    console.log("test");
    $.ajax({
        method: 'GET',
        url:"/remote/getStatus",
        headers: {
            'Authorization': 'Bearer ' + currentCookie
        },
        success: function(response){
            if(response.success=="t" && response.status=="0"){
                document.getElementById("law").innerHTML="<button class='btn btn-primary' style='color: black; background-color: white; border-color: white;' type='button' disabled><span class='spinner-border spinner-border-sm' style='color: black;' role='status' aria-hidden='true'></span> 燒錄中...</button>"
                document.getElementById("time").innerHTML=response.time;
                setTimeout("renewLAW()",1000)
            }else if(response.success=="t" && response.status=="1"){
                document.getElementById("time").innerHTML=response.time;
                document.getElementById("law").innerHTML="<a href='/getfile/law' download>law檔載點</a>"
            }
        }
    });
}

window.onload=function(){
    renewLAW()
}