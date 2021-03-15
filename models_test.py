from db.manipulator import Manipulator
from flask_login import UserMixin
# from app_test import login_manager
from flask import current_app
import random

mani = Manipulator()


class User():
    def __init__(self,input_email):
        if input_email == 'teacher@gmail.com':
            self.username = 'Michael'
            self.user_id = '1'
            self.first_name = 'One'
            self.last_name = 'T'
            self.email = 'teacher@gmail.com'
            self.password = '1'
            self.is_student = '0'
            self.token = ''
            self.activated = '1'
        else:
            self.username = 'Amy'
            self.user_id = '2'
            self.first_name = 'One'
            self.last_name = 'S'
            self.SID = '1234567890'
            self.email = input_email
            self.password = '1'
            self.is_student = '1'
            self.token = ''
            self.activated = '1'

    # user_id = mani.fetch_user_info_by_email(input_email, ['user_id'])
    # first_name = mani.fetch_user_info_by_email(input_email, ['first_name'])
    # last_name = mani.fetch_user_info_by_email(input_email, ['last_name'])
    # SID = mani.fetch_user_info_by_email(input_email, ['SID'])
    # email = mani.fetch_user_info_by_email(input_email, ['email'])
    # password = mani.fetch_user_info_by_email(input_email, ['password'])
    # is_student = mani.fetch_user_info_by_email(input_email, ['is_student'])
    # token = mani.fetch_user_info_by_email(input_email, ['token'])
    # activated = mani.fetch_user_info_by_email(input_email, ['activated'])

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

    # def activate(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     # change activated=1 in db
    #     return True

