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
