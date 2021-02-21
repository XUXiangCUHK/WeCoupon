# -*- coding: utf-8 -*-

import json
from database import Database

class Sql:
    def __init__(self):
        self.db = Database()

    def insert_account(self, data):
        statement = '''
                    INSERT IGNORE INTO `test`.`account`
                    (`user_name`, `passward`, `email`, `pos`)
                    VALUES
                    (%(user_name)s, %(passward)s, %(email)s, %(pos)s);
                    '''
        self.db.single_write_into_mysql(data, statement)

if __name__ == "__main__":
    e = Sql()
    write_info = {
            'user_name': 'zhou',
            'passward': 'zhou',
            'email': '1155107785@link.cuhk.edu.hk',
            'pos': 'S'
        }
    e.insert_account(write_info)