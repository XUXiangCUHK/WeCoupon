function processloginform() {
    var email = document.getElementById("email");
    var password = document.getElementById("password");

    if (email.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}