from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, NoneOf
from flask_pagedown.fields import PageDownField

from db.manipulator import Manipulator
mani = Manipulator()


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    SID = StringField('SID', validators=[Length(10),
                                         Regexp('^[0-9]*$', 0, 'SID requires 10 numbers')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email(),
                                             NoneOf(mani.fetch_registerd_email(),
                                                    'The email has already been registered.')])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    isInstructor = BooleanField('I am an instructor')
    submit = SubmitField('Sign Up')


class CreateClassForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    course_title = StringField('Course Title', validators=[DataRequired()])
    course_instructor = StringField('Course Instructor', validators=[DataRequired()])
    course_token = StringField('Course Token', validators=[DataRequired(),
                                                           NoneOf(mani.fetch_all_course_token(),
                                                                  'The token is occupied by others.')])
    submit = SubmitField('Create Course')


class AddQuestionForm(FlaskForm):
    question_title = StringField('Question Title', validators=[DataRequired()])
    question_content = PageDownField('Question Content', validators=[DataRequired()])
    question_answer = PageDownField('Suggested Answer', validators=[DataRequired()])
    submit = SubmitField('Create Question')


class EditQuestionForm(FlaskForm):
    question_title = StringField('Question Title', validators=[DataRequired()])
    question_content = PageDownField('Question Content', validators=[DataRequired()])
    question_answer = PageDownField('Suggested Answer', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class AddAnswer(FlaskForm):
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'onclick': 'alert("submitted!")'})


class RegClass(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Register')