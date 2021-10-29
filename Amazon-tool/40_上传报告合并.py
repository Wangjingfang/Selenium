# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
此脚本主要是合并生成的批量广告的文件，相比同一个站点多次上传（容易出现问题），
1.请以站点命名，如   022-1-US_FBA.xlsx ；
2.将要合并的文件放在同一个文件夹下
3.合并后的文件已单独放入在一个文件夹中，若原文件只有一个，也会新生成；
'''

import os
import pandas as pd

print('请输入要合并的上传报告的文件夹路径（将文件放入文件夹内）')
path = input('文件夹路径：')
if '"' in path:
    path = path.replace('"','')
    

os.chdir(path)
os.mkdir('合并后文件') 
os.chdir('合并后文件')   

filepath = []
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filepath.append(os.path.join(root,file))
        filenames.append(file[0:8])

filenames = set(filenames)  #列表去重

merge_upload_file = pd.DataFrame()
print('正在开始合并，请稍后')
for filename in filenames:
    for file in filepath:
        if file.split('\\')[-1][0:8] == filename:
            origin_df = pd.read_excel(file)
            merge_upload_file = pd.concat([merge_upload_file,origin_df])
    
    final_name = filename + '_合并.xlsx'    
    merge_upload_file.to_excel(final_name,index = False)
    merge_upload_file = pd.DataFrame()

print('合并完成，请在原文件下查看；')        
os.chdir(r'E:\01工作资料')        
