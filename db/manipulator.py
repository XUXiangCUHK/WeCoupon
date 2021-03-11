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

    def insert_question_info(self, owner_id, course_id, q_title, q_content, q_answer, q_status):
        data = {
            'owner_id': owner_id,
            'course_id': course_id,
            'q_title': q_title,
            'q_content': q_content,
            'q_answer': q_answer,
            'q_status': q_status,
        }
        self.sql.insert_question(data)

    def insert_answer_info(self, q_id, student_id, a_content, a_status):
        data = {
            'q_id': q_id,
            'student_id': student_id,
            'a_content': a_content,
            'a_status': a_status,
        }
        self.sql.insert_answer(data)

    def user_enrollment(self, user_id):
        enroll_info = list()
        res = self.sql.read_user_course(user_id)
        for item in res:
            enroll_info.append({
                'course_id': item[0],
                'code': item[1],
                'title': item[2],
                'info': item[3]
            })
        return enroll_info

    def user_verification(self, email, password):
        pw = self.sql.read_account_info_by_email(email, ['password'])
        if pw:
            if pw[0][0] == password:
                return True
        return False

    def fetch_user_info_by_email(self, email, cols):
        res = self.sql.read_account_info_by_email(email, cols)
        return res[0][0]

    def fetch_course_info(self, token):
        res = self.sql.read_course_info(token)
        if not res:
            return dict()
        course_info = {
            'course_id': res[0][0],
            'course_code': res[0][1],
            'course_name': res[0][2],
            'course_instructor': res[0][3]
        }
        return course_info

    def fetch_question_info(self, q_id):
        res = self.sql.read_question_info(q_id)
        if not res:
            return dict()
        question_info = {
            'corresponding_course': res[0][0],
            'question_name': res[0][1],
            'question_content': res[0][2],
        }
        return question_info

    def fetch_question_info_by_account(self, user_id, course_id):
        res = self.sql.read_question_info_by_account(user_id, course_id)
        new_question_list = list()
        old_question_list = list()
        if not res:
            return new_question_list, old_question_list
        for item in res:
            q = {
                'q_id': item[0],
                'course_code': item[1],
                'q_title': item[2],
                'q_content': item[3],
                'q_answer': item[4],
                'question_id': item[2],
                'question_type': item[4]
            }
            if item[5] == 'A':
                new_question_list.append(q)
            elif item[5] == 'N':
                old_question_list.append(q)
        return new_question_list, old_question_list

    def fetch_answer_list(self, q_id):
        res = self.sql.read_answer_list(q_id)
        answer_list = list()
        if not res:
            return answer_list
        for item in res:
            answer_list.append({
                'answer_user': item[0],
                'answer_content': item[1],
            })
        return answer_list


if __name__ == "__main__":
    m = Manipulator()
    # m.insert_account_info('StevenXU', 'xu', 'xiang', '1155107785@link.cuhk.edu.hk', '1155107785', 'wecoupon', '1')
    # m.insert_course_info('CSCI3100', 'Software Engineering', 'Prof. Michael R. Lyu', 'software')
    # m.insert_course_info('IERG3310', 'Computer Networking', 'Prof. Xing Guoliang', 'networks')
    # m.insert_course_info('FTEC3001', 'Financial Innovation & Structured Products', 'Prof. Chen Nan', 'FinTech0')
    # m.insert_enrollment_info('StevenXU', 'CSCI3100')
    # m.insert_enrollment_info('StevenXU', 'IERG3310')
    # m.insert_enrollment_info('3', '1')

    # m.user_enrollment('StevenXU')
    # res = m.user_verification('1155107785@link.cuhk.edu.hk', 'wecoupon')
    # print('res,', res)
    # res = m.user_is_student('1155107785@link.cuhk.edu.hk')
    m.insert_question_info(3, 1, 'Question5', 'What are s/w principles?', 'explosive states', 'N')
    # m.insert_answer_info(1, 1, 'hard to implement', 0)
    # m.insert_answer_info(1, 2, 'explosive states', 0)
    # print(m.fetch_question_info(1))
    # print(m.fetch_answer_list(1))