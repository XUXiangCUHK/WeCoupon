// function processform(){
//     console.log(document.querySelector("#login"));
//     console.log(document.querySelector("#password"));
    
// }

function processloginform() {
    // var username = document.querySelector("#login");
    // var password = document.querySelector("#password");
    var username = document.getElementById("username");
    var password = document.getElementById("password");

    if (username.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}