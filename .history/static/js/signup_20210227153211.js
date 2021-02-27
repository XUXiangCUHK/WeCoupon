function test(checkbox) {
    var checkboxes=document.getElementsByName("checkposition");
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}

function processsignupform() {
    alert("!");
    var firstname = document.getElementsById("first_name");
    var lastname = document.getElementsById("last_name");
    var username = document.getElementsById("username");
    var password = document.getElementsById("password");
    var email = document.getElementsById("Email");
    // var position = document.querySelector('.checkposition').checked;

    

}