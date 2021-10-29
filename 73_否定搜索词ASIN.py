# -*- coding: utf-8 -*-
"""
否定的维度是在投放的维度，不是在广告组维度；在否定中，已经归档的词语无法再次否定，暂时不知道为什么

否定搜索词需要根据广告活动，广告组，在投放位置上进行否定；需要的列：
    广告活动，广告组名称，否定的关键词（or ASIN）

"""

import os
import pandas as pd


path = input('excel文件：')
if '"' in path:
    path = path.replace('"','')

current_path = os.path.dirname(path)
os.chdir(current_path)
if not os.path.exists('否定搜索词-1V1已分解文件'):
    os.mkdir('否定搜索词-1V1已分解文件')

os.chdir('否定搜索词-1V1已分解文件')

pending_sheet = pd.read_excel(path)


#预处理，给关键词进行分广告组,分别分为ASIN，Broad,Phase,Exact四个组，按照转化率进行确定；在平均CPC竞价上乘以1.2；
# and len(pending_sheet.loc[i,'Customer Search Terms Upper']) == 10
for i in range(0,len(pending_sheet)):
    if pending_sheet.loc[i,'Customer Search Terms Upper'][0:2] == 'B0':
        pending_sheet.loc[i,'Negative_type'] = 'Negative Targeting Expression'
    else:
        pending_sheet.loc[i,'Negative_type'] = 'Negative Exact'

    pending_sheet.loc[i,'国家'] = pending_sheet.loc[i,'Station'].split('-')[-1].upper()
    

us_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
uk_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']

# report_sequence_func = lambda x:1 if x == 'US' else(2 if x == 'CA' else(3 if x == 'MX' else(4 if x == 'UK' else(5 if x == 'DE' else(6 if x == 'FR' else(7 if x == 'IT' else(8 if x == 'ES' else(9 if x == 'JP' else('A' if x == 'IN' else('B' if x == 'AU' else('C' if x == 'AE' else ('D' if x == 'SA' else 'E'))))))))))))

country_list = list(set(pending_sheet['国家']))
for country in country_list:
    country_sheet = pending_sheet[pending_sheet['国家'] == country]
    if country in ['US','MX','AU','AE','SA','CA']:
        df = pd.DataFrame(columns = us_lis)                
        station_list = list(set(country_sheet['Station']))
        for station in station_list:
            station_sheet = country_sheet[country_sheet['Station'] == station]
            station_sheet.reset_index(inplace=True)

            for i in range(0,len(station_sheet)):
                df.loc[i,'Campaign'] = station_sheet.loc[i,'Campaign Name']
                df.loc[i,'Ad Group'] = station_sheet.loc[i,'Ad Group Name']
                if station_sheet.loc[i,'Negative_type'] == 'Negative Exact':
                    df.loc[i,'Keyword or Product Targeting'] = station_sheet.loc[i,'Customer Search Terms Upper']                
                else:
                    df.loc[i,'Product Targeting ID'] = 'asin="' + station_sheet.loc[i,'Customer Search Terms Upper'] + '"'
                
                df.loc[i,'Match Type'] = station_sheet.loc[i,'Negative_type']
                df.loc[i,'Status'] = 'Enabled'
                    
                                       
            # report_sequence = report_sequence_func(country.upper())
            shop = station
            out_path = shop +  '-否定关键词' + '.xlsx'
            df.to_excel(out_path,index = False)  
            
    if country in ['UK','DE','FR','IT','ES']:
        df = pd.DataFrame(columns = uk_lis)                
        station_list = list(set(country_sheet['Station']))
        for station in station_list:
            station_sheet = country_sheet[country_sheet['Station'] == station]
            station_sheet.reset_index(inplace=True)

            for i in range(0,len(station_sheet)):
                df.loc[i,'Campaign Name'] = station_sheet.loc[i,'Campaign Name']
                df.loc[i,'Ad Group Name'] = station_sheet.loc[i,'Ad Group Name']
                if station_sheet.loc[i,'Negative_type'] == 'Negative Exact':
                    df.loc[i,'Keyword or Product Targeting'] = station_sheet.loc[i,'Customer Search Terms Upper']                
                else:
                    df.loc[i,'Product Targeting ID'] = 'asin="' + station_sheet.loc[i,'Customer Search Terms Upper'] + '"'
                
                df.loc[i,'Match Type'] = station_sheet.loc[i,'Negative_type']
                df.loc[i,'Status'] = 'Enabled'
                    
                                       
            # report_sequence = report_sequence_func(country.upper())
            # shop = station[0:3]
            shop= station
            # out_path = str(shop) + '-' + str(report_sequence) + '-' + country.upper()  + '-否定关键词' + '.xlsx'
            out_path = shop + '-否定关键词'+'.xlsx'
            df.to_excel(out_path,index = False)
               
print('文件分解成功，请在路径中%s的‘-否定搜索词1VN已分解文件’查看'%current_path)           
os.chdir(r'D:\data\否定ASIN和关键词')
           
           
