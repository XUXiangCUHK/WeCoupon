function test(obj) {
    var a=document.getElementById("position");
    for (var i=1;i<a.length;i++){
        a[i].checked=false;
    }
    if(obj.checked==true){
        obj.checked=false;
    }else{
        obj.checked=true;
    }    
}

function processsignupform() {


}