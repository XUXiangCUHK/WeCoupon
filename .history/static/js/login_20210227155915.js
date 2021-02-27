function processloginform() {
    var username = document.getElementById("username");
    var password = document.getElementById("password");

    if (username.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}

function mouseoverPass(obj) {
    var obj = document.getElementById('myPassword');
    obj.type = "text";
}

function mouseoutPass(obj) {
    var obj = document.getElementById('myPassword');
    obj.type = "password";
}

$(".toggle-password").click(function() {
    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
 });