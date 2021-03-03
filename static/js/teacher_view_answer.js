function teacherViewAnswer(){
    console.log("yes");
}

function answerTable() {

}

function reward(obj) {
    var $td = $(obj).parents('tr').children('td');
    var username = $td.eq(0).text();
    var flag = confirm('Are you sure to reward coupon to '+username);
    var coupon = {'username': username};
    if(flag==true){
        // not working, want to pass username to backend to add coupon
        // $.ajax({
        //     url: "/teacher_view_answer/<question>",
        //     type: 'POST',
        //     data: JSON.stringify(coupon),})
        //     .done(function(result){
        //         console.log(result)
        //     })
        return true;
    }else {
        return false;
    }
    
    
}