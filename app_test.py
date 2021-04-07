from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, CreateClassForm, AddQuestionForm, EditQuestionForm,AddAnswer
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
import json
import random
from models_test import User, Question, Coupon, Course, Answer
# from flask_socketio import SocketIO, emit
# from threading import Lock

# async_mode = None




app = Flask(__name__)
bootstrap = Bootstrap(app)
# socketio = SocketIO(app)

# thread = None
# thread_lock = Lock()

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

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        print("user loaded!: ", user_id)
        if user_id == '1':
            input_email = 'teacher@gmail.com'
            user = User(input_email)
        elif user_id == '2':
            input_email = 'student@gmail.com'
            user = User(input_email)
        print("user loaded???")
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


@app.route('/email_check')
def email_check():
    return render_template('email_check.html')


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
            login_user(user)
            # session['user_id'] = user.user_id
            print('user_id in login', user.user_id, user.username)
            print('current_user in login: ', current_user.username, current_user.email, current_user.token)
            if user.activated == '0':
                next = url_for('unconfirmed')
            else:
                if user.is_student == '1':
                    next = url_for('student_main')
                else:
                    next = url_for('teacher_main')
            return redirect(next)
        flash('Invalid username or password.')
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
        user_email = form.email.data
        user = User(user_email)
        # is_student = 1
        # activated = 0
        if form.isInstructor.data:
            user.is_student = '0'
        # insert into db
        # email verification
        token = user.generate_random_token()
        # token insert into db
        send_email(user_email, 'Confirm Your Account',
              'email/confirm', user=form.username.data, token=token)
        print("In signup: is_student ", user.is_student, form.isInstructor.data)
        login_user(user)
        return redirect(url_for('email_check'))
    return render_template('signup.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    print('token: ', current_user.token, token)
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
@login_required
def create_course(instructor):
    form = CreateClassForm()
    if form.validate_on_submit():
        input_token = form.course_token.data
        print(input_token)
        # return redirect(url_for('teacher_main_page'))
    return render_template('teacher_create_course.html', form=form)


@app.route('/teacher_main_page', methods=['GET', 'POST'])
@login_required
def teacher_main():
    print('teacher_main')
    print(current_user.username)
    teach_info = [{'course_id': 4, 'code': 'ESTR4999', 'title': 'Graduation Thesis', 'info': 'Prof. Michael R. Lyu'},
                  {'course_id': 5, 'code': 'ESTR4998', 'title': 'Graduation Thesis', 'info': 'Prof. Michael R. Lyu'}]
    teach_profile = [{'name': 'Michael R. Lyu', 'department': 'Computer Science and Engineering department', 'title': 'Professor'}]
    return render_template('teacher_main_page.html', teach_info=teach_info, teach_profile=teach_profile)


@app.route('/student_main_page', methods=['GET', 'POST'])
@login_required
def student_main():
    # user_msg = request.args['messages']
    print('student_main')
    print(current_user.username)
    # print(user_msg)
    enroll_info = [{'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'},
                   {'course_id': 3, 'code': 'IERG3310', 'title': 'Computer Networking', 'info': 'Prof. Xing Guoliang'}]
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
@login_required
def student_within_course(classcode):
    form = AddAnswer()
    if form.validate_on_submit():
        print(form.question)
        pass
    else:
        pass       
    current_user.current_classcode = classcode
    print("current_user.current_classcode: ", current_user.current_classcode)
    current_user.fill_course_info()
    print("here is course: ", current_user.current_course.course_name)
    open_question_list = [
            {'question_id': 2, 'course_id': 1, 'question_title': 'question#5', 'q_content': 'test2',
            'question_type': 'Type', 'q_status': '1'},
            {'question_id': 6, 'course_id': 7, 'question_title': 'question#6', 'q_content': 'test6',
            'question_type': 'Short', 'q_status': '1'}]

    return render_template('student_within_course.html', course_code=classcode,form = form)


@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
@login_required
def student_get_class(password):
    print('student_get_class')
    class_info = {'course_id': 7, 'course_code': 'CSCI2001', 'course_name': 'Data Structure', 'course_instructor': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_create_class/<course_name>&<course_token>', methods=['GET', 'POST'])
@login_required
def teacher_create_class(course_name, course_token):
    print('teacher_create_class')
    class_info = {'course_id': 7, 'course_code': 'CSCI2001', 'course_name': 'Data Structure', 'course_instructor': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_collect_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_collect_answer(question_id):
    if question_id == 'default':
        print("default empty question created!")
        # create a default question in database first
    # change the question status to open_to_student if not, start to receive answers from students and display
    print(question_id)
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    current_user.current_q.q_status = '1'
    current_user.current_classcode = current_user.current_q.course_id
    current_user.fill_course_info()
    print("teacher_collect_answer: ", current_user.current_q.q_status)
    answer_list = [{'answer_userid': '02', 'answer_user': 'student1', 'answer_content': 'This '},
                    # {'answer_userid': '234','answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_collect_answer.html', question_info=current_user.current_q, answer_list=answer_list, per_ans=per_ans)

@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_answer(question_id):
    # change the question status to stop_collecting if not, display results
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    current_user.current_q.q_status = '2'
    current_user.current_classcode = current_user.current_q.course_id
    current_user.fill_course_info()
    print("teacher_view_answer: ", current_user.current_q.q_status)
    answer_list = [{'answer_userid': '02', 'answer_user': 'student1', 'answer_content': 'This '},
                    # {'answer_userid': '234','answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},
                    {'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=current_user.current_q, answer_list=answer_list, per_ans=per_ans)

@app.route('/add_coupon/<userid>&<q_id>', methods=['GET', 'POST'])
@login_required
def reward_coupon(userid, q_id):
    # get the username of student who is rewarded coupon
    print(userid, q_id)
    current_user.current_q_id = q_id
    current_user.fill_question_info()
    current_user.current_classcode = current_user.current_q.course_id
    current_user.fill_course_info()
    print("add_coupon: ", current_user.current_course.course_name)
    # coupon_number++
    # update db
    # flash('Congratulations! {} got this coupon!'.format(username))
    return True

@app.route('/teacher_within_course/<course_id>', methods=['GET', 'POST'])
@login_required
def teacher_view(course_id):
    current_user.current_classcode = course_id
    print("current_user.current_classcode: ", current_user.current_classcode)
    current_user.fill_course_info()
    print("here is course: ", current_user.current_course.course_name)
    new_question_list = [{'question_id': 1, 'question_title': 'question#4', 'question_type': 'MC'},
                    {'question_id': 2, 'question_title': 'question#5', 'question_type': 'Type'},]
    old_question_list = [{'question_id': 3, 'question_title': 'question#1', 'question_type': 'MC'},
                    {'question_id': 4, 'question_title': 'question#2', 'question_type': 'Type'},
                    {'question_id': 5, 'question_title': 'question#3', 'question_type': 'Type'}]
    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon_rewarded': '1', 'coupon_used': '0'},
                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon_rewarded': '5', 'coupon_used': '2'},
                    {'student_id': '1155095233', 'student_name': 'Jason', 'attempt': '10', 'coupon_rewarded': '5', 'coupon_used': '5'}]
    return render_template('teacher_within_course.html', classcode='CSCI3100', course_id=course_id, new_question_list=new_question_list,
                           old_question_list=old_question_list, participation_list=participation_list)

@app.route('/use_coupon/<student_id>&<course_id>', methods=['GET', 'POST'])
@login_required
def use_coupon(student_id, course_id):
    print(student_id)
    print(course_id)
    # deduct 1 coupon from student
    return True
    # return "csci3100"
    # ? how to return refreshed same webpage? 

@app.route('/teacher_add_question/<course_id>', methods=['GET', 'POST'])
@login_required
def teacher_add_question(course_id):
    form = AddQuestionForm()
    if form.validate_on_submit():
        input_title = form.question_title.data
        input_content = form.question_content.data
        print(input_title)
        print(input_content)
        # Store the question in database and get back its question_id
        question_id = '123'
        return redirect(url_for('teacher_view_question', question_id=question_id))
    return render_template('teacher_add_question.html', course_id=course_id, form=form)

@app.route('/teacher_view_question/<question_id>', methods=['GET', 'POST'])
@login_required
def teacher_view_question(question_id):
    # use question_id to get question_title and question_content and corresponding course info
    form = EditQuestionForm(question_title='title', question_content='content')
    current_user.current_q_id = question_id
    current_user.fill_question_info()
    current_user.current_classcode = current_user.current_q.course_id
    print('In teacher_view_question, current_classcode:', current_user.current_classcode)
    current_user.fill_course_info()
    print('In teacher_view_question, q_status:', current_user.current_q.q_status)
    print('In teacher_view_question, current_course:', current_user.current_course.course_name)
    if form.validate_on_submit():
        input_title = form.question_title.data
        input_content = form.question_content.data
        print(input_title)
        print(input_content)
        # Store the edited question in database and get back its question_id, this time return the updated data 
        form = EditQuestionForm(question_title=input_title, question_content=input_content)
        course_info = {'course_id': '123', 'course_code': 'CSCI3100'}
        return render_template('teacher_view_question.html', form=form)
    course_info = {'course_id': '123', 'course_code': 'CSCI3100'}
    return render_template('teacher_view_question.html', form=form)

# @app.route('/update_answer', methods=["GET"])
# @login_required
# def update_answer():
#     answer_list = {"1":{'answer_userid': '02', 'answer_user': 'student1', 'answer_content': 'This '},
#                     "2":{'answer_userid': '234','answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
#                     "3":{'answer_userid': '312', 'answer_user': 'student3', 'answer_content': 'This?'}}
#     return json.dumps(answer_list)


#@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
#def teacher_view_participation(classcode):
#    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
#                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
#    return render_template('teacher_within_course.html', participation_list=participation_list)


# update value from backend without refreshing page
# @socketio.on('connect', namespace='/teacher_collect_answer')
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(target=background_thread)

# def background_thread():
#     while True: 
#         print("in text_connet")
#         socketio.sleep(5)
#         t = random.randint(1,100)
#         a = random.randint(100,1000)
#         print(t)
#         socketio.emit('server_response', {'data1': t, 'data2': a}, namespace='/teacher_collect_answer')

if __name__ == '__main__':
    app.run(debug=True)
