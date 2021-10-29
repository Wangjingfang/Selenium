# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:38:58 2019

@author: Administrator
"""

'''
分别对每个表依次读入并导入数据；要求数据库中本身有该表
注意从业绩合并报告中的数据Date在pandas中读入为object,需要转化成Date格式
数据来源于32 业绩报告清洗后，直接采用此脚本导入到数据中
先在数据删除后需要db.commit()提交，否则一直占用进程，导入无法使用；
业绩报告中business report 后缀名为xlsx,并不是CSV，请注意
2020.6.2已测试成功OK
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os

import warnings

warnings.filterwarnings('ignore')  #忽略警告错误

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8')  #注意此处不能写成utf-8

#数据导入部分
path = input('请输入已清理好要导入的业绩报告的路径：')
if '"' in path:
    path = path.replace('"','')

#获取业绩报告中各路径地址
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))

input_info_df = pd.DataFrame(columns = ['站点','实际导入数据','应该导入数据excel文件长度'])
i = 0

for filename in filenames:    
    business = pd.read_csv(filename)
    business['Date'] = pd.to_datetime(business['Date'])
    min_date = min(business['Date'])
    length = len(business)
    
    station = filename.split('\\')[-1].split('.')[0][0:6].lower()  #所有站点全部小写
    db_table = station + '_y' 
    
    print('当前导入站点为：%s'%station)
    
    #删除大于min_date的数据
    db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'ad_mysql')
    cursor = db.cursor()
    cursor.execute('delete from `%s` where Date >= "%s" '%(db_table,min_date))
    db.commit()                  #此处一定要先提交，否则由于进程占用导致全部锁死
    print('历史数据删除成功;')
    
    try:
        business.to_sql(db_table,connect,index = False,if_exists = 'append')
        print('业绩报告导入mysql成功，请在数据库中检查；')
    except Exception as e:
        print('导入出错，出错原因为',e)
        
    print('要导入的业绩报告的数量为%d'%length)
    print('业绩报告中时间最小为%s'%min_date)

    #数据检查部分，检查是否完全导入
    cursor_check = db.cursor()
    cursor_check.execute('select count(*) from `%s` where Date >= "%s" '%(db_table,min_date)) #此处通过将%s双引号即可完成在SQL中的引用
    data = cursor_check.fetchall()  #data返回的是一个多元元组，采用元组取数将其取出
    
    if data[0][0] == length:
        print('数据导入正确，且检查成功！实际导入为%d,要导入数量为%d'%(data[0][0],length))
    else:
        print('数据导入不一致，请在mysql中进行进一步核实！实际导入为%d,因导入数量为%d'%(data[0][0],length))
        
    print('\n')
    
    input_info_df.loc[i,'站点'] = station    
    input_info_df.loc[i,'实际导入数据'] = data[0][0]
    input_info_df.loc[i,'应该导入数据excel文件长度'] = length
    i += 1

input_path = path + '_导入数据库结果' + '.csv'    
input_info_df.to_csv(input_path,index = False)
print('导入结果请在路径中查看')