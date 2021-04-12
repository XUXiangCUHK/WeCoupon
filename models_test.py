from db.manipulator import Manipulator
from flask_login import UserMixin
# from app_test import login_manager
from flask import current_app
import random

mani = Manipulator()


class User(UserMixin):
    def __init__(self, input_email):
        if input_email == 'teacher@gmail.com':
            self.username = 'Michael'
            self.user_id = '1'
            self.first_name = 'Michael'
            self.last_name = 'Prof'
            self.email = 'teacher@gmail.com'
            self.password = '1'
            self.is_student = '0'
            self.token = ''
            self.activated = '1'
        else:
            self.username = 'Amy'
            self.user_id = '2'
            self.first_name = 'Alen'
            self.last_name = 'XU'
            self.SID = '1234567890'
            self.email = input_email
            self.password = '1'
            self.is_student = '1'
            self.token = ''
            self.activated = '1'

        self.current_course_id = str()
        self.current_course = dict()
        self.current_q_id = 0
        self.current_q = dict()


    def get_id(self):
        return self.user_id

    def generate_random_token(self):
        token = ''.join(str(random.choice(range(10))) for _ in range(6))
        self.token = token
        return token

    def activate(self, token):
        if token == self.token:
            self.activated = '1'
            return True
        else:
            return False

    def fill_course_info(self):
        self.current_course = Course(self.current_course_id)

    def fill_question_info(self):
        self.current_q = Question(self.current_q_id)

class Course:
    def __init__(self, classcode):

        enroll_info = [
            {'course_id': 1, 'code': 'CSCI3100', 'title': 'Software Engineering', 'course_instructor': 'Prof. Michael R. Lyu'},
            {'course_id': 3, 'code': 'IERG3310', 'title': 'Computer Networking', 'course_instructor': 'Prof. Xing Guoliang'},
            {'course_id': 7, 'code': 'CSCI2001', 'title': 'Data Structure', 'course_instructor': 'Prof. Michael R. Lyu'},
            {'course_id': 4, 'code': 'ESTR4999', 'title': 'Graduation Thesis', 'course_instructor': 'Prof. Michael R. Lyu'},
            {'course_id': 5, 'code': 'ESTR4998', 'title': 'Graduation Thesis', 'course_instructor': 'Prof. Michael R. Lyu'}]

        for i in enroll_info:
            # print("debug: ", i['course_id'],type(i['course_id']), classcode, type(classcode))
            if str(i['course_id']) == str(classcode):
                self.course_id = i['course_id']
                self.course_code = i['code']
                self.course_name = i['title']
                self.course_instructor = i['course_instructor']



class Question:
    def __init__(self, q_id):
        question_list = [{'question_id': 'default', 'course_id': 4, 'question_title': 'default question', 'q_content': 'def', 'question_type': 'Type', 'q_status': '0'},
                        {'question_id': 1, 'course_id': 4, 'question_title': 'question#4', 'q_content': 'test1', 'question_type': 'MC', 'q_status': '0'},
                         {'question_id': 2, 'course_id': 4, 'question_title': 'question#5', 'q_content': 'test2', 'question_type': 'Type', 'q_status': '0'},
                         {'question_id': 3, 'course_id': 4, 'question_title': 'question#1', 'q_content': 'test3', 'question_type': 'MC', 'q_status': '2'},
                         {'question_id': 4, 'course_id': 4, 'question_title': 'question#2', 'q_content': 'test4', 'question_type': 'Type', 'q_status': '2'},
                         {'question_id': 5, 'course_id': 4, 'question_title': 'question#3', 'q_content': 'test5', 'question_type': 'Type', 'q_status': '2'},
                         {'question_id': 123, 'course_id': 4, 'question_title': 'question#6', 'q_content': 'test6', 'question_type': 'Short', 'q_status': '2'},
                         {'question_id': 999, 'course_id': 4, 'question_title': 'test answer', 'q_content': 'you can input answer below', 'question_type': 'type', 'q_status': '1'}]

        # q_status: 0: unused; 1: ongoing; 2: used
        for i in question_list:
            if str(i['question_id']) == str(q_id):
                self.q_id = i['question_id']
                self.course_id = i['course_id']
                self.q_title = i['question_title']
                self.q_content = i['q_content']
                self.q_status = i['q_status']


class Answer:
    def __init__(self):
        self.a_id = 0
        self.q_id = 0
        self.student_id = 0
        self.a_content = str()
        self.a_status = 0
        self.a_time = 0

class Coupon:
    def __init__(self):
        self.id = 0
        self.student_id = 0
        self.coupon_num = 0
        self.insert_time = 0
        self.note = str()
