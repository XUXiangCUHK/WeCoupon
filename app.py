from flask import Flask, request, render_template, abort, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
# from email import send_email
import json
from db.manipulator import Manipulator

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hard to guess string'

mani = Manipulator()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_pw = form.password.data
        if mani.user_verification(input_email, input_pw):
            user_id = mani.fetch_user_info_by_email(input_email, ['user_id'])
            is_student = mani.fetch_user_info_by_email(input_email, ['is_student'])
            session['user_id'] = user_id

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if is_student:
                    # will add message=user_id to the link
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
        mani.insert_account_info(form.username.data,
                                 form.last_name.data,
                                 form.first_name.data,
                                 form.email.data,
                                 form.SID.data,
                                 form.password.data,
                                 is_student,
                                 activated)
        # email verification
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/teacher_main_page', methods=['GET', 'POST'])
def teacher_main():
    user_id = session['user_id']
    enroll_info = mani.user_enrollment(user_id)
    return render_template('teacher_main_page.html', teach_info=enroll_info)


@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    user_id = session['user_id']
    # user_id = request.args['messages']
    enroll_info = mani.user_enrollment(user_id)
    return render_template('student_main_page.html', enroll_info=enroll_info)


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def student_within_course(classcode):
    return render_template('student_within_course.html')


@app.route('/teacher_create_class/<course_code>&<course_name>&<course_instructor>&<course_token>', methods=['GET', 'POST'])
def teacher_create_class(course_code, course_name, course_instructor, course_token):
    user_id = session['user_id']
    mani.insert_course_info(course_code, course_name, course_instructor, course_token)
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(user_id, course_id)
    return json.dumps(class_info)


@app.route('/student_get_class/<course_token>', methods=['GET', 'POST'])
def student_get_class(course_token):
    user_id = session['user_id']
    class_info = mani.fetch_course_info(course_token)
    course_id = class_info['course_id']
    mani.insert_enrollment_info(user_id, course_id)
    print(class_info)
    return json.dumps(class_info)


@app.route('/teacher_view_answer/<question>', methods=['GET', 'POST'])
def teacher_view_answer(question):
    question_info = mani.fetch_question_info(question)
    answer_list = mani.fetch_answer_list(question)
    # answer_list = [{'answer_user': 'student1', 'answer_content': 'This is sample answer0'},
    #                 {'answer_user': 'student2', 'answer_content': 'This is sample answer1 This is sample answer0 This is sample answer0 This is sample answer0 This is sample answer0'},
    #                 {'answer_user': 'student3', 'answer_content': 'This?'},]
    per_ans = {'answered': 12, 'not_answered': 35}
    return render_template('teacher_view_answer.html', question_info=question_info, answer_list=answer_list, per_ans=per_ans)


if __name__ == '__main__':
    app.run(debug=True)
