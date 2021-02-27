function test(checkbox) {
    var checkboxes=document.getElementsByName("checkposition");
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}

function processsignupform() {
    var firstname = document.getElementById("first_name");
    var lastname = document.getElementById("last_name");
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var email = document.getElementById("email");
    var position = document.querySelector('.checkposition').checked; //student return true, professor return false

    
}