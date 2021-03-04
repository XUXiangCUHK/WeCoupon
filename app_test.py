from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, CreateClassForm
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

@app.route('/teacher_create_course/<instructor>', methods=['GET', 'POST'])
def create_course(instructor):
    form = CreateClassForm()
    if form.validate_on_submit():
        input_token=form.course_token.data
        print(input_token)
        # return redirect(url_for('teacher_main_page'))
    return render_template('teacher_create_course.html', form=form)

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

@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
def teacher_view(classcode):
    question_list = [{'question_id': 'question#1', 'question_type': 'MC'},
                    {'question_id': 'question#2', 'question_type': 'Type'},]
    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
    return render_template('teacher_within_course.html', question_list=question_list, participation_list=participation_list)

#@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
#def teacher_view_participation(classcode):
#    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
#                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
#    return render_template('teacher_within_course.html', participation_list=participation_list)


if __name__ == '__main__':
    app.run(debug=True)
