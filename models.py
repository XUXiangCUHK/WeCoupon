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


class Course:
    def __init__(self):
        self.course_id = 0
        self.course_code = str()
        self.course_name = str()
        self.course_instructor = str()
        self.course_token = str()


class Question:
    def __init__(self):
        self.q_id = 0
        self.owner_id = 0
        self.course_id = 0
        self.q_title = str()
        self.q_content = str()
        self.q_answer = str()
        self.q_status = str()


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
