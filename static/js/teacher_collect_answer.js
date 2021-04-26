function reward(obj, userid, username, q_id) {
    var flag = confirm(`Are you sure to reward coupon to ${username}?`);
    if(flag==true){
        $.getJSON(`../add_coupon/${userid}&${q_id}`)
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

function start_update(q_id){
    setInterval( function(q_id) {
        $.ajax({
            url:`/update_answer/${q_id}`,
            type:"GET",
            dataType:"JSON",
            success:function(answer_list){
                $('#answerList').empty();
                $.each(answer_list, function (k, v) {
                    var row = "";
                    row += "<tr><td style='width:20%'>"+v.answer_user+
                    "</td>"+"<td style='width:80%'>"+v.answer_content
                    ;
                    $('#answerList').append(row);
                })
            },
        })
    }, 3000, q_id);
}