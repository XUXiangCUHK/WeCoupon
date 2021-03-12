from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, CreateClassForm
from flask_login import login_required, current_user, LoginManager
import json
import random
from models import User

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'


from threading import Thread
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'wecoupon2021@163.com'
app.config['MAIL_PASSWORD'] = 'YRWOKOXTQLUDZVFV'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = 'WeCoupon'

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        input_email = 'teacher@gmail.com'
        user = User(input_email)
    elif user_id == '2':
        input_email = 'student@gmail.com'
        user = User(input_email)
    return user     # query all info of the user from db


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ': ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/unconfirmed')
def unconfirmed():
    if current_user.activated == '1':
        if current_user.is_student == '1':
            next = url_for('student_main')
        else:
            next = url_for('teacher_main')
        return redirect(next)
    return render_template('unconfirmed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_pw = form.password.data
        user = User(input_email)
        if user is not None and input_pw == user.password:
            session['user_id'] = user.user_id
            print(user.user_id)
            if user.activated == '0':
                next = url_for('unconfirmed')
            if next is None or not next.startswith('/'):
                if user.is_student == '1':
                    next = url_for('student_main')
                else:
                    next = url_for('teacher_main')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user = User(user_email)
        # is_student = 1
        # activated = 0
        if form.isInstructor.data:
            user.is_student = 0
        # insert into db
        # email verification
        token = user.generate_random_token()
        # token insert into db
        send_email(user_email, 'Confirm Your Account',
              'email/confirm', user=form.username.data, token=token)
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    print(token)
    if current_user.activated == '1':
        if current_user.is_student == '1':
            next = url_for('student_main')
        else:
            next = url_for('teacher_main')
        return redirect(next)
    else:
        if current_user.activate(token):
            if current_user.is_student == '1':
                next = url_for('student_main')
            else:
                next = url_for('teacher_main')
            return redirect(next)
    return redirect(url_for('login'))


@app.route('/teacher_create_course/<instructor>', methods=['GET', 'POST'])
def create_course(instructor):
    form = CreateClassForm()
    if form.validate_on_submit():
        input_token = form.course_token.data
        print(input_token)
        # return redirect(url_for('teacher_main_page'))
    return render_template('teacher_create_course.html', form=form)


@app.route('/teacher_main_page', methods=['GET', 'POST'])
def teacher_main():
    user_id = session['user_id']
    print('user_id: ', user_id)
    print('teacher_main')
    print(current_user.username)
    teach_info = [{'course_id': 4, 'code': 'ESTR4999', 'title': 'Graduation Thesis', 'info': 'Prof. Michael R. Lyu'},
                  {'course_id': 5, 'code': 'ESTR4998', 'title': 'Graduation Thesis', 'info': 'Prof. Michael R. Lyu'}]
    return render_template('teacher_main_page.html', teach_info=teach_info)


@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    user_id = session['user_id']
    print('user_id: ', user_id)
    # user_msg = request.args['messages']
    print(current_user.username)
    print('student_main')
    # print(user_msg)
    enroll_info = [{'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'},
                   {'course_id': 3, 'code': 'IERG3310', 'title': 'Computer Networking', 'info': 'Prof. Xing Guoliang'}]
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def student_within_course(classcode):
    print("student_within_course")
    return render_template('student_within_course.html',course_code=classcode)


@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
def student_get_class(password):
    user_id = session['user_id']
    print('student_get_class')
    class_info = {'course_id': 7, 'course_code': 'CSCI2001', 'course_name': 'Data Structure', 'course_instructor': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_create_class/<course_name>&<course_token>', methods=['GET', 'POST'])
def teacher_create_class(course_name, course_token):
    print('teacher_create_class')
    class_info = {'course_id': 7, 'course_code': 'CSCI2001', 'course_name': 'Data Structure', 'course_instructor': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
def teacher_view_answer(question_id):
    print(question_id)
    question_info = {'question_id': '1', 'question_name': 'Q1', 'corresponding_course': 'CSCI3100', 'question_status': '1'}
    answer_list = [{'answer_userid': '02', 'answer_user': 'student1', 'answer_content': 'This is sample answer0'},
                    {'answer_userid': '234','answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=question_info, answer_list=answer_list, per_ans=per_ans)

@app.route('/stopcollection', methods=['GET', 'POST'])
def stopCollection():
    print("stop collection")
    question_id=request.form.get('qid')
    print(question_id)
    # change the question status to not collecting 
    return redirect(url_for('teacher_view_answer'), question_id=question_id) 
    # bug here

@app.route('/add_coupon/<userid>', methods=['GET', 'POST'])
def reward_coupon(userid):
    # get the username of student who is rewarded coupon
    print(userid)
    current_class = 'CSCI3100'
    # coupon_number++
    # update db
    # flash('Congratulations! {} got this coupon!'.format(username))
    return current_class

@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
def teacher_view(classcode):
    print(classcode)
    new_question_list = [{'q_id': 1, 'question_id': 'question#4', 'question_type': 'MC'},
                    {'q_id': 2, 'question_id': 'question#5', 'question_type': 'Type'},]
    old_question_list = [{'q_id': 3, 'question_id': 'question#1', 'question_type': 'MC'},
                    {'q_id': 4, 'question_id': 'question#2', 'question_type': 'Type'},
                    {'q_id': 5, 'question_id': 'question#3', 'question_type': 'Type'}]
    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
    return render_template('teacher_within_course.html', course_code=classcode, new_question_list=new_question_list, old_question_list=old_question_list, participation_list=participation_list)

#@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
#def teacher_view_participation(classcode):
#    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
#                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
#    return render_template('teacher_within_course.html', participation_list=participation_list)


if __name__ == '__main__':
    app.run(debug=True)
