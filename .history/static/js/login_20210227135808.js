// function processform(){
//     console.log(document.querySelector("#login"));
//     console.log(document.querySelector("#password"));
    
// }

function processform() {
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
        window.location="student_main_page.html";
    }
}