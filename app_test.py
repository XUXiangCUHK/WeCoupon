from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, CreateClassForm
# from flask_mail import Mail
# from email import send_email
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'

# app = Mail(app)
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''


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
            if input_pw == '0':
                is_student = 0

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
        # insert into db
        # email verification
        # token =
        # user_email = form.email.data
        # send_email(user_email, 'Confirm Your Account',
        #       'email/confirm', user=user, token=token)

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

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
    print('teacher_main')
    teach_info = [{'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Monday'},
                   {'code': 'IERG3310', 'title': 'Computer Networking', 'info': 'Tuesday'},
                   {'code': 'FTEC3001', 'title': 'Financial Innovation & Structured Products', 'info': 'Thursday'}]
    return render_template('teacher_main_page.html', teach_info=teach_info)


@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    user_id = session['user_id']
    user_msg = request.args['messages']
    print('student_main')
    print(user_msg)
    enroll_info = [{'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'},
                   {'code': 'IERG3310', 'title': 'Computer Networking', 'info': 'Prof. Xing Guoliang'},
                   {'code': 'FTEC3001', 'title': 'Financial Innovation & Structured Products', 'info': 'Prof. Chen Nan'}]
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def student_within_course(classcode):
    print("student_within_course")
    return render_template('student_within_course.html',course_code=classcode)


@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
def student_get_class(password):
    user_id = session['user_id']
    print('student_get_class')
    class_info = {'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_create_class/<course_name>&<course_token>', methods=['GET', 'POST'])
def teacher_create_class(course_name, course_token):
    print('teacher_create_class')
    print(course_name)
    print()
    print(course_token)
    class_info = {'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'info': 'Prof. Michael R. Lyu'}
    course_id = class_info['course_id']
    return json.dumps(class_info)

@app.route('/teacher_view_answer/<question_id>', methods=['GET', 'POST'])
def teacher_view_answer(question_id):
    print(question_id)
    question_info = {'question_id': '1', 'question_name': 'Q1', 'corresponding_course': 'CSCI3100'}
    answer_list = [{'answer_user': 'student1', 'answer_content': 'This is sample answer0'},
                    {'answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
                    {'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=question_info, answer_list=answer_list, per_ans=per_ans)

@app.route('/stopcollection', methods=['GET', 'POST'])
def stopCollection():
    print("stop collection")
    question_id=request.form.get("id")
    print(question_id)
    current_class = 'CSCI3100'
    return redirect(url_for('teacher_view', classcode=current_class)) 
    # can we end this function without redictect or rendertemplate? just stay at original page

@app.route('/add_coupon/<username>', methods=['GET', 'POST'])
def reward_coupon(username):
    # get the username of student who is rewarded coupon
    print(username)
    current_class = 'CSCI3100'
    # coupon_number++
    # update db
    # flash('Congratulations! {} got this coupon!'.format(username))
    return redirect(url_for('teacher_view', classcode=current_class))

@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
def teacher_view(classcode):
    print(classcode)
    question_list = [{'question_id': 'question#1', 'question_type': 'MC'},
                    {'question_id': 'question#2', 'question_type': 'Type'},]
    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
    return render_template('teacher_within_course.html', course_code=classcode, question_list=question_list, participation_list=participation_list)

#@app.route('/teacher_within_course/<classcode>', methods=['GET', 'POST'])
#def teacher_view_participation(classcode):
#    participation_list = [{'student_id': '1155095222', 'student_name': 'Bob', 'attempt': '20', 'coupon': '1'},
#                    {'student_id': '1155095222', 'student_name': 'Peter', 'attempt': '10', 'coupon': '5'}]
#    return render_template('teacher_within_course.html', participation_list=participation_list)


if __name__ == '__main__':
    app.run(debug=True)
