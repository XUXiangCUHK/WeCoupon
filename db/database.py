# -*- coding: utf-8 -*-

import json
import pymysql
from contextlib import closing

class Database:
    def __init__(self):
        self.mysql_host = '127.0.0.1'
        self.mysql_port = 3306
        self.mysql_user = 'root'
        self.mysql_password = 'xuxiang19980917'
    
    def read_from_mysql(self, statement):
        mysql_connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_password)
        with closing(mysql_connection.cursor()) as cursor:
            cursor.execute(statement)
            select_query_result = cursor.fetchall()
        mysql_connection.close()
        return select_query_result

    def single_write_into_mysql(self, data, statement):
        if data:
            mysql_connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_password)
            with closing(mysql_connection.cursor()) as cursor:
                cursor.execute(statement, data)
                mysql_connection.commit()
            mysql_connection.close()

    def multiple_write_into_mysql(self, data, statement):
        if data:
            mysql_connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_password)
            with closing(mysql_connection.cursor()) as cursor:
                cursor.executemany(statement, data)
                mysql_connection.commit()
            mysql_connection.close()
    
    def execute_mysql(self, statement):
        mysql_connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_password)
        with closing(mysql_connection.cursor()) as cursor:
            cursor.execute(statement)
            mysql_connection.commit()
        mysql_connection.close()