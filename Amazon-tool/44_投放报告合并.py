# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 15:00:16 2019

@author: Administrator
"""

import pandas as pd
import os
from datetime import datetime

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
              df = pd.read_excel(filename)  #注意读入的是csv文件
              df['Station'] = filename.split('\\')[-1][0:6]
              final_file = pd.concat([final_file,df])
              print('文件正在合并中，请稍后；投放报告文件较大，合并速度很慢，请稍等；')
          
          final_name = 'targeting_report' + datetime.now().strftime('%Y%m%d') + '.xlsx'
          final_file.to_excel(final_name,index = False)
          print('文件合并完成')

    except Exception as e:
         print('文件合并错误',e)        
         
origin_path = input('请输入要合并的投放报告文件夹名称：')
if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path)    
merge = merge_file(origin_path)    
    
print('文件合并完成，请在路径中查看：%s'%origin_path)
