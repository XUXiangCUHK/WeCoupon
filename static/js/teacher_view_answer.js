function reward(obj, userid, username, q_id, a_id) {
    var flag = confirm(`Are you sure to reward coupon to ${username}?`);
    if(flag==true){
        $.getJSON(`http://127.0.0.1:5000/add_coupon/${userid}&${q_id}&${a_id}`)
        .always(function(){
            console.log("success");
            document.getElementById(a_id).setAttribute("value", "Rewarded");
            document.getElementById(a_id).setAttribute("onclick", "");
            document.getElementById(a_id).setAttribute("class", "btn btn-warning");
            $(obj).attr('disabled', 'true');
            $(obj).attr('value', 'Rewarded');
        })
        
        return true;
    }else {
        return false;
    }
}