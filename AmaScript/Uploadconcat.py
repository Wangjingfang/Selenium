# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
此脚本主要是合并生成的批量广告的文件，相比同一个站点多次上传（容易出现问题），
1.请以站点命名，如   022-1-US_FBA.xlsx ；122-US.xlsx
2.将要合并的文件放在同一个文件夹下
3.合并后的文件已单独放入在一个文件夹中，若原文件只有一个，也会新生成；
'''

import os
import pandas as pd
import numpy as np

# print('请输入要合并的上传报告的文件夹路径（将文件放入文件夹内）')
# path = input('文件夹路径：')
path = r"D:\data\周四批量\festival\周四批量20211028"

# if '"' in path:
#     path = path.replace('"','')
    

os.chdir(path)
os.mkdir('周四批量')
os.chdir('周四批量')

filepath = []
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filepath.append(os.path.join(root,file))
        filenames.append(file[0:6])

filenames = set(filenames)  #列表去重

merge_upload_file = pd.DataFrame()
print('正在开始合并，请稍后')
for filename in filenames:
    print(filename)
    for file in filepath:
        print(file)
        if file.split('\\')[-1][0:6] == filename:
            origin_df = pd.read_excel(file)
            merge_upload_file = pd.concat([merge_upload_file,origin_df])
    
    final_name = filename + '_合并.xlsx'
    
    #将BR，NL的初始竞价设置为字符串格式;np.isnan只有在列类型是float时才可以使用，如列类型为str会报错
    if filename[-2:] in ['BR','NL']:        
        merge_upload_file['Max Bid'] = merge_upload_file['Max Bid'].apply(lambda x:'' if np.isnan(x) else x)
        merge_upload_file['Max Bid'] = merge_upload_file['Max Bid'].apply(lambda x: str(x) if x else '')
    
    if filename[-2:] in ['US','CA','MX','JP','AE','AU','SA','BR','SG']:
        merge_upload_file =merge_upload_file[['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type', 'Campaign Status', 'Ad Group Status', 'Status', 'Bidding strategy']]
    else:
        merge_upload_file = merge_upload_file[['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                               'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type', 'Campaign Status', 'Ad Group Status', 'Status', 'Bid+']]
    
    merge_upload_file.to_excel(final_name,index = False)
    merge_upload_file = pd.DataFrame()

print('合并完成，请在原文件下查看；')
# path
# os.chdir(path + "\\" + "周四批量")
