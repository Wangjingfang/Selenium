# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 10:39:58 2020

@author: Administrator
"""
'''
目的：此脚本主要是合并原始的库龄报告
注意问题：
1.库龄报告中有csv文件，有xlsx文件，需要在循环读取时做一个判断；
2.由于US，CA，EU文件表头均不一致，这里只提取渠道SKU，0-90天，90-181等5个字段，其他字段舍弃
3.单独生成来源渠道字段（文件名+AmazonZ01）,EU需要添加markerplace字段（截取最后的国家），将90天以后库龄相加，汇总成一个字段；
4.文件的名称开头为  023-USXXXX.csv (开头6位需要以短渠道命名)
5.对渠道SKU重新命名以符合158listing导出的格式（来源渠道和SellSKU中间有5列，以ABCDE填充空列），筛选出90天及以上有库存的SKU
'''

import os
import pandas as pd

print('请输入要合并的库龄文件夹路径')
path = input('文件夹：')
if '"' in path:
    path = path.replace('"','')
    
    
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))

origin_df = pd.DataFrame()
for filename in filenames:
    excel_name = filename.split('\\')[-1]
    shop_name = excel_name.split('-')[0]
    country_name = excel_name[4:6].upper()
    suffix_name = excel_name.split('.')[-1].lower()
    
    if suffix_name == 'xlsx' or suffix_name == 'xls':
        df = pd.read_excel(filename)
    
    if suffix_name == 'csv':
        df = pd.read_csv(filename,encoding = 'ISO-8859-1')
        
    if country_name in ['AU','JP']:
        df_key_columns = df[['SKU','inv-age-0-to-90-days','inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']]
        df_key_columns['渠道来源'] = 'Amazon-Z01' + excel_name[0:6]
        df_key_columns.rename(columns = {'SKU':'sku'},inplace = True)

    if country_name == 'EU':
        df_key_columns = df[['sku','inv-age-0-to-90-days','inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']]
        df_key_columns['渠道来源'] = 'Amazon-Z01' + shop_name + '-' + df['marketplace'].apply(lambda x:x.split('.')[-1].upper())
        
    if country_name in ['US','CA','IN']:
        df_key_columns = df[['sku','inv-age-0-to-90-days','inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']]
        df_key_columns['渠道来源'] = 'Amazon-Z01' + excel_name[0:6]
    
    df_key_columns[['inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']] = df_key_columns[['inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']].apply(pd.to_numeric,errors='coerce').fillna(0)
    df_key_columns[['inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']] = df_key_columns[['inv-age-91-to-180-days','inv-age-181-to-270-days','inv-age-271-to-365-days','inv-age-365-plus-days']].astype('int')
    
    df_key_columns['bigger_than_90'] = df_key_columns['inv-age-91-to-180-days'] + df_key_columns['inv-age-181-to-270-days'] + df_key_columns['inv-age-271-to-365-days'] + df_key_columns['inv-age-365-plus-days']
    
    origin_df = pd.concat([origin_df,df_key_columns])
    

#对渠道SKU重新命名以符合158listing导出的格式（来源渠道和SellSKU中间有5列，以ABCDE填充空列），筛选出90天及以上有库存的SKU，
origin_df = origin_df[origin_df['bigger_than_90'] >= 1]
origin_df.rename(columns = {'sku':'SellSKU'},inplace = True) 
origin_df = pd.concat([origin_df,pd.DataFrame(columns = list('ABCDE'))])    
origin_df = origin_df.reindex(['渠道来源','A','B','C','D','E','SellSKU'],axis = 1)
final_name = path + '已合并的库龄报告.xlsx'
origin_df.to_excel(final_name,index = False)    
        