function display() {
    document.getElementById('contes').style.display = 'block';
}

function reg_class() {
    document.getElementById('contes').style.display = 'none';
    var course_token = document.getElementById('token').value;

    $.getJSON(`http://127.0.0.1:5000/student_get_class/${course_token}`,(data)=>{
        let c = data
        let addClass = `<tr><td><a href="http://127.0.0.1:5000/student_within_course/${c.course_id}">${c.course_code}</td> <td>${c.course_name}</td><td>${c.course_instructor}</td></tr>`
        let tbody = document.getElementsByTagName('tbody')[0]
        tbody.innerHTML = tbody.innerHTML + addClass
    })
}

 