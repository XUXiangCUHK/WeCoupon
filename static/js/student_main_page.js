// var reg_calss = function () {
//     let pass = window.prompt("pass", "please enter the class token");
//     console.log(pass)

//     let c = { 'code': 'csci3100', 'title': 'Tom', 'info': 'other' }
//     let xml = new XMLHttpRequest()
//     console.log(xml.readyState)
//     xml.onreadystatechange = function () {
//       if (xml.readyState == 4) {
//         console.log(xml.readyState)
//         console.log(xml.responseText)
//         let c = JSON.parse(xml.responseText)
//         console.log(c)
//         let addClass = `<tr><th><a href="http://127.0.0.1:5000/student_within_course?${c.code}">${c.code}</th> <td>${c.title}</td><td>${c.info}</td></tr>`
//         let tbody = document.getElementsByTagName('tbody')[0]
//         tboy.innerHTML = tbody.innerHTML + addClass
//       }
//     }
//     xml.open('GET', `http://127.0.0.1:5000/student_get_class?password=${pass}`)
//     xml.send()
//   }


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

 