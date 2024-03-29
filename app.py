"""
PROGRAM MAIN APPLICATION - Program to run WeCoupon Website
PROGRAMMER - XU Xiang (1155107785);
             LAI Wei (1155095200);
             ZENG Meiqi (1155107891);
             ZHANG Yusong(1155107841);
             ZHOU Yifan (1155124411)
CALLING SEQUENCE - Simply run 'python app.py' in the terminal
VERSION - written on 2021/04/13
REVISION - 2021/04/21 for testing and new function improvement
PURPOSE - To build a website for more interactive class participation and more fair coupon competition.
"""

import json
from threading import Thread
from hashlib import md5

from flask import Flask, request, render_template
from flask import flash, url_for, redirect, session
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
from forms import AddQuestionForm, EditQuestionForm, AddAnswer
from forms import CreateClassForm, RegClass
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

# login management
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# db configuration
sql = Sql()
mani = Manipulator()

@login_manager.user_loader
def load_user(user_email):
    if user_email:
        print('load user')
        return User.get(user_email)


########################################################################################################################
# This part is for email configuration, including send_email function, confirm and unconfirmed status.
########################################################################################################################

# For email configuration
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# The function is designed for sending email
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ': ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


# To create a route for email checking notification
@app.route('/email_check')
def email_check():
    return render_template('email_check.html')


# To create a route for token confirmation
# The function interacts with Account System
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


# To create a route for unconfirmed page
# The function interacts with Account System
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


########################################################################################################################
# This part is for user management, including login, logout, signup functions.
########################################################################################################################


# To create a route for login
# The function interacts with Account System
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


# To create a route for logout
# The function interacts with Account System
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# To create a route for signup
# The function interacts with Account System
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


########################################################################################################################
# This part is for teacher administration, including main page, question page and answer page.
########################################################################################################################


# To create a route for teacher main page
# The function interacts with Account System, Course System
@app.route('/teacher_main_page', methods=['GET', 'POST'])
@login_required
def teacher_main():
    print("Inside teacher_main_page")
    form = CreateClassForm()
    enroll_info = mani.user_enrollment(current_user.user_id)
    first_name = mani.fetch_user_info_by_id(current_user.user_id, ['first_name'])
    last_name = mani.fetch_user_info_by_id(current_user.user_id, ['last_name'])
    pos = mani.fetch_user_info_by_id(current_user.user_id, ['is_student'])
    greeting = "Welcome, {} {}".format(last_name, first_name)
    university = "The Chinese University of Hong Kong"
    if not pos:
        title = "Professor"
    else:
        title = "Student"
    teach_profile = [{'name': greeting, 'department': university, 'title': title}]
    if form.validate_on_submit():
        course_code = form.course_code.data
        course_title = form.course_title.data
        course_instructor = form.course_instructor.data
        course_token = form.course_token.data
        print("token:", course_token)
        mani.insert_course_info(course_code, course_title, course_instructor, course_token)
        class_info = mani.fetch_course_info(course_token)
        mani.insert_enrollment_info(current_user.user_id, class_info['course_id'])
        return redirect(url_for('teacher_main'))
    return render_template('teacher_main_page.html',
                           teach_info=enroll_info,
                           teach_profile=teach_profile,
                           form=form)


# To create a route for teacher to create a class
# The function interacts with Course System
@app.route('/teacher_create_class/<course_code>&<course_name>&<course_instructor>&<course_token>',
           methods=['GET', 'POST'])
@login_required
def teacher_create_class(course_code, course_name, course_instructor, course_token):
    print("Inside teacher_create_class")
    user_id = current_user.user_id
    mani.insert_course_info(course_code, course_name, course_instructor, course_token)
    class_info = mani.fetch_course_info(course_token)
    mani.insert_enrollment_info(user_id, class_info['course_id'])
    return json.dumps(class_info)


# To create a route for teacher to go into one specific course
# The function interacts with Course System
@app.route('/teacher_within_course/<course_id>', methods=['GET', 'POST'])
@login_required
def teacher_view(course_id):
    print("Inside teacher_within_course")
    new_question_list, old_question_list = mani.fetch_question_info_by_account(current_user.user_id, course_id)
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    participation_list = mani.fetch_participation(course_id)
    return render_template('teacher_within_course.html',
                           course_code=current_user.current_course.course_code,
                           new_question_list=new_question_list,
                           old_question_list=old_question_list,
                           participation_list=participation_list)


# To create a route for teacher to view answer
# The function interacts with Question System, Answer System
@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_answer(question_id):
    print("Inside teacher_view_answer")
    sql.update_question_status(question_id, 'N')
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    answer_list = mani.fetch_answer_list(question_id)
    per_ans = mani.fetch_per_ans(current_user.current_course_id, question_id)
    return render_template('teacher_view_answer.html',
                           question_info=current_user.current_q,
                           answer_list=answer_list,
                           per_ans=per_ans)


# To create a route for teacher to collect answers
# The function interacts with Question System, Answer System
@app.route('/teacher_collect_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_collect_answer(question_id):
    print("Inside teacher_collect_answer")
    if question_id == 'default':
        print("default empty question created!")
        mani.insert_question_info(current_user.user_id, 1, 'Random Coupon',
                                  'This is a random coupon. Please follow the instruction from professor.', '', 'A')
        question_id = sql.read_max_question_id()[0][0]
        return redirect(url_for('teacher_collect_answer', question_id=question_id))

    session['question_id'] = question_id
    sql.update_question_status(question_id, 'O')
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    answer_list = mani.fetch_answer_list(question_id)
    per_ans = mani.fetch_per_ans(current_user.current_course_id, question_id)
    return render_template('teacher_collect_answer.html',
                           question_info=current_user.current_q,
                           answer_list=answer_list,
                           per_ans=per_ans)


# To create a route for teacher to add coupon
# The function interacts with Coupon System
@app.route('/add_coupon/<userid>&<q_id>&<a_id>', methods=['GET', 'POST'])
@login_required
def reward_coupon(userid, q_id, a_id):
    print("Inside add_coupon")
    course_id = mani.fetch_question_info_by_id(q_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = q_id
    current_user.fill_question_info()
    mani.insert_coupon_info(userid, course_id, 0, "reward")
    sql.update_answer_status(a_id, 1)
    return str()


# To create a route for teacher to use coupon
# The function interacts with Coupon System
@app.route('/use_coupon/<student_id>&<course_id>', methods=['GET', 'POST'])
@login_required
def use_coupon(student_id, course_id):
    print("Inside use_coupon")
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    print(student_id, course_id)
    mani.mark_coupon_as_used(student_id, course_id)
    return redirect(url_for('teacher_view', course_id=course_id))


# To create a route for teacher to add question
# The function interacts with Question System
@app.route('/teacher_add_question/<course_id>', methods=['GET', 'POST'])
@login_required
def teacher_add_question(course_id):
    print("Inside teacher_add_question")
    form = AddQuestionForm()
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    if form.validate_on_submit():
        input_title = form.question_title.data
        input_content = form.question_content.data
        input_answer = form.question_answer.data
        status = 'A'
        mani.insert_question_info(current_user.user_id, current_user.current_course_id,
                                  input_title, input_content, input_answer, status)
        return redirect(url_for('teacher_view', course_id=current_user.current_course_id))
    return render_template('teacher_add_question.html', course_id=course_id, form=form)


# To create a route for teacher to view question
# The function interacts with Question System
@app.route('/teacher_view_question/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_question(question_id):
    print("Inside teacher_view_question")
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    form = EditQuestionForm(question_title=current_user.current_q.q_title,
                            question_content=current_user.current_q.q_content,
                            question_answer=current_user.current_q.q_answer)
    if form.validate_on_submit():
        input_title = form.question_title.data
        input_content = form.question_content.data
        input_answer = form.question_answer.data
        if input_title != current_user.current_q.q_title:
            sql.update_question(question_id, 'q_title', input_title)
        if input_content != current_user.current_q.q_content:
            sql.update_question(question_id, 'q_content', input_content)
        if input_answer != current_user.current_q.q_answer:
            sql.update_question(question_id, 'q_answer', input_answer)
        return redirect(url_for('teacher_view', course_id=current_user.current_course_id))
    return render_template('teacher_view_question.html', course_info=current_user.current_course, form=form)


# To create a route for teacher to update answer
# The function interacts with Answer System
@app.route('/update_answer/<q_id>', methods=["GET"])
@login_required
def update_answer(q_id):
    print("Inside update_answer")
    course_id = mani.fetch_question_info_by_id(q_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = q_id
    current_user.fill_question_info()
    answer_list = mani.fetch_answer_list(q_id)
    return json.dumps(answer_list)


########################################################################################################################
# This part is for student administration, including main page, competing page and participation page.
########################################################################################################################


# To create a route for student main page
# The function interacts with Account System, Course System
@app.route('/student_main_page', methods=['GET', 'POST'])
@login_required
def student_main():
    print("Inside student_main_page")
    form = RegClass()
    first_name = mani.fetch_user_info_by_id(current_user.user_id, ['first_name'])
    last_name = mani.fetch_user_info_by_id(current_user.user_id, ['last_name'])
    pos = mani.fetch_user_info_by_id(current_user.user_id, ['is_student'])
    greeting = "Welcome, {} {}".format(last_name, first_name)
    university = "The Chinese University of Hong Kong"
    if not pos:
        title = "Professor"
    else:
        title = "Student"
    student_profile = [{'name': greeting, 'department': university, 'title': title}]
    enroll_info = mani.user_enrollment(current_user.user_id)
    if form.validate_on_submit():
        course_token = form.token.data
        class_info = mani.fetch_course_info(course_token)
        course_id = class_info['course_id']
        print(mani.check_enrollment(current_user.user_id, course_id))
        if not mani.check_enrollment(current_user.user_id, course_id):
            mani.insert_enrollment_info(current_user.user_id, course_id)
        return redirect(url_for('student_main'))
    return render_template('student_main_page.html',
                           enroll_info=enroll_info,
                           student_profile=student_profile,
                           form=form)


# To create a route for student to register class
# The function interacts with Account System, Course System
@app.route('/student_get_class/<course_token>', methods=['GET', 'POST'])
@login_required
def student_get_class(course_token):
    print("Inside student_get_class")
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(current_user.user_id, course_id)
    return json.dumps(class_info)


# To create a route for student to go into specific course
# The function interacts with Answer System
@app.route('/student_within_course/<course_id>', methods=['GET', 'POST'])
@login_required
def student_within_course(course_id):
    print("Inside student_within_course")
    flag = 0
    question_list = list()
    form = AddAnswer()
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    open_q_id = mani.fetch_open_question(course_id)
    if open_q_id:
        flag = 1
        current_user.current_q_id = open_q_id
        current_user.fill_question_info()
        if form.validate_on_submit():
            input_answer = form.answer.data
            mani.insert_answer_info(open_q_id, current_user.user_id, input_answer, 0)
            print("here is question: ", current_user.current_q.q_content)
        else:
            print("there is no current open question")
    answer_list = mani.fetch_student_participation(current_user.user_id, course_id)
    return render_template('student_within_course.html',
                           course_id=course_id,
                           answer_list=answer_list,
                           form=form,
                           flag=flag,
                           question_list=question_list)


if __name__ == '__main__':
    app.run(debug=True)
