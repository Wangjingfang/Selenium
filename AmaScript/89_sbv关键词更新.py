# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:53:51 2021

@author: Administrator
"""

'''
SBV广告关键词更新以及上传
通过已经获取的广告信息的ASIN去tableau中搜索对应的关键词，将关键导出为pending_keyword表
'''
import pandas as pd

pending_keyword = pd.read_excel(r"C:\Users\Administrator\Desktop\keyword_pending.xlsx")

sbv_info_origin = pd.read_excel(r"C:\Users\Administrator\Desktop\sbv_campaign_media_info.xlsx")

pending_asin = set(pending_keyword['ASIN'])
pending_keyword['Match Type'] = pending_keyword.apply(lambda x:'exact' if x['Orders']>= 5 and x['CR']>= 0.16 else('phrase' if x['Orders']>= 3 and x['CR']>= 0.12 else 'broad'), axis=1)
sbv_info_origin['存在投放'] = sbv_info_origin['Creative ASINs'].apply(lambda x : 1 if x in pending_asin else 0)
sbv_info_origin = sbv_info_origin[sbv_info_origin['存在投放'] == 1]
sbv_info_origin['Campaign ID'] = sbv_info_origin['Campaign ID'].apply(str)

for sta in set(sbv_info_origin['Station']):
    
    output_df = pd.DataFrame()
    sbv_info = sbv_info_origin[sbv_info_origin['Station'] == sta]
    print('正在分解中，请稍后')
    
    for asin in set(sbv_info['Creative ASINs']):
        
        campaign_df = pd.DataFrame()
        group_df = pd.DataFrame()
        keyword_df = pd.DataFrame()
        
        asin_info = sbv_info[sbv_info['Creative ASINs'] == asin]
          
        # 广告活动行
        campaign_df = asin_info.drop('Ad Group',axis = 1)
        campaign_df['Budget'] = 10
        campaign_df['Record Type'] = 'Campaign'
    
        # 广告组行
        group_df = asin_info[['Campaign ID','Campaign','Ad Format','Ad Group']]
        group_df['Record Type'] = 'Ad Group'
        
        # 关键词行
        keyword_df = pending_keyword[pending_keyword['ASIN'] == asin]
        keyword_df = keyword_df[['ASIN','Customer Search Term','Match Type']]
        # bid_func = lambda x: 0.25 if x == 'US' else 0.15
        # keyword_df['Max Bid'] = bid_func(sta[-2:].upper())
        keyword_df['Max Bid'] = keyword_df['Match Type'].apply(lambda x: 0.33 if x == 'exact' else(0.28 if x=='phrase' else(0.25 if sta[-2:] == 'US' else 0.15)))
        keyword_df['Record Type'] = 'Keyword'
        keyword_df.rename(columns = {'Customer Search Term':'Keyword'},inplace = True)
        
        # 合并3个df，并进行处理
        total_campaign = pd.concat([campaign_df,group_df,keyword_df],axis = 0)
        total_campaign[['Campaign','Campaign ID','Ad Format','Ad Group']] = total_campaign[['Campaign','Campaign ID','Ad Format','Ad Group']].fillna(axis = 0,method = 'ffill')
        total_campaign['Campaign Status'] = 'enabled'
        
        total_campaign = total_campaign.drop(['ASIN','Station','存在投放'],axis = 1)
        
        output_df = pd.concat([output_df,total_campaign],axis = 0)
        
    output_df[['Campaign Type','Record ID','Portfolio ID','Campaign End Date','Landing Page ASINs	','Brand Name','Brand Entity ID','Brand Logo Asset ID','Headline','Automated Bidding','Bid Multiplier','Ad Group Status','Status','Impressions','Clicks','Spend','Orders','Total Units','Sales','ACoS','Placement Type']] = ''
    output_df = output_df.reindex(['Record ID','Record Type','Campaign ID','Campaign','Campaign Type','Ad Format','Budget','Portfolio ID','Campaign Start Date','Campaign End Date','Budget Type','Landing Page Url','Landing Page ASINs','Brand Name','Brand Entity ID','Brand Logo Asset ID','Headline','Creative ASINs','Media ID','Automated Bidding','Bid Multiplier','Ad Group','Max Bid','Keyword','Match Type','Campaign Status','Serving Status','Ad Group Status','Status','Impressions','Clicks','Spend','Orders','Total Units','Sales','ACoS','Placement Type'],axis = 1)
    output_df['Campaign ID']
    output_df.to_excel(r'C:\Users\Administrator\Desktop\sbv_上传\{}_sbv上传报告.xlsx'.format(sta),index = False)

    