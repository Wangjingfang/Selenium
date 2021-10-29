# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
此脚本主要用来合并从158里面下载的产品（由于每次只能下载2W条，所以可能会出现需要多次下载，这里是将多次下载的结果合并在一起）
注意：Excel保存为.xlsx（可以保存1048576条数据）,若保存为.xls最多只能支持65535条数据，


提醒：
若出现“'utf-8' codec can't decode byte 0xa1 in position 69: invalid start byte”错误，则可能是该txt文档不是以utf-8编码的，可以在notepad里面修改编码方式；
'''

import os
import pandas as pd

print('请输入要合并的all_listing文件夹路径（将文件放入文件夹内）：')
path = input('文件夹路径：')
if '"' in path:
    path = path.replace('"','')
    
    
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))

alllisting_df = pd.DataFrame()

for filename in filenames:
    origin_df = pd.read_excel(filename)

    alllisting_df = pd.concat([alllisting_df,origin_df])

final_name = path + '158_listing合并.xlsx'
alllisting_df.to_excel(final_name,index = False)


