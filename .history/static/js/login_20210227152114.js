// function processform(){
//     console.log(document.querySelector("#login"));
//     console.log(document.querySelector("#password"));
    
// }

function showPwd(id, el) {
    let x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
        el.className = 'fa fa-eye-slash showpwd';
    } else {
        x.type = "password";
        el.className = 'fa fa-eye showpwd';
    } 
}

function processloginform() {
    // var username = document.querySelector("#login");
    // var password = document.querySelector("#password");
    var username = document.getElementById("username");
    var password = document.getElementById("password");


    if (username.value == ""){
        alert("please input username!");
    }
    else if (password.value == ""){
        alert("please input password!");
    }else if (username.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}