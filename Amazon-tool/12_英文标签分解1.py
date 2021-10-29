# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:11:58 2019

@author: Administrator
"""
'''
从title中提取英文标签的产品，如何提取；
输入：一堆title; 输出：每个title对应的产品；  中间的函数关系：将title分解成每个单词，将单词中的名词提取出来，确定名词是否为产品类词语（与数据库核对）
'''

# import pandas as pd

# split_df = pd.read_excel(r"C:\Users\Administrator\Desktop\title_tag.xlsx")
# count = {}

file = open(r"C:\Users\Administrator\Desktop\tag.txt",'r').read()

count = {}






'''
import jieba
import jieba.analyse
import pandas as pd
import numpy as np
import jieba.posseg
import os

#jieba.analyse.set_idf_path(r"E:\01工作资料\000 C_group data\C_group_product_name\C组产品主要词语-utf-8.txt")  #常见错误，字典之间的空格要注意，保留一个空格

def ad_tag(path):

    df = pd.read_excel(path)
    
    df.reset_index(inplace = True)
    
    filename = path.split('\\')[-1].split('.')[0]
    
    for i in range(0,len(df)):
        ad_tag = jieba.analyse.extract_tags(df.loc[i,'中文名'],topK = 4,allowPOS=('n','nr','ns')) 
        df.loc[i,'ad_tag'] = ''.join(ad_tag)
        
    
    #将df中的空值复制为缺失值
    for i in range(0,len(df)):
        if df.loc[i,'ad_tag'] == '':
            df.loc[i,'ad_tag'] = np.nan 
    
    
    #更改ad_tag在df中的位置
    df_tag = df.ad_tag
    df = df.drop('ad_tag',axis = 1)
    df.insert(7,'ad_tag',df_tag)
            
    #将缺失值填充前一个值
    df[['中文名','ad_tag']] = df[['中文名','ad_tag']].fillna(method = 'ffill',axis = 1) #此处不可用inplace = true
    
    #去除ad_tag中字符串×，在亚马逊后台系统并不识别,
    df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace('×','')) 
    #去除空格        
    df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace(' ','')) 
    
    output_path = filename + '_广告标签已分解提取' + '.xlsx'
    
    #导出格式
    df.to_excel(output_path, index = False)
    
file_path = input('请输入要分解标签的文件（注意经过处理后VBA脚本处理后）:')
#去除输入路径时带入的双引号
if '"' in file_path:
    file_path = file_path.replace('"','')
    
f_path = os.path.dirname(file_path)
os.chdir(f_path)

ad_tag(file_path)

print('数据提取成功，路径为:%s'%f_path)
'''











