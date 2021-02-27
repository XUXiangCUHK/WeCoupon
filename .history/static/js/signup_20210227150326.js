function test(checkbox) {
    var checkboxes=document.getElementsByName("check");
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}

function processsignupform() {


}