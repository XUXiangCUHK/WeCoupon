function test() {
    if (document.getElementById("position1").checked){
        document.getElementById("sid").style.display = 'inline-block';
        document.getElementById("sid").setAttribute("required", "");
    }else{
        document.getElementById("sid").style.display = 'none';
        document.getElementById("sid").removeAttribute("required");
    }
}

function processsignupform() {
    var sid = document.getElementById("sid");
    var firstname = document.getElementById("first_name");
    var lastname = document.getElementById("last_name");
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var email = document.getElementById("email");
    var student = document.getElementById("position1").checked;
    var instructor = document.getElementById("position2").checked;

}