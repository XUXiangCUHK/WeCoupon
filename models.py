"""
PROGRAM MAIN APPLICATION - Program to define modules used in main application
PROGRAMMER - XU Xiang (1155107785);
             LAI Wei (1155095200);
             ZENG Meiqi (1155107891);
             ZHANG Yusong(1155107841);
             ZHOU Yifan (1155124411)
CALLING SEQUENCE - The modules will be accessed and used by app.py
VERSION - written on 2021/04/13
PURPOSE - To define three potential modules for clear coding, namely user, course and question
"""

from flask_login import UserMixin
from db.manipulator import Manipulator

mani = Manipulator()


class User(UserMixin):
    def __init__(self, input_email):
        self.user_name = mani.fetch_user_info_by_email(input_email, ['user_name'])
        self.user_id = mani.fetch_user_info_by_email(input_email, ['user_id'])
        self.first_name = mani.fetch_user_info_by_email(input_email, ['first_name'])
        self.last_name = mani.fetch_user_info_by_email(input_email, ['last_name'])
        self.email = mani.fetch_user_info_by_email(input_email, ['email'])
        self.password = mani.fetch_user_info_by_email(input_email, ['password'])
        self.is_student = mani.fetch_user_info_by_email(input_email, ['is_student'])
        self.activated = mani.fetch_user_info_by_email(input_email, ['activated'])

        self.current_course_id = 0
        self.current_course = dict()
        self.current_q_id = 0
        self.current_q = dict()

        self.token = str()

    def get_id(self):
        return self.email

    @staticmethod
    def get(user_email):
        if not user_email:
            return None
        return User(user_email)

    def activate(self, token):
        if token == self.token:
            self.activated = 1
            return True
        else:
            return False

    def fill_course_info(self):
        self.current_course = Course(self.current_course_id)

    def fill_question_info(self):
        self.current_q = Question(self.current_q_id)


class Course:
    def __init__(self, course_id):
        self.course_id = course_id
        self.course_code = mani.fetch_course_info_by_id(course_id, ['course_code'])
        self.course_name = mani.fetch_course_info_by_id(course_id, ['course_name'])
        self.course_instructor = mani.fetch_course_info_by_id(course_id, ['course_instructor'])
        self.course_token = mani.fetch_course_info_by_id(course_id, ['course_token'])


class Question:
    def __init__(self, q_id):
        self.q_id = q_id
        self.owner_id = mani.fetch_question_info_by_id(q_id, ['owner_id'])
        self.course_id = mani.fetch_question_info_by_id(q_id, ['course_id'])
        self.q_title = mani.fetch_question_info_by_id(q_id, ['q_title'])
        self.q_content = mani.fetch_question_info_by_id(q_id, ['q_content'])
        self.q_answer = mani.fetch_question_info_by_id(q_id, ['q_answer'])
        self.q_status = mani.fetch_question_info_by_id(q_id, ['q_status'])
