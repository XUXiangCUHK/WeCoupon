function processloginform() {
    var username = document.getElementById("username");
    var password = document.getElementById("password");

    if (username.value == "123" && password.value == "123"){
        window.location.href="../templates/student_main_page.html";
        return false;
    }
}

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');
togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});