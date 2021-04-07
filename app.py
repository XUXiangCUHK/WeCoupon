import json
from threading import Thread
from hashlib import md5

from flask import Flask, request, render_template
from flask import flash, url_for, redirect, session
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, AddQuestionForm, EditQuestionForm, AddAnswer
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

# @login_manager.user_loader
# def load_user(user_id):
#     print("user loaded!: ", user_id)
#     user_email = mani.fetch_user_info_by_id(user_id, ['email'])
#     user = User(user_email)
#     print("user email: ", user_email)
#     return user


########################################################################################################################
# This part is for email configuration, including send_email function, confirm and unconfirmed status.
########################################################################################################################


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


########################################################################################################################
# This part is for user management, including login, logout, signup functions.
########################################################################################################################


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


########################################################################################################################
# This part is for teacher administration, including main page, question page and answer page.
########################################################################################################################


@app.route('/teacher_main_page', methods=['GET', 'POST'])
@login_required
def teacher_main():
    print("Inside teacher_main_page")
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
    return render_template('teacher_main_page.html',
                           teach_info=enroll_info,
                           teach_profile=teach_profile)


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


@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_answer(question_id):
    print("Inside teacher_view_answer")
    sql.update_question_status(question_id)
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    # question_info = mani.fetch_question_info(question_id)
    answer_list = mani.fetch_answer_list(question_id)
    per_ans = mani.fetch_per_ans(current_user.current_course_id, question_id)
    return render_template('teacher_view_answer.html',
                           question_info=current_user.current_q,
                           answer_list=answer_list,
                           per_ans=per_ans)


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
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    print("here is", question_id)
    answer_list = mani.fetch_answer_list(question_id)
    per_ans = mani.fetch_per_ans(current_user.current_course_id, question_id)
    return render_template('teacher_collect_answer.html',
                           question_info=current_user.current_q,
                           answer_list=answer_list,
                           per_ans=per_ans)


@app.route('/add_coupon/<userid>', methods=['GET', 'POST'])
@login_required
def reward_coupon(userid):
    print("Inside add_coupon")
    coupon_num = mani.fetch_coupon_num(userid)
    mani.insert_coupon_info(userid, current_user.current_course_id, coupon_num+1, "reward")
    return True


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


@app.route('/update_answer', methods=["GET"])
@login_required
def update_answer():
    print('Inside update_answer')
    question_id = session['question_id']
    course_id = mani.fetch_question_info_by_id(question_id, ['course_id'])
    answer_list = mani.fetch_answer_list(course_id)
    return json.dumps(answer_list)


########################################################################################################################
# This part is for student administration, including main page, competing page and participation page.
########################################################################################################################


@app.route('/student_main_page', methods=['GET', 'POST'])
@login_required
def student_main():
    print("Inside student_main_page")
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
    return render_template('student_main_page.html',
                           enroll_info=enroll_info,
                           student_profile=student_profile)


@app.route('/student_get_class/<course_token>', methods=['GET', 'POST'])
@login_required
def student_get_class(course_token):
    print("Inside student_get_class")
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(current_user.user_id, course_id)
    return json.dumps(class_info)


@app.route('/student_within_course/<course_id>', methods=['GET', 'POST'])
@login_required
def student_within_course(course_id):
    print("Inside student_within_course")
    form = AddAnswer()
    current_user.current_course_id = course_id
    current_user.fill_course_info()
    if form.validate_on_submit():
        input_answer = form.answer.data
        print(input_answer)
        open_q_id = mani.fetch_open_question(course_id)
        if open_q_id:
            current_user.current_q_id = open_q_id
            current_user.fill_question_info()
            print("here is question: ", current_user.current_q.q_content)
        else:
            print("there is no current open question")
    return render_template('student_within_course.html', course_id=course_id, form=form)


if __name__ == '__main__':
    app.run(debug=True)
