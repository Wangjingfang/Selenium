# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

此脚本主要是为了将业绩报告按站点合并成一个新的站点，并添加新的一列：站点的名称；共19列；
此脚本是运行上一清理过业绩报告的脚本后执行的，上一脚本已经添加过日期
"""

import pandas as pd
import os

def get_file(path):
    try:
        filenames = []
        for root,dirs,files in os.walk(path):
                for file in files:
                    filenames.append(os.path.join(root,file))
        return filenames
    except Exception as e:
        print('获取文件失败',e)
        
def merge_file(file_path):
    final_file = pd.DataFrame()
    filenames = get_file(file_path)
    try:
          for filename in filenames:
              df = pd.read_csv(filename)  #注意读入的是csv文件
              df['Station'] = filename.split('\\')[-1][0:6]
              # df['Date'] = year_month  #请添加要合并的月份
             
              final_file = pd.concat([final_file,df])
              print('文件正在合并中，请稍后；')
          
          final_name = 'business_report' + '_按站点合并' + '.csv'
          final_file.to_csv(final_name,index = False)    

    except Exception as e:
         print('文件合并错误',e)        
         
origin_path = input('请输入要合并的业绩报告的文件夹名称：')
# year_month = input('请输入要写入的日期（格式如：2019-10）：')
if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path)    
merge = merge_file(origin_path)    
    
print('文件合并完成，请在路径中查看：%s'%origin_path)



