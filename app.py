from flask import Flask, request, render_template, abort, flash, url_for, redirect
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
        print(input_email, input_pw)
        if mani.user_verification(input_email, input_pw):
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if mani.user_is_student(input_email):
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


@app.route('/teacher_main', methods=['GET', 'POST'])
def teacher_main():
    return render_template('teacher_main.html')


@app.route('/student_main_page', methods=['GET', 'POST'])
def student_main():
    return render_template('student_main_page.html')


@app.route('/student_within_course/<classcode>', methods=['GET', 'POST'])
def atudent_within_course(classcode):
    return render_template('student_within_course.html')


@app.route('/student_get_class/<password>', methods=['GET', 'POST'])
def student_get_class(password):
    # param = request.get_data()
    # print(param)
    print('token', password)
    classinfo = mani.fetch_course_info(password)
    return json.dumps(classinfo)


if __name__ == '__main__':
    app.run(debug=True)
