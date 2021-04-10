# -*- coding: utf-8 -*-

import datetime
from db.sql import Sql


class Manipulator:
    def __init__(self):
        self.sql = Sql()

    def insert_account_info(self, user_name, first_name, last_name, email, SID, password, is_student, activated, token):
        data = {
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'SID': SID,
            'password': password,
            'is_student': is_student,
            'activated': activated,
            'token': token
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
            'a_time': int(datetime.datetime.now().timestamp())
        }
        self.sql.insert_answer(data)

    def insert_coupon_info(self, student_id, course_id, is_used, note):
        data = {
            'student_id': student_id,
            'course_id': course_id,
            'is_used': is_used,
            'insert_time': int(datetime.datetime.now().timestamp()),
            'note': note
        }
        self.sql.insert_coupon(data)

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

    def fetch_registerd_email(self):
        email_list = list()
        res = self.sql.read_registered_email()
        for item in res:
            email_list.append(item[0])
        return email_list

    def fetch_user_info_by_email(self, email, cols):
        res = self.sql.read_account_info_by_email(email, cols)
        if res:
            return res[0][0]
        else:
            return str()

    def fetch_user_info_by_token(self, token, cols):
        res = self.sql.read_account_info_by_token(token, cols)
        if res:
            return res[0][0]
        else:
            return str()

    def fetch_user_info_by_id(self, user_id, cols):
        res = self.sql.read_account_info_by_id(user_id, cols)
        if res:
            return res[0][0]
        else:
            return str()

    def fetch_all_course_token(self):
        token_list = list()
        res = self.sql.read_all_course_token()
        for item in res:
            token_list.append(item[0])
        return token_list

    def fetch_course_info_by_id(self, course_id, cols):
        res = self.sql.read_course_info_by_id(course_id, cols)
        if res:
            return res[0][0]
        else:
            return str()

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

    def fetch_question_info_by_id(self, q_id, cols):
        res = self.sql.read_question_info_by_id(q_id, cols)
        if res:
            return res[0][0]
        else:
            return str()

    def fetch_question_info(self, q_id):
        res = self.sql.read_question_info(q_id)
        if not res:
            return dict()
        question_info = {
            'course_id': res[0][0],
            'corresponding_course': res[0][1],
            'question_name': res[0][2],
            'question_content': res[0][3],
        }
        return question_info

    def fetch_question_info_by_account(self, user_id, course_id):
        res = self.sql.read_question_info_by_account(user_id, course_id)
        new_question_list = list()
        old_question_list = list()
        if not res:
            return new_question_list, old_question_list
        for item in res:
            q_content = item[3]
            if len(item[3]) > 30:
                q_content = item[3][:30] + '...'
            q = {
                'q_id': item[0],
                'course_code': item[1],
                'q_title': item[2],
                'q_content': q_content,
                'q_answer': item[4],
                'question_id': item[0],
                'question_title': item[2],
                'question_type': q_content
            }
            if item[5] == 'A':
                new_question_list.append(q)
            elif item[5] == 'N':
                old_question_list.append(q)
        return new_question_list, old_question_list

    def fetch_open_question(self, course_id):
        res = self.sql.read_open_question(course_id)
        if res:
            return res[0][0]
        else:
            return 0

    def fetch_answer_list(self, q_id):
        res = self.sql.read_answer_list(q_id)
        answer_list = list()
        if not res:
            return answer_list
        for item in res:
            answer_list.append({
                'answer_id': item[0],
                'answer_userid': item[1],
                'answer_user': item[2],
                'answer_content': item[3],
                'status': item[4]
            })
        return answer_list

    def fetch_participation(self, course_id):
        participation_list = list()
        res = self.sql.read_course_enrolled_users(course_id)
        for item in res:
            user_id = item[0]
            student_id = self.fetch_user_info_by_id(user_id, ['SID'])
            first_name = self.fetch_user_info_by_id(user_id, ['first_name'])
            last_name = self.fetch_user_info_by_id(user_id, ['last_name'])
            attempt = self.fetch_attempt_num(course_id, user_id)
            coupon_num = self.fetch_coupon_num(user_id, course_id)
            used_coupon_num = self.fetch_used_coupon_num(user_id, course_id)
            participation_list.append({
                'user_id': user_id,
                'student_id': student_id,
                'student_name': '{} {}'.format(first_name, last_name),
                'attempt': attempt,
                'coupon_rewarded': coupon_num,
                'coupon_used': used_coupon_num,
            })
        return participation_list

    def mark_coupon_as_used(self, user_id, course_id):
        coupon_id = self.sql.read_unused_coupon_id(user_id, course_id)[0][0]
        self.sql.update_coupon(coupon_id)

    def fetch_coupon_num(self, user_id, course_id):
        res = self.sql.read_coupon_info(user_id, course_id)
        if not res:
            return 0
        return res[0][0]

    def fetch_used_coupon_num(self, user_id, course_id):
        res = self.sql.read_used_coupon_info(user_id, course_id)
        if not res:
            return 0
        return res[0][0]

    def fetch_attempt_num(self, course_id, user_id):
        res = self.sql.read_attempt_count(course_id, user_id)
        if not res:
            return 0
        return res[0][0]

    def fetch_per_ans(self, course_id, q_id):
        answered = 0
        per_ans = dict()
        res = self.sql.read_ans_num(q_id)
        if res:
            answered = res[0][0]

        users = self.sql.read_course_enrolled_users(course_id)
        total_num = len(users)
        if total_num > answered:
            not_answered = total_num - answered
        else:
            not_answered = 0

        per_ans['answered'] = answered
        per_ans['not_answered'] = not_answered
        return per_ans

    def fetch_student_participation(self, user_id, course_id):
        res = self.sql.read_student_participation(user_id, course_id)
        answer_list = list()
        for item in res:
            answer_list.append({
                'question_title': item[0],
                'question_content': item[1],
                'question_answer': item[2],
                'correct_answer': item[3],
                'get_coupon_or_not': item[4],
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
    m.insert_enrollment_info('3', '1')

    # m.user_enrollment('StevenXU')
    # res = m.user_verification('1155107785@link.cuhk.edu.hk', 'wecoupon')
    # print('res,', res)
    # res = m.user_is_student('1155107785@link.cuhk.edu.hk')
    # m.insert_question_info(3, 1, 'Question5', 'What are s/w principles?', 'explosive states', 'N')
    # m.insert_answer_info(21, 2, 'hard to answer testing', 0)
    # m.insert_answer_info(1, 2, 'explosive states', 0)
    # print(m.fetch_question_info(1))
    # print(m.fetch_answer_list(1))
    # m.fetch_participation(1, 0, 'initial')
    # print(m.fetch_participation(1))
    # print(m.fetch_coupon_num(1))
    # print(m.fetch_participation(1))
