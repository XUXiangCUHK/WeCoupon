function test(checkbox) {
    var checkboxes=document.getElementsByName("checkposition");
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}

function processsignupform() {


}