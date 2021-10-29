# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:38:58 2019

@author: Administrator
"""

'''

文件名称命名  JP-XXXX  （请要导入的文件首字母以国家命名）
注意：pandas读入Excel后，若Excel有相同列名，pandas会自动在一个列名后加 “.1”；如   Mashup SnS click.1
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')  #忽略警告错误

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/dsp?charset=utf8')  #注意此处不能写成utf-8

#数据导入部分
print('输入已清理好要导入的DSP报告的文件夹路径：')
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
    
    #删除'Mashup SnS click'，因为该列存在相同列
    search_term.drop('Mashup SnS click',axis = 1,inplace = True)
    search_term.drop('Mashup SnS click.1',axis = 1,inplace = True)
    #替换到sales后面的货币符号，注意sales里面有大小写之分
    for col in search_term.columns:
        if 'sales' in col:
            new_col = col.split('sales')[0] + 'sales'
            search_term.rename(columns = {col : new_col},inplace  = True)
        
        if 'Sales' in col:
            new_col = col.split('Sales')[0] + 'Sales'
            search_term.rename(columns = {col : new_col},inplace  = True)


    
    db_table = filename.split('\\')[-1][0:2]  #取该文件作为表名
    
    print('当前导入站点为%s'%db_table)  
    #删除大于min_date的数据
    db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',database = 'dsp')
    cursor = db.cursor()
    cursor.execute('delete from `%s` where Date >= "%s" '%(db_table,min_date))
    db.commit()                  #此处一定要先提交，否则由于进程占用导致全部锁死
    print('历史数据删除成功;')
    
    try:
        search_term.to_sql(db_table,connect,index = False,if_exists = 'append')
        print('报告导入mysql成功，请在数据库中检查；')
    except Exception as e:
        print('导入出错，出错原因为',e)
        db.rollback()
        
    #print('要导入的报告的数量为%d'%length)
    #print('报告中时间最小为%s'%min_date)
    
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
    print('\n')
    
    input_info_df.loc[i,'站点'] = db_table    
    # input_info_df.loc[i,'实际导入数据'] = data[0][0]
    input_info_df.loc[i,'应该导入数据excel文件长度'] = length
    input_info_df.loc[i,'最小日期'] = min_date
    i += 1

input_path = path + '_导入数据库结果' + '.csv'    
input_info_df.to_csv(input_path,index = False)
print('导入结果请在路径中查看')