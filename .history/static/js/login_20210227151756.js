// function processform(){
//     console.log(document.querySelector("#login"));
//     console.log(document.querySelector("#password"));
    
// }

$(".toggle-password").click(function() {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
    });

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