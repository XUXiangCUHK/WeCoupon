import json
from threading import Thread
from hashlib import md5

from flask import Flask, request, render_template
from flask import flash, url_for, redirect, session
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user
from flask_login import login_required, current_user, LoginManager

from models import User
from db.sql import Sql
from db.manipulator import Manipulator

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
# mail configuration
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'wecoupon2021@163.com'
app.config['MAIL_PASSWORD'] = 'YRWOKOXTQLUDZVFV'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = 'WeCoupon'

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
# db configuration
sql = Sql()
mani = Manipulator()


@login_manager.user_loader
def load_user(user_email):
    print('load user')
    return User.get(user_email)


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


@app.route('/email_check')
def email_check():
    return render_template('email_check.html')


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    current_user.token = token
    if current_user.activated == 1:
        if current_user.is_student == 1:
            next = url_for('student_main')
        else:
            next = url_for('teacher_main')
        return redirect(next)
    else:
        if current_user.activate(token):
            print("update: ", current_user.user_id)
            sql.update_account_activated(current_user.user_id)
            if current_user.is_student == 1:
                next = url_for('student_main')
            else:
                next = url_for('teacher_main')
            return redirect(next)
    return redirect(url_for('login'))


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.activated == 1:
        if current_user.is_student == 1:
            next = url_for('student_main')
        else:
            next = url_for('teacher_main')
        return redirect(next)
    return render_template('unconfirmed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_pw = form.password.data
        if mani.user_verification(input_email, input_pw):
            user = User(input_email)
            login_user(user)
            if current_user.activated:
                if current_user.is_student:
                    # will add message=user_id to the link
                    next = url_for('student_main', messages=current_user.user_id)
                else:
                    next = url_for('teacher_main')
            else:
                next = url_for('unconfirmed')
            return redirect(next)
        # flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        is_student = 1
        activated = 0
        if form.isInstructor.data:
            is_student = 0

        encoded_info = form.username.data + form.last_name.data + form.first_name.data + form.email.data
        token = md5(encoded_info.encode("utf-8")).hexdigest()

        mani.insert_account_info(form.username.data,
                                 form.last_name.data,
                                 form.first_name.data,
                                 form.email.data,
                                 form.SID.data,
                                 form.password.data,
                                 is_student,
                                 activated,
                                 token)

        send_email(form.email.data, 'Confirm Your Account', 'email/confirm',
                   user=form.username.data, token=token)

        user = User(form.email.data)
        login_user(user)

        return redirect(url_for('email_check'))
    return render_template('signup.html', form=form)


@app.route('/teacher_main_page', methods=['GET', 'POST'])
@login_required
def teacher_main():
    user_id = session['user_id']
    enroll_info = mani.user_enrollment(user_id)
    print(enroll_info)
    return render_template('teacher_main_page.html', teach_info=enroll_info)


@app.route('/student_main_page', methods=['GET', 'POST'])
@login_required
def student_main():
    print('student main: ', current_user.user_name)
    # user_id = session['user_id']
    # user_id = request.args['messages']
    enroll_info = mani.user_enrollment(current_user.user_id)
    print(enroll_info)
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/teacher_create_class/<course_code>&<course_name>&<course_instructor>&<course_token>', methods=['GET', 'POST'])
@login_required
def teacher_create_class(course_code, course_name, course_instructor, course_token):
    user_id = session['user_id']
    mani.insert_course_info(course_code, course_name, course_instructor, course_token)
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(user_id, course_id)
    print(class_info)
    return json.dumps(class_info)


@app.route('/student_get_class/<course_token>', methods=['GET', 'POST'])
@login_required
def student_get_class(course_token):
    user_id = session['user_id']
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(user_id, course_id)
    print(class_info)
    return json.dumps(class_info)


@app.route('/teacher_within_course/<course_id>', methods=['GET', 'POST'])
@login_required
def teacher_view(course_id):
    user_id = session['user_id']
    new_question_list, old_question_list = mani.fetch_question_info_by_account(user_id, course_id)
    course_code = new_question_list[0]['course_code']
    participation_list = mani.fetch_participation(course_id)
    return render_template('teacher_within_course.html',
                           course_code=course_code,
                           new_question_list=new_question_list,
                           old_question_list=old_question_list,
                           participation_list=participation_list)


@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_answer(question_id):
    print(question_id)
    question_info = mani.fetch_question_info(question_id)
    answer_list = mani.fetch_answer_list(question_id)
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=question_info, answer_list=answer_list, per_ans=per_ans)


@app.route('/add_coupon/<userid>', methods=['GET', 'POST'])
@login_required
def reward_coupon(userid):
    print(userid)
    coupon_num = mani.fetch_coupon_num(userid)
    mani.insert_coupon_info(userid, coupon_num+1, "reward")
    return True
    # current_class = 'CSCI3100'
    # return current_class


@app.route('/teacher_add_question/<courseid>', methods=['GET', 'POST'])
@login_required
def teacher_add_question(courseid):
    return render_template('teacher_add_question.html', course_id=courseid)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
@login_required
def student_within_course(classcode):
    return render_template('student_within_course.html')


if __name__ == '__main__':
    app.run(debug=True)
