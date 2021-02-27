# -*- coding: utf-8 -*-

import json
from database import Database

class Sql:
    def __init__(self):
        self.db = Database()

    def insert_account(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`account`
                    (`user_name`, `first_name`, `last_name`, `email`, `SID`, `password`, `is_student`)
                    VALUES
                    (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(SID)s, %(password)s, %(is_student)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def insert_course(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`course`
                    (`course_id`, `course_name`, `course_instructor`, `course_token`)
                    VALUES
                    (%(course_id)s, %(course_name)s, %(course_instructor)s, %(course_token)s);
                    '''
        self.db.single_write_into_mysql(data, statement)
    
    def insert_enrollment(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`enrollment`
                    (`user_name`, `course_id`)
                    VALUES
                    (%(user_name)s, %(course_id)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

    def read_user_course(self, user_name):
        statement = '''
                    SELECT c.course_id, course_name, course_instructor 
                    FROM WeCoupon.enrollment AS e
                    JOIN Wecoupon.course AS c ON e.course_id = c.course_id
                    WHERE user_name = '{}'
                    '''.format(user_name)
        return self.db.read_from_mysql(statement)

if __name__ == "__main__":
    e = Sql()
    write_info = {
            'user_name': 'zhou',
            'passward': 'zhou',
            'email': '1155107785@link.cuhk.edu.hk',
            'pos': 'S'
        }
    e.insert_account(write_info)