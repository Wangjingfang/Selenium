# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 21:41:46 2019

@author: Administrator
"""

'''
基本思路：
1.从158系统中导出文件，读入到pandas中
2.进行价格筛选>6.99,不需要筛选库存，评分是否需要筛选根据自己需要,挑选出中广告投放需要的数据列（渠道，SKU ,ASIN,中文名）
3.进行广告标签文本分词，并删除原来行，生成（渠道，SKU ,ASIN,广告活动名）
4.进行文件分割成1V1，调用表头模板文件函数file_header(此处还可以优化)，调用生成详细数据文件（split_fill_file），在主函数split_station中进行循环生成；

注意问题点：
1.不同国家的写入的时间格式不一样，模板内的格式（导入的表头，active等状态）也不一样；
2.jieba分词库中的一些数据仍不完善，最好人工手动训练；
3.文件信息生成函数split_fill_file，可以采用其他方式优化，待完成；
'''
import jieba
import jieba.analyse
import pandas as pd
import numpy as np
import jieba.posseg
import os
import calendar
from datetime import datetime


#jieba.analyse.set_idf_path(r"E:\01工作资料\000 C_group data\C_group_product_name\C组产品主要词语-utf-8.txt")  #导入产品词语库
            
#将价格低于一定的数据删除掉,提取主要的信息（渠道来源，SKU，ASIN，中文名）
def filter_price(price,path):   
    df_price = pd.read_excel(path)    
    df_filter = df_price[df_price['原价'] >= price]
    print('原始数据总共为%d,过滤价格后的数据为%d条'%(len(df_price),len(df_filter)))
    df_main_info = df_filter[['渠道来源','ASIN','SellSKU','产品中文名称']]
    print('价格删除成功，重点数据提取成功，下一步进行中；')
    df_main_info.reset_index(inplace = True)
    df_main_info = df_main_info.drop('index',axis = 1)
    return df_main_info

#对广告描述栏进行分词和合并，并进行后缀(suffix)公式合并标识 ,已完善   
def split_ad_tag(df,suffix):
    for i in range(0,len(df)):
        ad_tag = jieba.analyse.extract_tags(df.loc[i,'产品中文名称'],topK = 3,allowPOS=('n','nr','ns')) 
        df.loc[i,'ad_tag'] = ''.join(ad_tag)
            
    #将df中的空值复制为缺失值
    for i in range(0,len(df)):
        if df.loc[i,'ad_tag'] == '':
            df.loc[i,'ad_tag'] = np.nan 
           
    #将缺失值填充前一个值
    df[['产品中文名称','ad_tag']] = df[['产品中文名称','ad_tag']].fillna(method = 'ffill',axis = 1) #此处不可用inplace = true
    
    #去除ad_tag中字符串×，在亚马逊后台系统并不识别,
    df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace('×','')) 
    #去除空格        
    df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace(' ','')) 
        
    df['广告活动'] = df['ASIN'] + ' ' + df['ad_tag'] + '-' + suffix
    df = df.drop('产品中文名称',axis = 1)
    df = df.drop('ad_tag',axis = 1)    
    print('广告tag分词已完成，可以直接进行下一步的分解')
    return df
  
#添加广告活动预算和广告竞价
def add_bid_info(origin_df):
  
    cam_budget_func = lambda x:5.12 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(500.12 if x == 'IN' or x == 'JP' else(10 if x == 'AU' else 15))
    
    max_bid_func = lambda x:0.2 if x == 'US'  else(0.2 if x == 'CA' else(0.35 if x == 'MX' else(0.15 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'AU' else(0.12 if x == 'IT' or x == 'ES' else(15 if x == 'JP' else(3 if x == 'IN' else 0.3))))))
       
    for i in range(0,len(origin_df)):
        
        origin_df.loc[i,'budget'] = cam_budget_func(origin_df.loc[i,'渠道来源'][-2:])
        origin_df.loc[i,'bid'] = max_bid_func(origin_df.loc[i,'渠道来源'][-2:])
        origin_df.loc[i,'广告组名称'] = origin_df.loc[i,'SellSKU']

        origin_df = origin_df.reindex(['渠道来源','广告活动','广告组名称','SellSKU','budget','bid'],axis = 1)
  
    return origin_df


if __name__ == '__main__':

    origin_path = input('请输入要分解成1V1广告的文件路径（原始的从158系统中导出的）：')
    if '"' in origin_path:
        origin_path = origin_path.replace('"','')

    os.chdir(os.path.dirname(origin_path))

    del_low_price = float(input('请输入要筛选的价格范围（直接输入最小价格即可,如3.99）：'))
    #suffix = 'W' + str(datetime.now().isocalendar()[1]) + 'bFBA'
    suffix = 'FBA'
    #suffix = str(input('请输入要添加的广告的后缀名（如：W51bFBA）:'))

    split_df = filter_price(del_low_price,origin_path)

    ad_tag_df = split_ad_tag(split_df,suffix)

    result_df = add_bid_info(ad_tag_df)

    result_df.to_excel(r'%s.xlsx'%(suffix),index = False)

    print('文件路径已经创建好，请在%s中的‘1V1已分解的文件夹’查看'%origin_path)

    os.chdir(r'E:\01工作资料')  #此处应该是关闭打开的‘1V1文件夹’,可以对文件夹进行剪切移动等操作，但目前未找到对应的操作方法

    print('\n 如果想请清理python内存，请在IPython中输入‘reset’')
