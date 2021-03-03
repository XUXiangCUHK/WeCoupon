function reward(obj) {
    var $td = $(obj).parents('tr').children('td');
    let username = $td.eq(0).text();
    var flag = confirm(`Are you sure to reward coupon to ${username}?`);
    if(flag==true){
        $.getJSON(`http://127.0.0.1:5000/add_coupon/${username}`)
        return true;
    }else {
        return false;
    }
}

function stopCollecting(){

}
