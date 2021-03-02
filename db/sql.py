# -*- coding: utf-8 -*-

from db.database import Database


class Sql:
    def __init__(self):
        self.db = Database()

    def insert_account(self, data):
        statement = '''
                    INSERT IGNORE INTO `WeCoupon`.`account`
                    (`user_name`, `first_name`, `last_name`, `email`, `SID`, `password`, `is_student`, `activated`)
                    VALUES
                    (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(SID)s, %(password)s, %(is_student)s, %(activated)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

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

    def read_account_info_by_email(self, email, column_list):
        col = ', '.join(column_list)
        statement = '''SELECT {} FROM WeCoupon.account WHERE email='{}';'''.format(col, email)
        return self.db.read_from_mysql(statement)

    def read_course_info(self, token):
        statement = '''SELECT * FROM WeCoupon.course WHERE course_token='{}';'''.format(token)
        return self.db.read_from_mysql(statement)

    def read_user_course(self, user_id):
        statement = '''
                    SELECT c.course_code, course_name, course_instructor 
                    FROM WeCoupon.enrollment AS e
                    JOIN Wecoupon.course AS c ON e.course_id = c.course_id
                    WHERE user_id = '{}'
                    '''.format(user_id)
        return self.db.read_from_mysql(statement)


if __name__ == "__main__":
    pass
