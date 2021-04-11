# -*- coding: utf-8 -*-

from db.database import Database


class Sql:
    def __init__(self):
        self.db = Database()

    def insert_account(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`account`
                    (`user_name`, `first_name`, `last_name`, `email`, `SID`, `password`, `is_student`, `activated`, `token`)
                    VALUES
                    (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(SID)s, %(password)s, %(is_student)s, %(activated)s, %(token)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def update_account_activated(self, user_id):
        statement = '''
                    UPDATE `WeCoupon`.`account`
                    SET activated = 1
                    WHERE user_id = {};
                    '''.format(user_id)
        self.db.execute_mysql(statement)

    def insert_course(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`course`
                    (`course_code`, `course_name`, `course_instructor`, `course_token`)
                    VALUES
                    (%(course_code)s, %(course_name)s, %(course_instructor)s, %(course_token)s);
                    '''
        self.db.single_write_into_mysql(data, statement)
    
    def insert_enrollment(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`enrollment`
                    (`user_id`, `course_id`)
                    VALUES
                    (%(user_id)s, %(course_id)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def insert_question(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`question`
                    (`owner_id`, `course_id`, `q_title`, `q_content`, `q_answer`, `q_status`)
                    VALUES
                    (%(owner_id)s, %(course_id)s, %(q_title)s, %(q_content)s, %(q_answer)s, %(q_status)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def update_question(self, q_id, col, data):
        statement = '''
                    UPDATE `WeCoupon`.`question`
                    SET {} = '{}'
                    WHERE q_id = {};
                    '''.format(col, data, q_id)
        self.db.execute_mysql(statement)

    def update_question_status(self, q_id, q_status):
        statement = '''
                    UPDATE `WeCoupon`.`question`
                    SET q_status = '{}'
                    WHERE q_id = {};
                    '''.format(q_status, q_id)
        self.db.execute_mysql(statement)

    def insert_answer(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`answer`
                    (`q_id`, `student_id`, `a_content`, `a_status`, `a_time`)
                    VALUES
                    (%(q_id)s, %(student_id)s, %(a_content)s, %(a_status)s, %(a_time)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def update_answer_status(self, a_id, a_status):
        statement = '''
                    UPDATE `WeCoupon`.`answer`
                    SET a_status = '{}'
                    WHERE a_id = {};
                    '''.format(a_status, a_id)
        self.db.execute_mysql(statement)

    def insert_coupon(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`coupon`
                    (`student_id`, `course_id`, `is_used`, `insert_time`, `note`)
                    VALUES
                    (%(student_id)s, %(course_id)s, %(is_used)s, %(insert_time)s, %(note)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def update_coupon(self, coupon_id):
        statement = '''
                    UPDATE `WeCoupon`.`coupon`
                    SET is_used = 1
                    WHERE id = {};
                    '''.format(coupon_id)
        self.db.execute_mysql(statement)

    def read_registered_email(self):
        statement = '''
                    SELECT distinct email
                    FROM `WeCoupon`.`account`;
                    '''
        return self.db.read_from_mysql(statement)

    def read_account_info_by_email(self, email, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.account WHERE email='{}';'''.format(col, email)
        return self.db.read_from_mysql(statement)

    def read_account_info_by_token(self, token, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.account WHERE token='{}';'''.format(col, token)
        return self.db.read_from_mysql(statement)

    def read_account_info_by_id(self, user_id, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.account WHERE user_id='{}';'''.format(col, user_id)
        return self.db.read_from_mysql(statement)

    def read_course_info_by_id(self, course_id, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.course WHERE course_id='{}';'''.format(col, course_id)
        return self.db.read_from_mysql(statement)

    def read_all_course_token(self):
        statement = '''
                    SELECT distinct course_token
                    FROM WeCoupon.course;
                    '''
        return self.db.read_from_mysql(statement)

    def read_course_info(self, token):
        statement = '''SELECT * FROM WeCoupon.course WHERE course_token='{}';'''.format(token)
        return self.db.read_from_mysql(statement)

    def read_user_course(self, user_id):
        statement = '''
                    SELECT c.course_id, c.course_code, course_name, course_instructor 
                    FROM WeCoupon.enrollment AS e
                    JOIN Wecoupon.course AS c ON e.course_id = c.course_id
                    WHERE user_id = '{}'
                    '''.format(user_id)
        return self.db.read_from_mysql(statement)

    def read_max_question_id(self):
        statement = '''SELECT max(q_id) FROM WeCoupon.question'''
        return self.db.read_from_mysql(statement)

    def read_question_info_by_id(self, q_id, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.question WHERE q_id='{}';'''.format(col, q_id)
        return self.db.read_from_mysql(statement)

    def read_question_info(self, q_id):
        statement = '''
                    SELECT c.course_id, course_code, q_title, q_content
                    FROM WeCoupon.question q
                    JOIN WeCoupon.course c ON c.course_id = q.course_id 
                    WHERE q_id='{}';'''.format(q_id)
        return self.db.read_from_mysql(statement)

    def read_question_info_by_account(self, user_id, course_id):
        statement = '''
                    SELECT q_id, course_code, q_title, q_content, q_answer, q_status
                    FROM WeCoupon.question q
                    JOIN WeCoupon.course c ON c.course_id = q.course_id 
                    WHERE owner_id='{}' AND c.course_id='{}';'''.format(user_id, course_id)
        return self.db.read_from_mysql(statement)

    def read_open_question(self, course_id):
        statement = '''
                    SELECT q_id FROM WeCoupon.question q
                    WHERE q.course_id = {} and q_status = 'O';
        '''.format(course_id)
        return self.db.read_from_mysql(statement)

    def read_answer_list(self, q_id):
        statement = '''
                    SELECT a_id, user_id, user_name, a_content, a_status
                    FROM WeCoupon.answer an
                    JOIN WeCoupon.account ac ON ac.user_id = an.student_id 
                    WHERE q_id='{}';'''.format(q_id)
        return self.db.read_from_mysql(statement)

    def read_course_enrolled_users(self, course_id):
        statement = '''
                    SELECT DISTINCT e.user_id
                    FROM WeCoupon.enrollment AS e
                    JOIN WeCoupon.account AS a ON e.user_id = a.user_id
                    WHERE e.course_id = '{}' AND is_student = 1;
                    '''.format(course_id)
        return self.db.read_from_mysql(statement)

    def read_attempt_count(self, course_id, user_id):
        statement = '''
                    SELECT count(*)
                    FROM WeCoupon.answer AS an
                    JOIN WeCoupon.question AS q ON q.q_id = an.q_id
                    WHERE an.q_id IN (SELECT q.q_id FROM WeCoupon.question WHERE course_id='{}') 
                    AND an.student_id = '{}';
                    '''.format(course_id, user_id)
        return self.db.read_from_mysql(statement)

    def read_unused_coupon_id(self, user_id, course_id):
        statement = '''
                    SELECT min(id)
                    FROM WeCoupon.coupon
                    WHERE student_id='{}'AND course_id='{}' AND is_used=0;
                    '''.format(user_id, course_id)
        return self.db.read_from_mysql(statement)

    def read_coupon_info(self, user_id, course_id):
        statement = '''
                    SELECT count(*)
                    FROM WeCoupon.coupon
                    WHERE student_id='{}'AND course_id='{}';
                    '''.format(user_id, course_id)
        return self.db.read_from_mysql(statement)

    def read_used_coupon_info(self, user_id, course_id):
        statement = '''
                    SELECT count(*)
                    FROM WeCoupon.coupon
                    WHERE student_id='{}'AND course_id='{}' AND is_used = 1;
                    '''.format(user_id, course_id)
        return self.db.read_from_mysql(statement)

    def read_ans_num(self, q_id):
        statement = '''
                    SELECT count(distinct student_id)
                    FROM WeCoupon.answer
                    WHERE q_id = '{}';
                    '''.format(q_id)
        return self.db.read_from_mysql(statement)

    def read_student_participation(self, user_id, course_id):
        statement = '''
                    SELECT q.q_title, q.q_content, a.a_content, q.q_answer, a.a_status
                    FROM WeCoupon.answer AS a
                    JOIN WeCoupon.question AS q ON q.q_id = a.q_id
                    WHERE a.student_id = {} AND q.course_id = course_id = {} AND q.q_status = 'N';
                    '''.format(user_id, course_id)
        return self.db.read_from_mysql(statement)


if __name__ == "__main__":
    s = Sql()
    print(s.read_coupon_info(1))
