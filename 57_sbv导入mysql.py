# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:38:58 2019

@author: Administrator
"""

'''
分别对每个表依次读入并导入数据；要求数据库中本身有该表
注意从搜索词报告中的数据Date在pandas中读入为object,需要转化成Date格式
先在数据删除后需要db.commit()提交，否则一直占用进程，导入无法使用；
# =============================================================================
# 有时候会偶然出现  min() arg is an empty sequence  这种错误，找不出原因是什么，重启程序执行就行
# =============================================================================
1.空表如何处理过滤处理，出现空表直接跳过
2.文件夹中非正常表的处理

update20210302:更新对下载搜索报告超出utf-8字符的处理，通过正则表达式将超出的字符替换成空值，导入就不会出错了；
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os
import warnings
import re

warnings.filterwarnings('ignore')  #忽略警告错误

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8mb4')  #注意此处不能写成utf-8

#数据导入部分
print('请输入已清理好要导入的搜索词报告的路径：')
path = input('路径：')
if '"' in path:
    path = path.replace('"','')

#获取业绩报告中各路径地址
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))

i = 0
p=re.compile(r'[^\x00-\x7f]')

for filename in filenames:    
    search_term = pd.read_excel(filename)
    search_term['Customer Search Term'] = search_term['Customer Search Term'].apply(lambda x:re.sub(p,'',x))
    if len(search_term) == 0:
        continue
    else:
        search_term['Date'] = pd.to_datetime(search_term['Date'])
        min_date = min(search_term['Date'])
        length = len(search_term)
        
        #清理搜索词报告中的前后空格，以及不同国家下载的报告有轻微的区别，此处进行统一命名；
        for col in search_term.columns:
            if 'ACoS' in col:
                search_term.rename(columns = {col : 'Total Advertising Cost of Sales (ACoS)'},inplace  = True)
                                                        
            col_space = col.rstrip()
            search_term.rename(columns = {col:col_space},inplace = True)
        
        station = filename.split('\\')[-1].split('.')[0][0:6].lower()  #所有站点全部小写
        db_table = station + '_v'   
        
        print('当前导入站点为%s：'%station)  
        #删除大于min_date的数据
        db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'ad_mysql')
        cursor = db.cursor()
        cursor.execute('delete from `%s` where Date >= "%s" '%(db_table,min_date))
        db.commit()                  #此处一定要先提交，否则由于进程占用导致全部锁死
        #print('历史数据删除成功;')
        
        try:
            search_term.to_sql(db_table,connect,index = False,if_exists = 'append')
            #print('搜索词报告导入mysql成功，请在数据库中检查；')
        except Exception as e:
            print('导入出错，出错原因为',e)
            db.rollback()
            
print('导入成功')