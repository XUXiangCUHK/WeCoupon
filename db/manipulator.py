# -*- coding: utf-8 -*-

import json
from sql import Sql

class Manipulator:
    def __init__(self):
        self.sql = Sql()

    def insert_account_info(self, user_name, passward, email, pos):
        data = {
            'user_name': user_name,
            'passward': passward,
            'email': email,
            'pos': pos
        }
        self.sql.insert_account(data)
        

if __name__ == "__main__":
    m = Manipulator()
    m.insert_account_info('3100', '3100', '1155107785@link.cuhk.edu.hk', 'T')