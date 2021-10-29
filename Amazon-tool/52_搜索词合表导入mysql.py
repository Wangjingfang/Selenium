# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 20:56:16 2019

@author: Administrator
"""

import pymysql
from sqlalchemy import create_engine
import pandas as pd

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/testb?charset=utf8')  #注意此处不能写成utf-8

#数据导入部分
path = input('请输入已合并要导入的搜索词报告的路径：')
if '"' in path:
    path = path.replace('"','')
    
df = pd.read_excel(path)
print('数据正在读入中，请稍后')
date = min(df['Date'])
min_date = min(df['Date']).strftime('%Y-%m-%d')
length = len(df)
print('数据正在清洗中，请稍后')
for col in df.columns:
                  if '7 Day Advertised SKU Sales' in col:
                      df.rename(columns = {col : '7 Day Advertised SKU Sales'},inplace  = True)
                  if '7 Day Total Sales' in col:
                      df.rename(columns = {col : '7 Day Total Sales'},inplace  = True)
                  if '7 Day Other SKU Sales' in col:
                      df.rename(columns = {col : '7 Day Other SKU Sales'},inplace  = True)
                  if 'Advertising Cost of Sales' in col:
                      df.rename(columns = {col : 'Total Advertising Cost of Sales (ACoS)'},inplace  = True)
                  if 'Return' in col:
                      df.rename(columns = {col : 'Total Return on Advertising Spend (RoAS)'},inplace  = True) 
                                        
                  col_space = col.rstrip()
                  df.rename(columns = {col:col_space},inplace = True)
                                    
db_table = 'search_3'   #请输入想导入的数据库的表名称，若没有的话，数据库会新建

#先执行删除df中最小的值之前的所有数据；
db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'testb')
cursor = db.cursor()
# cursor.execute('delete from search_2 where Date <= "2019-10-28"')
cursor.execute('delete from search_2 where Date <= "%s"'%(min_date))   #注意此处的时间日期需要手动填写，暂时调试不出来，没办法--在%s前添加引号即可，实际传入SQL
db.commit()
print('删除%s时间之前的数据成功'%min_date)

#删除之前数据有再导入现在数据
try:
    df.to_sql(db_table,connect,index = False,if_exists = 'append')
    print('\n搜索词报告导入mysql成功，请在数据库中检查；')
except Exception as e:
    print('导入出错，出错原因为',e)

print('\n')
print('要导入的搜索词报告的数量为%d'%length)
print('搜索词报告中时间最小为%s'%min_date)


#数据检查部分，检查是否完全导入
cursor.execute('select count(*) from %s where Date >= "%s"'%(db_table,min_date))
data = cursor.fetchall()  #data返回的是一个多元元组，采用元组取数将其取出

if data[0][0] == length:
    print('数据导入正确，且检查成功！实际导入为%d,要导入数量为%d'%(data[0][0],length))
else:
    print('数据导入不一致，请在mysql中进行进一步核实！实际导入为%d,要导入数量为%d'%(data[0][0],length))






