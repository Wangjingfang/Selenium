# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:47:39 2021

@author: Administrator
"""

import pandas as pd
import math
import datetime
import os

os.chdir(r'C:\Users\Administrator\Desktop\NL')
df = pd.read_excel(r"C:\Users\Administrator\Desktop\NL.xlsx")

uk_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']


station = list(set(df['渠道来源']))

for sta in station:
        
    station_split_df = df[df['渠道来源'] == sta]  #分别获取每个渠道的对应数据
        
    sta_short = sta[-6:]
    
    print('正在分解中')

    for i in range(0,math.ceil(len(station_split_df)/19990)):
        
        group_sheet = pd.DataFrame()
        sku_sheet = pd.DataFrame()
        
        if i > 0:               
            cam_name = sta_short + '-' + str(datetime.datetime.today().strftime('%Y%m')) + '_' + str(i)            
        else:
            cam_name = sta_short + '-' + str(datetime.datetime.today().strftime('%Y%m'))
            
        budget = 200
        date = datetime.datetime.today().strftime('%Y/%m/%d')
        
        get_sellSKU = station_split_df[i * 19990:19990 + 19990 * i]
           
        data = [cam_name,budget,date,'','Auto','','','','','','','','Enabled','','','']
        campaign_sheet = pd.DataFrame(columns = uk_lis)
        campaign_sheet.loc['0'] = data
        
        group_sheet['Ad Group Name'] = get_sellSKU['SellSKU']
        group_sheet['Campaign Name'] = cam_name
        group_sheet['Max Bid'] = str(0.03)
        group_sheet['Ad Group Status'] = 'Enabled'
        
        
        sku_sheet['Ad Group Name'] = get_sellSKU['SellSKU']
        sku_sheet['Campaign Name'] = cam_name
        sku_sheet['SKU'] = get_sellSKU['SellSKU']
        sku_sheet['Status'] = 'Enabled'
        
        station_done_df = pd.concat([campaign_sheet,group_sheet,sku_sheet],sort = False)       
        out_path = str(sta_short) + '-FBM' + str(i) + '.xlsx'          
        station_done_df.to_excel(out_path,index = False) 
        
