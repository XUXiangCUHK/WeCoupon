function reward(obj, userid, username, q_id) {
    // var $td = $(obj).parents('tr').children('td');
    // let username = $td.eq(1).text();
    // let userid = $td.eq(0).text();
    var flag = confirm(`Are you sure to reward coupon to ${username}?`);
    if(flag==true){
        $.getJSON(`http://127.0.0.1:5000/add_coupon/${userid}&${q_id}`)
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

// function update_answer() {
//     $.ajax({
//         url:"/update_answer",
//         type:"GET",
//         dataType:"JSON",
//         success:function(answer_list){
//             $('#answerList').empty();
//             $.each(answer_list, function (k, v) {
//                 var row = "";
//                 row += "<tr><td style='width:15%'>"+v.answer_user+
//                 "</td>"+"<td style='width:60%'>"+v.answer_content+ 
//                 "</td>"+"<td style='width:25%'>"+
//                 `<input type='button' class='btn btn-primary' value='Reward' onclick="reward(this, '${v.answer_userid}' , '${v.answer_user}' )"></input></td>`+
//                 +"</tr>";
//                 $('#answerList').append(row);
//                 // answer_userid, answer_user, answer_content
//             })
//         }
//     })
// }

// setInterval(update_answer,3000); 
