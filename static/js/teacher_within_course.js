function display() {
  document.getElementById('contes').style.display = 'block';
}

var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})


function useCoupon(user_id, courseid){
  console.log(user_id, courseid)
  var flag = confirm(`Are you sure to use 1 coupon?`);
  if(flag==true){
    $.getJSON(`http://127.0.0.1:5000/use_coupon/${user_id}&${courseid}`)
    .always(function(){
        console.log("success");
    })
    return true;
}else {
    return false;
}
}


var reg_calss = function () {
    let pass = window.prompt("pass", "please enter the class token");
    console.log(pass)

    $.getJSON(`http://127.0.0.1:5000/student_get_class/${pass}`,(data)=>{
        let c = data
        let addClass = `<tr><th><a href="http://127.0.0.1:5000/student_within_course/${c.code}">${c.code}</th> <td>${c.title}</td><td>${c.info}</td></tr>`
        let tbody = document.getElementsByTagName('tbody')[0]
        tbody.innerHTML = tbody.innerHTML + addClass
    })
}

function show_question_list() {
	//let pass = window.prompt("pass", "please enter the class token");
    //console.log(pass)

        c = {name: "Q1", type: "Next"};
        //let addClass = `<tr><th><a href="http://127.0.0.1:5000/student_within_course/${c.code}">${c.code}</th> <td>${c.title}</td><td>${c.info}</td></tr>`
        let addQuestion = `<tr>
	                        <th scope="row">${c.name}</th>
	                        <td>${c.type}</td>
	                        <td><button type="button" class="btn btn-primary">View</button></td>
	                        <td><button type="button" class="btn btn-success">Start</button></td>
	                      </tr>`
        let tbody = document.querySelector("#qlist")
        console.log(document.querySelector("#qlist"))
        //let tbody = document.getElementsByTagName('qlist')[0]
        console.log(tbody)
        tbody.innerHTML = tbody.innerHTML + addQuestion

/*    $.getJSON(`http://127.0.0.1:5000/teacher_get_question/${pass}`,(data)=>{
        //let c = data

    })*/
}

//show_question_list();

