# -*- coding: utf-8 -*-

from db.sql import Sql


class Manipulator:
    def __init__(self):
        self.sql = Sql()

    def insert_account_info(self, user_name, first_name, last_name, email, SID, password, is_student, activated):
        data = {
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'SID': SID,
            'password': password,
            'is_student': is_student,
            'activated': activated
        }
        self.sql.insert_account(data)
    
    def insert_course_info(self, course_code, course_name, course_instructor, course_token):
        data = {
            'course_code': course_code,
            'course_name': course_name,
            'course_instructor': course_instructor,
            'course_token': course_token,
        }
        self.sql.insert_course(data)
    
    def insert_enrollment_info(self, user_id, course_id):
        data = {
            'user_id': user_id,
            'course_id': course_id,
        }
        self.sql.insert_enrollment(data)

    def user_enrollment(self, user_name):
        res = self.sql.read_user_course(user_name)
        return res

    def user_verification(self, email, password):
        pw = self.sql.read_account_info_by_email(email, ['password'])
        if pw:
            if pw[0][0] == password:
                return True
        return False

    def user_is_student(self, email):
        pos = self.sql.read_account_info_by_email(email, ['is_student'])
        return pos[0][0]

    def fetch_course_info(self, token):
        res = self.sql.read_course_info(token)
        if not res:
            return dict()
        course_info = {
            'code': res[0][1],
            'title': res[0][2],
            'info': res[0][3]
        }
        return course_info


if __name__ == "__main__":
    m = Manipulator()
    # m.insert_account_info('StevenXU', 'xu', 'xiang', '1155107785@link.cuhk.edu.hk', '1155107785', 'wecoupon', '1')
    # m.insert_course_info('CSCI3100', 'Software Engineering', 'Prof. Michael R. Lyu', 'software')
    # m.insert_course_info('IERG3310', 'Computer Networking', 'Prof. Xing Guoliang', 'networks')
    # m.insert_course_info('FTEC3001', 'Financial Innovation & Structured Products', 'Prof. Chen Nan', 'FinTech0')
    # m.insert_enrollment_info('StevenXU', 'CSCI3100')
    # m.insert_enrollment_info('StevenXU', 'IERG3310')
    # m.insert_enrollment_info('StevenXU', 'FTEC3001')

    # m.user_enrollment('StevenXU')
    # res = m.user_verification('1155107785@link.cuhk.edu.hk', 'wecoupon')
    # print('res,', res)
    res = m.user_is_student('1155107785@link.cuhk.edu.hk')
    print(res)
