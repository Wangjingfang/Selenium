# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:54:52 2019

@author: Administrator
"""

import pandas as pd
import os

def get_data(path):
    
    filename = path.split('\\')[-1].split('.')[0]
    
    df = pd.read_excel(path)

    df.reset_index(inplace = True)
    
    for i in range(0,len(df)//5):
        df.loc[i,'来源渠道_1'] = df.loc[i *5 + 4,'来源渠道']
        df.loc[i,'匹配类型_1'] = df.loc[i *5 +2,'匹配类型']
        df.loc[i,'活动名称_1'] = df.loc[i *5 + 3,'活动名称']
        df.loc[i,'广告组_1'] = df.loc[i * 5 + 3,'活动名称']
        df.loc[i,'竞价_1'] = df.loc[i * 5 + 2,'竞价']
        df.loc[i,'曝光量_1'] = df.loc[i * 5 + 2,'曝光量']
        df.loc[i,'点击量_1'] = df.loc[i * 5 + 2,'点击量']
        df.loc[i,'花费_1'] = df.loc[i * 5 + 2,'花费']
        df.loc[i,'点击率_1'] = df.loc[i * 5 + 2,'点击率']
        df.loc[i,'CPC_1'] = df.loc[i * 5 + 2,'CPC']
        df.loc[i,'出单数_1'] = df.loc[i * 5 + 2,'出单数']
        df.loc[i,'贡献销售额_1'] = df.loc[i * 5 + 2,'贡献销售']
        df.loc[i,'转化率_1'] = df.loc[i * 5 + 2,'转化率']
        df.loc[i,'Acos_1'] = df.loc[i * 5 + 2,'ACoS']
      
    datadf = df[['来源渠道_1','匹配类型_1','活动名称_1','广告组_1','竞价_1','曝光量_1','点击量_1','花费_1','点击率_1','CPC_1','出单数_1','贡献销售额_1','转化率_1','Acos_1']]    
    output_path = filename + '_数据已提取' + '.xlsx'   
    datadf.to_excel(output_path,index = False)



file_path = input('请输入CPC中产品页面要提取的文件:')
#去除输入路径时带入的双引号
if '"' in file_path:
    file_path = file_path.replace('"','')
    
f_path = os.path.dirname(file_path)
os.chdir(f_path)

get_data(file_path)

print('数据提取成功，路径为:%s'%f_path)


