function processloginform() {
    var username = document.getElementById("username");
    var password = document.getElementById("password");

    if (username.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}