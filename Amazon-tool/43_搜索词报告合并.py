# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 20:09:36 2019

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
              df = pd.read_excel(filename)
              
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
                              
              df['Station'] = filename.split('\\')[-1][0:6]
              final_file = pd.concat([final_file,df])
              print('文件正在合并中，请稍后；')
          
          final_name = 'Search_term_' + datetime.now().strftime('%Y%m%d') + '.xlsx'
          final_file.to_excel(final_name,index = False)    

    except Exception as e:
         print('文件合并错误',e)
               
origin_path = input('请输入要合并的搜索词报告文件夹名称：')

if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path)    
merge = merge_file(origin_path)    
    
print('文件合并完成，请在路径中查看：%s'%origin_path)

