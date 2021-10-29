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

update20210302:更新对下载搜索报告超出utf-8字符的处理，通过正则表达式将超出的字符替换成空值，导入就不会出错了；
update20210416:更新对搜索词报告未在mysql中建表出现报错的情况，若没有该表，则自动创建该新表；
update20210714:超出utf-8字符集全部出错，已重新从3月2号开始全部导入数据
'''
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')  #忽略警告错误

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8mb4')  #注意此处不能写成utf-8

#数据导入部分
path = input('请输入搜索词报告的文件夹：').replace('"','')

#获取搜索词报告中各路径地址
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))


for filename in filenames:    
    search_term = pd.read_excel(filename)
    
    if len(search_term) == 0:
        continue
    else:
        search_term['Date'] = pd.to_datetime(search_term['Date'])
        min_date = min(search_term['Date'])
        length = len(search_term)
        
        #清理搜索词报告中的前后空格，以及不同国家下载的报告有轻微的区别，此处进行统一命名；
        for col in search_term.columns:
            if '7 Day Advertised SKU Sales' in col:
                search_term.rename(columns = {col : '7 Day Advertised SKU Sales'},inplace  = True)
            if '7 Day Total Sales' in col:
                search_term.rename(columns = {col : '7 Day Total Sales'},inplace  = True)
            if '7 Day Other SKU Sales' in col:
                search_term.rename(columns = {col : '7 Day Other SKU Sales'},inplace  = True)
            if 'Advertising Cost of Sales' in col:
                search_term.rename(columns = {col : 'Total Advertising Cost of Sales (ACoS)'},inplace  = True)
            if 'Return' in col:
                search_term.rename(columns = {col : 'Total Return on Advertising Spend (RoAS)'},inplace  = True) 
                                            
            col_space = col.rstrip()
            search_term.rename(columns = {col:col_space},inplace = True)
        
        station = filename.split('\\')[-1].split('.')[0][0:6].lower()  #所有站点全部小写
        db_table = station + '_s'   
        
        print('当前导入站点为%s：'%station)  
        #删除大于min_date的数据
        db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'ad_mysql')
        cursor = db.cursor()
        
        try:
            cursor.execute('delete from `%s` where Date >= "%s" '%(db_table,min_date))
            db.commit()                  #此处一定要先提交，否则由于进程占用导致全部锁死
        except:
            cursor.execute('''
                CREATE TABLE `{}` (
              `Date` date DEFAULT NULL,
              `Portfolio name` longtext CHARACTER SET utf8,
              `Currency` longtext CHARACTER SET utf8,
              `Campaign Name` longtext CHARACTER SET utf8,
              `Ad Group Name` longtext CHARACTER SET utf8,
              `Targeting` longtext CHARACTER SET utf8,
              `Match Type` longtext CHARACTER SET utf8,
              `Customer Search Term` longtext CHARACTER SET utf8mb4,
              `Impressions` decimal(18,0) DEFAULT NULL,
              `Clicks` decimal(18,0) DEFAULT NULL,
              `Click-Thru Rate (CTR)` decimal(18,6) DEFAULT NULL,
              `Cost Per Click (CPC)` decimal(18,2) DEFAULT NULL,
              `Spend` decimal(18,2) DEFAULT NULL,
              `7 Day Total Sales` decimal(18,2) DEFAULT NULL,
              `Total Advertising Cost of Sales (ACoS)` decimal(18,6) DEFAULT NULL,
              `Total Return on Advertising Spend (RoAS)` decimal(18,6) DEFAULT NULL,
              `7 Day Total Orders (#)` decimal(18,0) DEFAULT NULL,
              `7 Day Total Units (#)` decimal(18,0) DEFAULT NULL,
              `7 Day Conversion Rate` decimal(18,6) DEFAULT NULL,
              `7 Day Advertised SKU Units (#)` decimal(18,0) DEFAULT NULL,
              `7 Day Other SKU Units (#)` decimal(18,0) DEFAULT NULL,
              `7 Day Advertised SKU Sales` decimal(18,2) DEFAULT NULL,
              `7 Day Other SKU Sales` decimal(18,2) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
              '''.format(db_table))
            print('  新建表{0}成功'.format(db_table))
        
        
        try:
            search_term.to_sql(db_table,connect,index = False,if_exists = 'append')
        except Exception as e:
            print(' 导入出错，出错原因为',e)
            















