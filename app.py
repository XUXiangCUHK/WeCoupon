from flask import Flask, request, render_template, abort, flash, url_for, redirect
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
# from email import send_email
import json
from db.manipulator import Manipulator

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='hard to guess string'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #print(form)
        user = form   # testing
        user.pos = "Instructor"   # testing
        print(user)
        # db query user details
        # To be filled
        '''
        if form.password.data == "111":   # pw verify
            next = request.args.get('next')
            print(next)
            if next is None or not next.startswith('/'):
                if user.pos == "Student":
                    next = url_for('student_main')
                elif user.pos == "Instructor":
                    next = url_for('teacher_main')
            return redirect(next)
        '''
        if user is not None and user.verify_password(form.password.data):  # to be modified
            # login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if user.pos == "Student":
                    next = url_for('student_main_page')
                elif user.pos == "Instructor":
                    next = url_for('teacher_main')
            return redirect(next)
        flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    '''
    if form.validate_on_submit():
        if form.isInstructor.data:
            pos = 'Instructor'
        else:
            pos = 'Student'
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    SID=form.SID.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role=pos)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        print(token)
        # send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('login'))
    '''
    if form.validate_on_submit():
        print(form,type(form))

        if form.isInstructor.data:
            pos = 0
        else:
            pos = 1
        print(pos)
        # db insert new user
        new = Manipulator()
        new.insert_account_info(form.username.data,
                                form.last_name.data,
                                form.first_name.data,
                                form.email.data,
                                form.SID.data, pos)
        # email verification

        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

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
    param = request.get_data()
    print(param)
    # get from db
    classinfo = {
        'name': 'csc1231',
        'code': '123456',
        'info':'other'
    }
    return json.dumps(classinfo)


if __name__ == '__main__':
    app.run(debug=True)
