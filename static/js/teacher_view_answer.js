function reward(obj, userid, username) {
    // var $td = $(obj).parents('tr').children('td');
    // let username = $td.eq(1).text();
    // let userid = $td.eq(0).text();
    var flag = confirm(`Are you sure to reward coupon to ${username}?`);
    if(flag==true){
        $.getJSON(`http://127.0.0.1:5000/add_coupon/${userid}`)
        .always(function(){
            console.log("success");
            $(obj).attr('disabled', 'true');
            $(obj).attr('value', 'Rewarded');
        })
        
        return true;
    }else {
        return false;
    }
}

function stopCollecting(question_id){
    // set the status of answer into stop collecting
    console.log(question_id)
    $.get(`http://127.0.0.1:5000/stopcollection`, {'qid':question_id})
}
