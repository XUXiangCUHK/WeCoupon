function display() {
    document.getElementById('contes').style.display = 'block';
}

function teacher_add_class() {
    document.getElementById('contes').style.display = 'none';
    var course_code = document.getElementById('code').value;
    var course_name = document.getElementById('name').value;
    var course_instructor = document.getElementById('instructor').value;
    var course_token = document.getElementById('token').value;

    $.getJSON(`../teacher_create_class/${course_code}&${course_name}&${course_instructor}&${course_token}`,(data)=>{
        let c = data
        let addClass = `<tr><th><a href="http://127.0.0.1:5000/teacher_within_course/${c.course_id}">${c.course_code}</th> <td>${c.course_name}</td><td>${c.course_instructor}</td></tr>`
        let tbody = document.getElementsByTagName('tbody')[0]
        tbody.innerHTML = tbody.innerHTML + addClass
    })

}

function display_edit_profile() {
    //console.log(document.getElementById("name"))

    var b = document.querySelector("#name");
    b.setAttribute("value", document.getElementById("name_display").value);
    console.log(document.getElementById("name_display").value)

    document.getElementById("name").innerHTML = "New text!";
    document.getElementById('edit_profile').style.display = 'block';
}

function edit_profile() {
    document.getElementById('edit_profile').style.display = 'none';
    var course_token = document.getElementById('token').value;

    $.getJSON(`http://127.0.0.1:5000/student_get_class/${course_token}`,(data)=>{
        let c = data
        let addClass = `<tr><th><a href="http://127.0.0.1:5000/student_within_course/${c.course_id}">${c.course_code}</th> <td>${c.course_name}</td><td>${c.course_instructor}</td></tr>`
        let tbody = document.getElementsByTagName('tbody')[0]
        tbody.innerHTML = tbody.innerHTML + addClass
    })
}