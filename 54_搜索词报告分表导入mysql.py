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
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')  #忽略警告错误

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8')  #注意此处不能写成utf-8

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

input_info_df = pd.DataFrame(columns = ['站点','实际导入数据','应该导入数据excel文件长度','最小日期'])
i = 0

for filename in filenames:    
    search_term = pd.read_excel(filename)
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
    cursor.execute('delete from `%s` where Date >= "%s" '%(db_table,min_date))
    db.commit()                  #此处一定要先提交，否则由于进程占用导致全部锁死
    #print('历史数据删除成功;')
    
    try:
        search_term.to_sql(db_table,connect,index = False,if_exists = 'append')
        #print('搜索词报告导入mysql成功，请在数据库中检查；')
    except Exception as e:
        print('导入出错，出错原因为',e)
        db.rollback()
        
    #print('要导入的搜索词报告的数量为%d'%length)
    #print('搜索词报告中时间最小为%s'%min_date)
    
    """
    #数据检查部分，检查是否完全导入;经过多次验证后发现不需要，为了节省程序时间，省略，此处可以参考，不删
    cursor_check = db.cursor()
    cursor_check.execute('select count(*) from `%s` where Date >= "%s" '%(db_table,min_date)) #此处通过将%s双引号即可完成在SQL中的引用
    data = cursor_check.fetchall()  #data返回的是一个多元元组，采用元组取数将其取出
    
    if data[0][0] == length:
        print('数据导入正确，且检查成功！实际导入为%d,要导入数量为%d'%(data[0][0],length))
    else:
        print('数据导入不一致，请在mysql中进行进一步核实！实际导入为%d,因导入数量为%d'%(data[0][0],length))
    """  
    #print('\n')
    
    input_info_df.loc[i,'站点'] = station    
    # input_info_df.loc[i,'实际导入数据'] = data[0][0]
    input_info_df.loc[i,'应该导入数据excel文件长度'] = length
    input_info_df.loc[i,'最小日期'] = min_date
    i += 1

input_path = path + '_导入数据库结果' + '.csv'    
input_info_df.to_csv(input_path,index = False)
print('导入结果请在路径中查看')