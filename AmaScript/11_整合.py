# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 15:10:47 2021

@author: Administrator
"""

import os
import pandas as pd
from shutil import copyfile
from math import ceil


class batch_script:
    
    # 初始化一个类的实例，传入文件夹路径，文件路径
    def __init__(self,folder_path,file_path):
        self.folder_path = folder_path.replace('"','')
        self.file_path = file_path.replace('"','')
        
    # 输出一个文件下所有文件的名称与路径    
    def get_file_in_folder(self):
        filenames = []
        df = pd.DataFrame()
        for root,dirs,files in os.walk(self.folder_path):
            for file in files:
                filenames.append(os.path.join(root,file))

        df['文件路径'] = filenames
        df['文件名'] = files
        
        final_name = self.folder_path + '_文件名路径.xlsx'
        df.to_excel(final_name,index = False)
        
    # 主要应用于多个文件夹下的文件合并到一个文件下
    def file_to_one_folder(self):
        os.chdir(self.folder_path)
        os.mkdir('0total')
        os.chdir('0total')

        folders= os.listdir(self.folder_path)
        for folder in folders:
            dir = self.folder_path + '\\' +  str(folder)
            files = os.listdir(dir)
            for file in files:
                source = dir + '\\' + str(file)
                deter = str(file)
                copyfile(source, deter)
                
        print('多文件夹合并完成，请在total下查看')  

    # 主要应用于 158listing中一个Excel中多个sheet的合并
    def merge_sheet(self):
        workbook = pd.read_excel(self.file_path,None)
        sheets = list(workbook.keys())
        
        origin_df = pd.DataFrame()
        for sheet in sheets:
            df = pd.read_excel(self.file_path,sheet_name = sheet)
            origin_df = pd.concat([origin_df,df])
            print('正在合并中，请稍等；')
        
        final_name = self.file_path.split('.')[0] + '合并.xlsx'
        origin_df.to_excel(final_name,index = False)
        print('合并完成，请在桌面查看！')
        
    # 主要应用于 多个一样的Excel合并成一个文件，多Excel合并
    def merge_workbook(self):
        filenames = []
        for root,dirs,files in os.walk(self.folder_path):
            for file in files:
                filenames.append(os.path.join(root,file))
        
        alllisting_df = pd.DataFrame()
        
        print('正在合并，请稍后')
        for filename in filenames:
            origin_df = pd.read_excel(filename)
            alllisting_df = pd.concat([alllisting_df,origin_df])

        final_name = self.folder_path + '合并.xlsx'
        alllisting_df.to_excel(final_name,index = False)
        print('合并完成，请在桌面查看！')

    # 将Excel拆分成多个个Excel的简单小脚本,需要传入参数n,即你想要拆分的Excel数量
    def sheet_to_few_sheet(self,n):
        df = pd.read_excel(self.file_path)
        long = ceil(len(df)/n)
        
        for i in range(0,n):
            new_df = df[long * i : long * (i +1)]
            to_path = self.file_path.split('.xlsx')[0] + '_' + str(i) + '.xlsx'
            new_df.to_excel(to_path,index = False)
        print('生成完成，请在原路径下查看！')

doing = batch_script(input('请输入文件夹路径：'),input('请输入文件路径：'))  # 若无文件路径，可以直接为空

# merge = doing.get_file_in_folder()  # 输出一个文件下所有文件的名称与路径

# merge = doing.file_to_one_folder()  # 主要应用于多个文件夹下的文件合并到一个文件夹下

# merge = doing.merge_sheet()         # 主要应用于 158listing中一个Excel中多个sheet的合并

# merge = doing.merge_workbook()      # 主要应用于 多个一样的Excel合并成一个文件，多Excel合并

merge = doing.sheet_to_few_sheet(20)   # 将Excel拆分成多个个Excel的简单小脚本,需要传入参数n,即你想要拆分的Excel数量




