from flask import Flask, request, render_template, abort
import json
#from db_operations import db_verify

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    return render_template('student_main_page.html')

@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def atudent_within_course(classcode):
    return render_template('student_within_course.html')

@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
def student_get_class(password):
    param = request.get_data()
    print(param)
    # get from db
    classinfo = {
        'name': 'csc1231',
        'code': '123456',
        'info':'other'
    }
    return json.dumps(classinfo)

@app.route('/login_test', methods=['GET', 'POST'])
def login_test():
    login_info = request.get_data()
    if login_info:
        print(login_info)
        json_info = json.loads(login_info)

        username = json_info['user_name']
        password = json_info['password']
        #success = db_verify(json_info)
        success = 1
        print(json_info)
        if success == 1:
            return 'Successful!'
        else:
            abort(404)

if __name__ == '__main__':
    app.run()