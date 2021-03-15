from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from db.manipulator import Manipulator

mani = Manipulator()


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    SID = StringField('SID', validators=[Length(10),
                                         Regexp('^[0-9]*$', 0, 'SIDs must have 10 numbers')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    isInstructor = BooleanField('I am an instructor')
    submit = SubmitField('Sign Up')

    # def validate_email(self, field):
    #     if mani.fetch_user_info_by_email(field.email, ['user_id']):
    #         raise ValidationError('Email already registered.')


class CreateClassForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    course_title = StringField('Course Title', validators=[DataRequired()])
    course_instructor = StringField('Course Instructor', validators=[DataRequired()])
    course_token = StringField('Course Token', validators=[DataRequired()])
    submit = SubmitField('Create Course')
