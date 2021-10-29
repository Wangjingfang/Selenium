# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 20:20:06 2019

@author: Administrator
"""

import os
import pandas as pd

# 获取文件夹中的文件名，写入到filenames中
def get_filename(path):
    filenames = []
    try:
        for root,dirs,files in os.walk(path):
            for file in files:
                filenames.append(os.path.join(root,file))
        return filenames
    except Exception as e:
        print('文件位置读取错误',e)
        
# 读取文件文件内容，并进行合并
def merge_file(file_path):
    merged_file = pd.DataFrame()
    filenames = get_filename(file_path)
    try:
        for filename in filenames:
            df = pd.read_csv(filename)
            df['Date'] = filename.split('\\')[-1].split('.csv')[0]           # 将文件名称作为日期新建一列
            df['Date'] = pd.to_datetime(df['Date'])
            df['station'] = filename.split('\\')[4]                         # 将站别新做一列
            merged_file = pd.concat([merged_file,df])
        merged_name = filename.split('\\')[4] + '.csv'                      #将文件名改为站点名称
        merged_file.to_csv(merged_name,index = False)
    except Exception as e:
        print('文件合并错误',e)


origin_path = input('请输入要合并的业绩报告的文件夹名称：')
if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path)    
merge = merge_file(origin_path)    
    
print('文件合并完成，请在路径中查看：%s'%origin_path)






