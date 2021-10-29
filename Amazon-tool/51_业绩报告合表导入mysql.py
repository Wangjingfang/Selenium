# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:38:58 2019

@author: Administrator
"""

'''
使用前请阅读：
此导入的数据库为c_py,请谨慎导入，出错很麻烦;
注意从业绩合并报告中的数据Date在pandas中读入为object,需要转化成Date格式
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/c_py?charset=utf8')  #注意此处不能写成utf-8

#数据导入部分
path = input('请输入已合并要导入的业绩报告的路径：')
if '"' in path:
    path = path.replace('"','')
    
business = pd.read_csv(path)
business['Date'] = pd.to_datetime(business['Date'])
min_date = min(business['Date'])
length = len(business)

db_table = 'business_report'   #请输入想导入的数据库的表名称，若没有的话，数据库会新建

try:
    business.to_sql(db_table,connect,index = False,if_exists = 'append')
    print('业绩报告导入mysql成功，请在数据库中检查；')
except Exception as e:
    print('导入出错，出错原因为',e)

print('\n')
print('要导入的业绩报告的数量为%d'%length)
print('业绩报告中时间最小为%s'%min_date)

#数据检查部分，检查是否完全导入
db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'c_py')
cursor = db.cursor()
cursor.execute('select count(*) from %s where date >= "%s" '%(db_table,min_date)) #此处通过将%s双引号即可完成在SQL中的引用
data = cursor.fetchall()  #data返回的是一个多元元组，采用元组取数将其取出

if data[0][0] == length:
    print('数据导入正确，且检查成功！实际导入为%d,要导入数量为%d'%(data[0][0],length))
else:
    print('数据导入不一致，请在mysql中进行进一步核实！实际导入为%d,因导入数量为%d'%(data[0][0],length))

