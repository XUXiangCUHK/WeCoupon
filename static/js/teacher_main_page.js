var teacher_add_class = function () {
    document.getElementById('contes').style.display = 'block';

    $.getJSON(`http://127.0.0.1:5000/teacher_create_class/${course_name}${course_token}`,(data)=>{
        let c = data
        c = { 'code': 'csci3100', 'title': 'Tom', 'info': 'other' }
        console.log(c)
        let addClass = `<tr><th><a href="http://127.0.0.1:5000/teacher_within_course/${c.code}">${c.code}</th> <td>${c.title}</td><td>${c.info}</td></tr>`
        let tbody = document.getElementsByTagName('tbody')[0]
        tbody.innerHTML = tbody.innerHTML + addClass
    })
}

