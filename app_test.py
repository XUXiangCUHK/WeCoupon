from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
# from email import send_email
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_pw = form.password.data
        if True:
            user_id = 1
            is_student = 1
            session['user_id'] = user_id

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if is_student:
                    next = url_for('student_main', messages=user_id)
                else:
                    next = url_for('teacher_main')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        is_student = 1
        activated = 0
        if form.isInstructor.data:
            is_student = 0
        # email verification
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/teacher_main_page', methods=['GET', 'POST'])
def teacher_main():
    user_id = session['user_id']
    print(user_id)
    return render_template('teacher_main_page.html')


@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    user_id = session['user_id']
    enroll_info = [{'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'},
                   {'code': 'IERG3310', 'title': 'Computer Networking', 'info': 'Prof. Xing Guoliang'},
                   {'code': 'FTEC3001', 'title': 'Financial Innovation & Structured Products', 'info': 'Prof. Chen Nan'}]
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def atudent_within_course(classcode):
    return render_template('student_within_course.html')


@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
def student_get_class(password):
    user_id = session['user_id']
    class_info = {'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_view_answer/<question>', methods=['GET', 'POST'])
def teacher_view_answer(question):
    question_info = {'question_name': 'Q1', 'corresponding_course': 'CSCI3100'}
    answer_list = [{'answer_user': 'student1', 'answer_content': 'This is sample answer0'},
                    {'answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
                    {'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=question_info, answer_list=answer_list, per_ans=per_ans)

@app.route('/add_coupon/<username>', methods=['GET', 'POST'])
def reward_coupon(username):
    # get the username of student who is rewarded coupon
    print(username)
    return username

if __name__ == '__main__':
    app.run(debug=True)
