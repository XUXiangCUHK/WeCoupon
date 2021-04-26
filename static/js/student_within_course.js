var text;
function display() {
    document.getElementById('contes').style.display = 'block';
}
function show() {
    var allfullTextByClass = document.getElementsByClassName('fullText');
    var allsubTextByClass = document.getElementsByClassName('subText');
    var allbtnByClass = document.getElementsByClassName('btn');
    for(var i=0, len=allfullTextByClass.length|0; i<len; i=i+1|0){
        text = allfullTextByClass[i].innerHTML;
        allfullTextByClass[i].innerHTML = "";
        allsubTextByClass[i].style.float = "left";
        allbtnByClass[i].style.float = "left";
        if (text.length > 20) {
            allsubTextByClass[i].innerHTML = text.substring(0, 20);
            allbtnByClass[i].innerHTML = "...open";
        } else {
            allsubTextByClass[i].innerHTML = text;
            allbtnByClass[i].innerHTML = "...open";
        }
    } 
}

function change(el) {
    var bro = el.parentNode.children
    var t = bro[2]
    var tt = bro[1];
    // 从后端拿
    text = {text};
    
    if (t.innerHTML == "...open") {
        tt.innerHTML = text;
        t.innerHTML = "close"
    } else {
        tt.innerHTML = text.substring(0, 20);
        t.innerHTML = "...open"
    }
}
function submit_ans(ans){
    var sibling = ans.parentNode.children;
    var form = sibling[0].children;
    var ans = form[1].innerHTML;
    // return answer 给db存着
}
show();
