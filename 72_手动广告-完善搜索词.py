# -*- coding: utf-8 -*-
"""

# =============================================================================
# 2020.12.1  被杨大佬称此脚本为“垃圾”，请引以为戒；
# =============================================================================


手动广告：数据来源于自动广告中的关键词，通过tableau批量导出后，生成对应的模板直接在后台上传；tableau中要求字段：
  站点，search_terms_asin大写，CPC，CR，Campaign Name，SellerSKU；   请在tableau中导出后进行批量填充Ctrl + Enter；
1.上传手动广告时，ASIN投放的格式不一样，请注意；常见API文档：https://advertising.amazon.com/API/docs/en-us/bulksheets/sp/sp-examples/sp-create-manual-targeting
2.此模板是US，MX，AE，AU，SA为一套US的模板，EU（UK，DE，FR，IT，ES）按照UK的模板，剩下CA按照CA的模板，无法同自动广告的生成的报告合并（表头不一样）
3.请处理好从tableau中的导出的Excel的空值单元格，进行填充或着删除掉（注意广告组为渠道SKU）；

目前竞价用于测试阶段，测试阶段的手动广告的名称为 -bManual
"""

import os
import pandas as pd
import datetime

path = input('excel文件：')
if '"' in path:
    path = path.replace('"','')

current_path = os.path.dirname(path)
os.chdir(current_path)
if not os.path.exists('手动广告-1V1已分解文件'):
    os.mkdir('手动广告-1V1已分解文件')

os.chdir('手动广告-1V1已分解文件')

print('文件分解成功，请在路径中%s的‘1VN已分解文件’查看'%current_path)

pending_sheet = pd.read_excel(path)


#预处理，给关键词进行分广告组,分别分为ASIN，Broad,Phase,Exact四个组，按照转化率进行确定；在平均CPC竞价上乘以1.2；
for i in range(0,len(pending_sheet)):
    if pending_sheet.loc[i,'search_terms_asin大写'][0:2] == 'B0' and len(pending_sheet.loc[i,'search_terms_asin大写']) == 10: 
        if pending_sheet.loc[i,'CR'] > 0.15:
            pending_sheet.loc[i,'Ad_group'] = 'ASIN'
    else:
        if pending_sheet.loc[i,'CR'] < 0.1:
            pending_sheet.loc[i,'Ad_group'] = 'Broad'
            pending_sheet.loc[i,'Broad_all'] = 'Broad+'
        elif pending_sheet.loc[i,'CR'] >= 0.1 and pending_sheet.loc[i,'CR'] < 25:
            pending_sheet.loc[i,'Ad_group'] = 'Phrase'
            pending_sheet.loc[i,'Broad_all'] = 'Broad+'
            pending_sheet.loc[i,'Phrase_all'] = 'Phrase+'
        elif pending_sheet.loc[i,'CR'] >= 0.25:
            pending_sheet.loc[i,'Ad_group'] = 'Exact'
            pending_sheet.loc[i,'Broad_all'] = 'Broad+'
            pending_sheet.loc[i,'Phrase_all'] = 'Phrase+'

    pending_sheet.loc[i,'Broad_CPC'] = round(pending_sheet.loc[i,'CPC']*1.1,2)  #将初始竞价值设定为平均CPC的竞价值的1.2倍
    pending_sheet.loc[i,'Phrase_CPC'] = round(pending_sheet.loc[i,'CPC']*1.2,2)
    pending_sheet.loc[i,'Exact_CPC'] = round(pending_sheet.loc[i,'CPC']*1.5,2)
    pending_sheet.loc[i,'ASIN_CPC'] = round(pending_sheet.loc[i,'CPC']*1.2,2)
    pending_sheet.loc[i,'国家'] = pending_sheet.loc[i,'站点'].split('-')[-1].lower()
    

us_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
uk_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']
ca_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']


date = datetime.datetime.today() + datetime.timedelta(days=0)    
cam_start_date_func = lambda x:date.strftime('%m/%d/%Y') if x == 'US' or x == 'CA'  else(date.strftime('%d/%m/%Y') if x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else date.strftime('%Y/%m/%d'))
report_sequence_func = lambda x:1 if x == 'US' else(2 if x == 'CA' else(3 if x == 'MX' else(4 if x == 'UK' else(5 if x == 'DE' else(6 if x == 'FR' else(7 if x == 'IT' else(8 if x == 'ES' else(9 if x == 'JP' else('A' if x == 'IN' else('B' if x == 'AU' else('C' if x == 'AE' else ('D' if x == 'SA' else 'E'))))))))))))
cam_budget_func = lambda x:5 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(60 if x == 'IN' else(200 if x == 'JP' else(6 if x == 'AU' else 8)))

country_list = list(set(pending_sheet['国家']))  
for country in country_list:
    country_sheet = pending_sheet[pending_sheet['国家'] == country]
    if country in ['us','mx','au','ae','sa','ca']:
        station_lis = us_lis                
        station_list = list(set(country_sheet['站点']))
        for station in station_list:
            station_sheet = country_sheet[country_sheet['站点'] == station]
            
            station_output = pd.DataFrame()
            campaign_list = list(set(station_sheet['Campaign Name']))
              
            for campaign_name in campaign_list:                        
                 df = pd.DataFrame(columns = station_lis)
                 campaign_manual = station_sheet[station_sheet['Campaign Name'] == campaign_name]
                 campaign_manual.reset_index(inplace=True)
                 manual_length = len(campaign_manual)
                
                # 写入广告活动第一行
                 df.loc[0,'Campaign'] = campaign_name
                 df.loc[0,'Campaign Daily Budget'] = cam_budget_func(country.upper())
                 df.loc[0,'Campaign Start Date'] = cam_start_date_func(country.upper())
                 df.loc[0,'Campaign Targeting Type'] = 'Manual'
                 df.loc[0,'Campaign Status'] = 'Enabled'
                ######### 此处未完待续
                
                 i = 1
                # 判断存在多少个广告组,并创建广告组
                 if 'ASIN' in set(list(campaign_manual['Ad_group'])):
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'ASIN'
                    df.loc[i,'Max Bid'] = 0.2
                    df.loc[i,'Ad Group Status'] = 'Enabled'
                    
                    i += 1
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'ASIN'
                    df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                    df.loc[i,'Status'] = 'Enabled'
                
                    ASIN_manual = campaign_manual[campaign_manual['Ad_group'] == 'ASIN']
                    ASIN_manual.reset_index(inplace=True)
                    ASIN_length = len(ASIN_manual)
                    for j in range(1,ASIN_length + 1):
                        df.loc[i + j,'Campaign'] = campaign_name
                        df.loc[i + j,'Ad Group'] = 'ASIN'
                        df.loc[i + j,'Max Bid'] = ASIN_manual.loc[j - 1,'ASIN_CPC']
                        df.loc[i + j,'Product Targeting ID'] = 'asin="' + ASIN_manual.loc[j - 1,'search_terms_asin大写'] + '"'
                        df.loc[i + j,'Match Type'] = 'Targeting Expression'
                        df.loc[i + j,'Status'] = 'Enabled'
                    
                    i = i + ASIN_length + 1
                    
                 if 'Broad+' in set(list(campaign_manual['Broad_all'])):
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Broad'
                    df.loc[i,'Max Bid'] = 0.2
                    df.loc[i,'Ad Group Status'] = 'Enabled'
                    
                    i += 1
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Broad'
                    df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                    df.loc[i,'Status'] = 'Enabled'
                
                    Broad_manual = campaign_manual[campaign_manual['Broad_all'] == 'Broad+']  
                    Broad_manual.reset_index(inplace=True)
                    Broad_length = len(Broad_manual)
                    for j in range(1,Broad_length + 1):
                        df.loc[i + j,'Campaign'] = campaign_name
                        df.loc[i + j,'Ad Group'] = 'Broad'
                        df.loc[i + j,'Max Bid'] = Broad_manual.loc[j - 1,'Broad_CPC']
                        df.loc[i + j,'Keyword or Product Targeting'] = Broad_manual.loc[j - 1,'search_terms_asin大写']
                        df.loc[i + j,'Match Type'] = 'Broad'
                        df.loc[i + j,'Status'] = 'Enabled'
                    
                    i = i + Broad_length + 1    
                    
                 if 'Phrase+' in set(list(campaign_manual['Phrase_all'])):
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Phrase'
                    df.loc[i,'Max Bid'] = 0.2
                    df.loc[i,'Ad Group Status'] = 'Enabled'
                    
                    i += 1
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Phrase'
                    df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                    df.loc[i,'Status'] = 'Enabled'
                
                    Phrase_manual = campaign_manual[campaign_manual['Phrase_all'] == 'Phrase+']  ###此处待修改回来
                    Phrase_manual.reset_index(inplace=True)
                    Phrase_length = len(Phrase_manual)
                    for j in range(1,Phrase_length + 1):
                        df.loc[i + j,'Campaign'] = campaign_name
                        df.loc[i + j,'Ad Group'] = 'Phrase'
                        df.loc[i + j,'Max Bid'] = Phrase_manual.loc[j - 1,'Phrase_CPC']
                        df.loc[i + j,'Keyword or Product Targeting'] = Phrase_manual.loc[j - 1,'search_terms_asin大写']
                        df.loc[i + j,'Match Type'] = 'Phrase'
                        df.loc[i + j,'Status'] = 'Enabled'
                    
                    i = i + Phrase_length + 1    
                    
                 if 'Exact' in set(list(campaign_manual['Ad_group'])):
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Exact'
                    df.loc[i,'Max Bid'] = 0.2
                    df.loc[i,'Ad Group Status'] = 'Enabled'
                    
                    i += 1
                    df.loc[i,'Campaign'] = campaign_name
                    df.loc[i,'Ad Group'] = 'Exact'
                    df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                    df.loc[i,'Status'] = 'Enabled'
                
                    Exact_manual = campaign_manual[campaign_manual['Ad_group'] == 'Exact']  ###此处待修改回来
                    Exact_manual.reset_index(inplace=True)
                    Exact_length = len(Exact_manual)
                    for j in range(1,Exact_length + 1):
                        df.loc[i + j,'Campaign'] = campaign_name
                        df.loc[i + j,'Ad Group'] = 'Exact'
                        df.loc[i + j,'Max Bid'] = Exact_manual.loc[j - 1,'Exact_CPC']
                        df.loc[i + j,'Keyword or Product Targeting'] = Exact_manual.loc[j - 1,'search_terms_asin大写']
                        df.loc[i + j,'Match Type'] = 'Exact'
                        df.loc[i + j,'Status'] = 'Enabled'
                    
                    i = i + Exact_length + 1    
                                       
                 station_output = pd.concat([station_output,df])           
                                       
            report_sequence = report_sequence_func(country.upper())
            shop = station[0:3]
            out_path = str(shop) + '-' + str(report_sequence) + '-' + country.upper()  + '-手动广告' + '.xlsx'        
            station_output.to_excel(out_path,index = False)        
               
    if country in ['uk','de','fr','it','es']:
        station_lis = uk_lis
        station_list = list(set(country_sheet['站点']))
        for station in station_list:
            station_sheet = country_sheet[country_sheet['站点'] == station]
            
            station_output = pd.DataFrame()
            campaign_list = list(set(station_sheet['Campaign Name']))
            
            for campaign_name in campaign_list:
                df = pd.DataFrame(columns = station_lis)
                campaign_manual = station_sheet[station_sheet['Campaign Name'] == campaign_name]
                campaign_manual.reset_index(inplace=True)
                manual_length = len(campaign_manual)
               
                # 写入广告活动第一行
                df.loc[0,'Campaign Name'] = campaign_name
                df.loc[0,'Campaign Daily Budget'] = cam_budget_func(country.upper())
                df.loc[0,'Campaign Start Date'] = cam_start_date_func(country.upper())
                df.loc[0,'Campaign Targeting Type'] = 'Manual'
                df.loc[0,'Campaign Status'] = 'Enabled'
               
                i = 1
                # 判断存在多少个广告组,并创建广告组
                if 'ASIN' in set(list(campaign_manual['Ad_group'])):
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'ASIN'
                   df.loc[i,'Max Bid'] = 0.2
                   df.loc[i,'Ad Group Status'] = 'Enabled'
                   
                   i += 1
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'ASIN'
                   df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                   df.loc[i,'Status'] = 'Enabled'
               
                   ASIN_manual = campaign_manual[campaign_manual['Ad_group'] == 'ASIN']
                   ASIN_manual.reset_index(inplace=True)
                   ASIN_length = len(ASIN_manual)
                   for j in range(1,ASIN_length + 1):
                       df.loc[i + j,'Campaign Name'] = campaign_name
                       df.loc[i + j,'Ad Group Name'] = 'ASIN'
                       df.loc[i + j,'Max Bid'] = ASIN_manual.loc[j - 1,'ASIN_CPC']
                       df.loc[i + j,'Product Targeting ID'] = 'asin="' + ASIN_manual.loc[j - 1,'search_terms_asin大写'] + '"'
                       df.loc[i + j,'Match Type'] = 'Targeting Expression'
                       df.loc[i + j,'Status'] = 'Enabled'
                   
                   i = i + ASIN_length + 1
                   
                if 'Broad+' in set(list(campaign_manual['Broad_all'])):
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Broad'
                   df.loc[i,'Max Bid'] = 0.2
                   df.loc[i,'Ad Group Status'] = 'Enabled'
                   
                   i += 1
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Broad'
                   df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                   df.loc[i,'Status'] = 'Enabled'
               
                   Broad_manual = campaign_manual[campaign_manual['Broad_all'] == 'Broad+']  
                   Broad_manual.reset_index(inplace=True)
                   Broad_length = len(Broad_manual)
                   for j in range(1,Broad_length + 1):
                       df.loc[i + j,'Campaign Name'] = campaign_name
                       df.loc[i + j,'Ad Group Name'] = 'Broad'
                       df.loc[i + j,'Max Bid'] = Broad_manual.loc[j - 1,'Broad_CPC']
                       df.loc[i + j,'Keyword or Product Targeting'] = Broad_manual.loc[j - 1,'search_terms_asin大写']
                       df.loc[i + j,'Match Type'] = 'Broad'
                       df.loc[i + j,'Status'] = 'Enabled'
                   
                   i = i + Broad_length + 1    
                   
                if 'Phrase+' in set(list(campaign_manual['Phrase_all'])):
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Phrase'
                   df.loc[i,'Max Bid'] = 0.2
                   df.loc[i,'Ad Group Status'] = 'Enabled'
                   
                   i += 1
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Phrase'
                   df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                   df.loc[i,'Status'] = 'Enabled'
               
                   Phrase_manual = campaign_manual[campaign_manual['Phrase_all'] == 'Phrase+']  ###此处待修改回来
                   Phrase_manual.reset_index(inplace=True)
                   Phrase_length = len(Phrase_manual)
                   for j in range(1,Phrase_length + 1):
                       df.loc[i + j,'Campaign Name'] = campaign_name
                       df.loc[i + j,'Ad Group Name'] = 'Phrase'
                       df.loc[i + j,'Max Bid'] = Phrase_manual.loc[j - 1,'Phrase_CPC']
                       df.loc[i + j,'Keyword or Product Targeting'] = Phrase_manual.loc[j - 1,'search_terms_asin大写']
                       df.loc[i + j,'Match Type'] = 'Phrase'
                       df.loc[i + j,'Status'] = 'Enabled'
                   
                   i = i + Phrase_length + 1    
                   
                if 'Exact' in set(list(campaign_manual['Ad_group'])):
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Exact'
                   df.loc[i,'Max Bid'] = 0.2
                   df.loc[i,'Ad Group Status'] = 'Enabled'
                   
                   i += 1
                   df.loc[i,'Campaign Name'] = campaign_name
                   df.loc[i,'Ad Group Name'] = 'Exact'
                   df.loc[i,'SKU'] = campaign_manual.loc[0,'SellerSKU']
                   df.loc[i,'Status'] = 'Enabled'
               
                   Exact_manual = campaign_manual[campaign_manual['Ad_group'] == 'Exact']  ###此处待修改回来
                   Exact_manual.reset_index(inplace=True)
                   Exact_length = len(Exact_manual)
                   for j in range(1,Exact_length + 1):
                       df.loc[i + j,'Campaign Name'] = campaign_name
                       df.loc[i + j,'Ad Group Name'] = 'Exact'
                       df.loc[i + j,'Max Bid'] = Exact_manual.loc[j - 1,'Exact_CPC']
                       df.loc[i + j,'Keyword or Product Targeting'] = Exact_manual.loc[j - 1,'search_terms_asin大写']
                       df.loc[i + j,'Match Type'] = 'Exact'
                       df.loc[i + j,'Status'] = 'Enabled'
                   
                   i = i + Exact_length + 1    
           
                station_output = pd.concat([station_output,df])               
        
            report_sequence = report_sequence_func(country.upper())
            shop = station[0:3]
            out_path = str(shop) + '-' + str(report_sequence) + '-' + country.upper()  + '-手动广告' + '.xlsx'        
            station_output.to_excel(out_path,index = False)  
           
os.chdir(r'E:\01工作资料')                 
           
           
