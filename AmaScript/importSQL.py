from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')  #忽略警告错误

# connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8mb4')  #注意此处不能写成utf-8

connection = pymysql.connect(host= 'localhost', #host属性
                             user= 'root',  # 用户名
                             passwd= 'P@ssw0rd123',  # 登录数据库的密码
                             db = 'amadata'   # 数据库名
                             )
cur = connection.cursor()

tables = cur.execute('show tables')
for table in tables:
    print(table)
# print(tables)