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

每周搜索前一个月的FBA数据，对数据进行CPC确认筛选后再进行

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
            
# =============================================================================
# #将价格低于一定的数据删除掉,提取主要的信息（渠道来源，SKU，ASIN，中文名）
# def filter_price(price,path):   
#     df_price = pd.read_excel(path)    
#     df_filter = df_price[(df_price['原价'] >= price) | (df_price['原价'] == 0)]
#     print('原始数据总共为%d,过滤价格后的数据为%d条'%(len(df_price),len(df_filter)))
#     df_main_info = df_filter[['渠道来源','ASIN','SellSKU','产品中文名称']]
#     print('价格删除成功，重点数据提取成功，下一步进行中；')
#     df_main_info.reset_index(inplace = True)
#     df_main_info = df_main_info.drop('index',axis = 1)
#     return df_main_info
# =============================================================================

#确定节日or产品的后缀名，给广告活动以区分
def get_suffix(df):
    for i in range(len(df)):
        if df.loc[i,'节日标识'] == '圣诞节':
            suffix = '圣诞_bFBA'
        elif df.loc[i,'节日标识'] == '万圣节':
            suffix = '万圣_bFBA'
        else:
            suffix = 'W' + str(datetime.now().isocalendar()[1]) + 'bFBA'
    
        df.loc[i,'suffix'] = suffix
        
    return df

#根据产品的原价确定广告的初始竞价，后期所有的FBA产品都投放；
def set_bid(sta,origin_price,festival_tag):
    station = sta[-2:].lower()
    us_ca_bid = lambda x:0.05 if x < 4.99 else(0.1 if x < 6.99 else(0.14 if x < 8.99 else(0.18 if x < 10.99 else 0.20)))
    uk_de_bid = lambda x:0.04 if x < 4.99 else(0.08 if x < 6.99 else(0.12 if x < 8.99 else(0.16 if x < 10.99 else 0.18)))
    fr_it_es_bid = lambda x:0.04 if x < 4.99 else(0.06 if x < 6.99 else(0.1 if x < 8.99 else(0.14 if x < 10.99 else 0.16)))
    ae_bid = lambda x:0.24 if x < 10 else(0.26 if x < 15 else 0.3)
    in_bid = lambda x:1 if x < 100 else(2 if x < 300 else(3 if x < 500 else 4))
    jp_bid = lambda x:4 if x < 1000 else(8 if x < 1500 else(10 if x < 2000 else 15))
    mx_bid = lambda x:0.4 if x < 200 else(0.6 if x < 400 else(0.8 if x < 2000 else 1))
    au_bid = lambda x:0.12 if x < 10 else(0.18 if x < 20 else(0.25 if x < 30 else 0.3))
    
    if station in ['us','ca']:
        bid = us_ca_bid(origin_price)
    
    elif station in ['uk','de']:
        bid = uk_de_bid(origin_price)
    
    elif station in ['fr','it','es']:
        bid = fr_it_es_bid(origin_price)
        
    elif station in ['ae','sa']:
        bid = ae_bid(origin_price)

    elif station in ['in']:
        bid = in_bid(origin_price)

    elif station in ['jp']:
        bid = jp_bid(origin_price)

    elif station in ['mx']:
        bid = mx_bid(origin_price)
        
    else:
        bid = 0
        print('此站点不在预设站点之内')
    
    if festival_tag in ['万圣节','圣诞节']:
        bid += 0.03
    
    #品牌店铺094的广告
    if sta[-6:-3] == '094':
        bid += 0.1
    
    return bid

#对广告描述栏进行分词和合并，并进行后缀(suffix)公式合并标识 ,已完善   
def split_ad_tag(df):
    for i in range(0,len(df)):
        ad_tag = jieba.analyse.extract_tags(df.loc[i,'产品中文名称'],topK = 3,allowPOS=('n','nr','ns'))
        # words = []
        # for word in ad_tag:
        #     if len(word) > 1 and len(word) < 4:
        #         words.append(word)
                
        df.loc[i,'ad_tag'] = ''.join(ad_tag)
                
    #将df中的空值复制为缺失值
    for i in range(0,len(df)):
        if df.loc[i,'ad_tag'] == '':
            df.loc[i,'ad_tag'] = np.nan 
           
    #将缺失值填充前一个值
    df[['产品中文名称','ad_tag']] = df[['产品中文名称','ad_tag']].fillna(method = 'ffill',axis = 1) #此处不可用inplace = true
    
    #去除ad_tag中字符串×，在亚马逊后台系统并不识别,
    for sysbol in ['×',' ','（','）','(',')','，',',']:
        df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace(sysbol,'')) 

    df['广告活动'] = df['ASIN'] + '-' + df['ad_tag'] + '-' + df['suffix']
    df = df.drop('产品中文名称',axis = 1)
    df = df.drop('ad_tag',axis = 1)    
    print('广告tag分词已完成，可以直接进行下一步的分解')
    return df
  
#添加广告活动预算和广告竞价
def add_bid_info(origin_df):
    
    #常规FBA1V1预算-C组
    cam_budget_func = lambda x:5 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(300 if x == 'IN' or x == 'JP' else(6 if x == 'AU' else 10))
    
    # #常规FBA1V1预算-G组
    # #cam_budget_func = lambda x:4.5 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(300 if x == 'IN' or x == 'JP' else(6 if x == 'AU' else 5))
    
    # #万圣竞价
    # #max_bid_func = lambda x:0.18 if x == 'US'  else(0.2 if x == 'CA' else(0.7 if x == 'MX' else(0.16 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'AU' else(0.12 if x == 'IT' or x == 'ES' else(10 if x == 'JP' else(5 if x == 'IN' else 0.3))))))
    
    # #圣诞竞价
    # #max_bid_func = lambda x:0.16 if x == 'US'  else(0.2 if x == 'CA' else(0.5 if x == 'MX' else(0.14 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'AU' else(0.12 if x == 'IT' or x == 'ES' else(10 if x == 'JP' else(5 if x == 'IN' else 0.3))))))
    
    # #常规FBA1V1竞价-C组
    # max_bid_func = lambda x:0.14 if x == 'US'  else(0.18 if x == 'CA' else(0.5 if x == 'MX' else(0.12 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'AU' else(0.10 if x == 'IT' or x == 'ES' else(10 if x == 'JP' else(5 if x == 'IN' else 0.3))))))

    # #常规FBA1V1竞价-G组
    # #max_bid_func = lambda x:0.12 if x == 'US'  else(0.14 if x == 'CA' else(0.5 if x == 'MX' else(0.10 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'AU' else(0.08 if x == 'IT' or x == 'ES' else(10 if x == 'JP' else(5 if x == 'IN' else 0.3))))))
    
    for i in range(len(origin_df)):
        
        origin_df.loc[i,'budget'] = cam_budget_func(origin_df.loc[i,'渠道来源'][-2:])
        origin_df.loc[i,'bid'] = set_bid(origin_df.loc[i,'渠道来源'],origin_df.loc[i,'原价'],origin_df.loc[i,'节日标识'])
        origin_df.loc[i,'广告组名称'] = origin_df.loc[i,'SellSKU']

    origin_df = origin_df.reindex(['渠道来源','广告活动','广告组名称','SellSKU','budget','bid'],axis = 1)
  
    return origin_df

print('请输入要分解成1V1广告的文件路径（原始的从158系统中导出的）：')    
origin_path = input('excel文件：')
if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(os.path.dirname(origin_path))  
origin_file = pd.read_excel(origin_path)
# del_low_price = float(input('请输入要筛选的价格范围（直接输入最小价格即可,如3.99）：'))
suffix = 'W' + str(datetime.now().isocalendar()[1]) + 'bFBA'
# suffix = '圣诞_bFBA'
# suffix = '万圣_bFBA'
# suffix = 'bFBA'

#suffix = str(input('请输入要添加的广告的后缀名（如：W51bFBA）:'))

#split_df = filter_price(del_low_price,origin_path)

suffix_df = get_suffix(origin_file)
ad_tag_df = split_ad_tag(suffix_df)
result_df = add_bid_info(ad_tag_df)

writer = pd.ExcelWriter(origin_path)
origin_file.to_excel(writer,'原始数据158导出数据',index = False)
result_df.to_excel(writer,'待上传CPC广告文件',index = False)
writer.save()

#result_df.to_excel(r'bFBA_{}.xlsx'.format(datetime.today().strftime('%Y%m%d')),index = False)

print('文件路径已经创建好，请在%s中的‘1V1已分解的文件夹’查看'%origin_path) 

os.chdir(r'E:\01工作资料')  #此处应该是关闭打开的‘1V1文件夹’,可以对文件夹进行剪切移动等操作，但目前未找到对应的操作方法

print('\n 如果想请清理python内存，请在IPython中输入‘reset’')
