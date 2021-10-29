# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 21:41:46 2019

@author: Administrator
"""

'''
update20200925:按照产品原价生成广告竞价，根据节日标识对产品进行广告活动后缀名的处理，将生成的广告活动等汇总到原表中的一个新sheet中
update20201023:新增SA站点，SA竞价基本同AE，跟AE同模板


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
import datetime


#jieba.analyse.set_idf_path(r"E:\01工作资料\000 C_group data\C_group_product_name\C组产品主要词语-utf-8.txt")  #导入产品词语库

#创建文件和文件夹路径
def creat_filepath(path):
    current_path = os.path.dirname(path)
    os.chdir(current_path)
    if not os.path.isdir('bFBA-1V1已分解的文件夹'):
        os.mkdir('bFBA-1V1已分解的文件夹')
    else:
        os.removedirs('bFBA-1V1已分解的文件夹')
        os.mkdir('bFBA-1V1已分解的文件夹')
    os.chdir('bFBA-1V1已分解的文件夹')
    print('文件路径已经创建好，请在%s中的‘1V1已分解的文件夹’查看'%current_path)                

'''
#将价格低于一定的数据删除掉,提取主要的信息（渠道来源，SKU，ASIN，中文名）
def filter_price(price,path):   
    df_price = pd.read_excel(path)    
    df_filter = df_price[(df_price['原价'] >= price) | (df_price['原价'] == 0)]
    print('原始数据总共为%d,过滤价格后的数据为%d条'%(len(df_price),len(df_filter)))
    df_main_info = df_filter[['渠道来源','ASIN','SellSKU','产品中文名称']]
    print('价格删除成功，重点数据提取成功，下一步进行中；')
    df_main_info.reset_index(inplace = True)
    df_main_info = df_main_info.drop('index',axis = 1)
    return df_main_info
'''

#确定节日or产品的后缀名，给广告活动以区分
def get_suffix(df):
    for i in range(len(df)):
        if df.loc[i,'节日标识'] == '圣诞节':
            suffix = '圣诞_bFBA'
        elif df.loc[i,'节日标识'] == '万圣节':
            suffix = '万圣_bFBA'
        else:
            suffix = 'W' + str(datetime.datetime.now().isocalendar()[1]) + 'bFBA'
    
        df.loc[i,'suffix'] = suffix
        
    return df

#根据产品的原价确定广告的初始竞价，后期所有的FBA产品都投放；
def set_bid(df):

    us_ca_bid = lambda x:0.05 if x < 4.99 else(0.1 if x < 6.99 else(0.14 if x < 8.99 else(0.18 if x < 10.99 else 0.20)))
    uk_de_bid = lambda x:0.04 if x < 4.99 else(0.08 if x < 6.99 else(0.12 if x < 8.99 else(0.16 if x < 10.99 else 0.18)))
    fr_it_es_bid = lambda x:0.04 if x < 4.99 else(0.06 if x < 6.99 else(0.1 if x < 8.99 else(0.14 if x < 10.99 else 0.16)))
    ae_bid = lambda x:0.24 if x < 10 else(0.26 if x < 15 else 0.3)
    in_bid = lambda x:1 if x < 100 else(2 if x < 300 else(3 if x < 500 else 4))
    jp_bid = lambda x:4 if x < 1000 else(8 if x < 1500 else(10 if x < 2000 else 15))
    mx_bid = lambda x:0.4 if x < 200 else(0.6 if x < 400 else(0.8 if x < 2000 else 1))
    
    for i in range(len(df)):
        station = df.loc[i,'渠道来源'][-2:].lower()
        origin_price = df.loc[i,'原价']
        festival_tag = df.loc[i,'节日标识']
        
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
        if df.loc[i,'渠道来源'][-6:-3] == '094':
            bid += 0.1
    
        df.loc[i,'max_bid'] = bid
        
    return df

#对广告描述栏进行分词和合并，并进行后缀(suffix)公式合并标识 ,已完善   
def split_ad_tag(df):
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
    for sysbol in ['×',' ','（','）','(',')','，',',']:
        df['ad_tag'] = df['ad_tag'].apply(lambda x:x.replace(sysbol,'')) 
        
    df['广告活动'] = df['ASIN'] + '-' + df['ad_tag'] + '-' + df['suffix']
  
    print('广告tag分词已完成，可以直接进行下一步的分解')
    return df

#创建模板文件表头，可以引用1VN中的表头函数
def file_header(station_long):
    
    station = station_long[-2:]
    
    us_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
    ca_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
    mx_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
    uk_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']
    de_lis = ['Kampagne','Tagesbudget Kampagne','Startdatum der Kampagne','Enddatum der Kampagne','Ausrichtungstyp der Kampagne','Portfolio-ID','Anzeigengruppe','Maximales Gebot','SKU','Schlüsselwort- oder Produktausrichtung','Produktausrichtungs-ID','übereinstimmungstyp','Kampagnenstatus','Anzeigengruppe Status','Status','gebot+']
    fr_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']
    #fr_lis = ['Nom de la Campagne','Budget quotidien de la Campagne','Date de début de la Campagne','Date de fin de la Campagne','Type de Ciblage de la Campagne','ID de portfolio','Nom du groupe d\'annonces','Enchère Max','SKU','Ciblage de mots-clés ou de produits','ID de ciblage de produits','Type de correspondance','Statut de la campagne','Statut du groupe d’annonces','Statut']
    it_lis = ['Nome della campagna','Budget giornaliero campagna','Data di inizio della campagna','Data di fine della campagna','Tipo di targeting della campagna','ID portfolio','Nome del gruppo di annunci','Offerta massima','SKU','Targeting per parola chiave o prodotto','ID targeting per prodotto','Tipo di corrispondenza','Stato della campagna','Stato del gruppo','Stato']
    es_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group Name','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status','Bid+']
    in_lis = ['Campaign Name','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','SKU','Keyword or Product Targeting','Product Targeting ID','Match Type','Campaign Status','Ad Group Status','Status']
    jp_lis = ['キャンペーン名','1日の平均予算','開始日','終了日','ターゲティング','ポートフォリオ ID','広告グループ名','入札額','キーワードまたは商品ターゲティング','商品ターゲティング ID','マッチタイプ','広告(SKU)','キャンペーン ステータス','広告グループ ステータス','ステータス']
    au_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']
    ae_lis = ['Record ID','Record Type','Campaign ID','Campaign','Campaign Daily Budget','Campaign Start Date','Campaign End Date','Campaign Targeting Type','Portfolio ID','Ad Group','Max Bid','Keyword or Product Targeting','Product Targeting ID','Match Type','SKU','Campaign Status','Ad Group Status','Status','Bidding strategy','Placement Type','Increase bids by placement']

    
    if station == 'US' or station =='SA':      
        station_lis = us_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'
          
    elif station == 'CA':
        station_lis = ca_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'
       
    elif station == 'MX':
        station_lis = mx_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'

    elif station == 'UK':
        station_lis = uk_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'

    elif station == 'DE':
        station_lis = de_lis
        active_tag = 'aktiviert'
        auto_tag = 'automatisch'

    elif station == 'FR':
        station_lis = uk_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'    
   
    # elif station == 'FR':
    #     station_lis = fr_lis
    #     active_tag = 'Activé'
    #     auto_tag = 'Automatique'
                
    elif station == 'IT':
        station_lis = it_lis
        active_tag = 'attivo'
        auto_tag = 'Automatico'

    elif station == 'ES':
        station_lis = es_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'

    elif station == 'IN':
        station_lis = in_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'

    elif station == 'JP':
        station_lis = jp_lis
        active_tag = '有効'
        auto_tag = 'オート'

    elif station == 'AU':
        station_lis = au_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'
        
    elif station == 'AE':
        station_lis = ae_lis
        active_tag = 'Enabled'
        auto_tag = 'Auto'

    else:
        print('该站点不在预设站点之内，该站点为：%s,请检查!'%station_long)
        station_lis = []
        active_tag = ''
        auto_tag = ''

    station_header = pd.DataFrame(columns = station_lis)
    return(station_header,active_tag,auto_tag)  
    
    
#创建#根据表头文件和对应站点参数进行文件的拆分，数据的填充  
def split_fill_file(station_split_df,df,active_tag,auto_tag,cam_budget,cam_start_date,country):
    sta = country.upper()
    sku_len = len(station_split_df)
    print('文件正在生成中，请稍后；')
    
    if sta == 'US' or sta == 'MX' or sta == 'AU' or sta == 'AE' or sta == 'SA':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Campaign'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Campaign Daily Budget'] = cam_budget
                    df.loc[i + j *3,'Campaign Start Date'] = cam_start_date
                    df.loc[i + j *3,'Campaign Targeting Type'] = auto_tag
                    df.loc[i + j *3,'Campaign Status'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Campaign'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Max Bid'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'Ad Group Status'] = active_tag
                else:
                    df.loc[i + j *3,'Campaign'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Status'] = active_tag   
    
    elif sta == 'CA':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Campaign Daily Budget'] = cam_budget
                    df.loc[i + j *3,'Campaign Start Date'] = cam_start_date
                    df.loc[i + j *3,'Campaign Targeting Type'] = auto_tag
                    df.loc[i + j *3,'Campaign Status'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Max Bid'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'Ad Group Status'] = active_tag
                else:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Status'] = active_tag   
             
    elif sta == 'UK' or sta == 'ES' or sta == 'FR':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Campaign Daily Budget'] = cam_budget
                    df.loc[i + j *3,'Campaign Start Date'] = cam_start_date
                    df.loc[i + j *3,'Campaign Targeting Type'] = auto_tag
                    df.loc[i + j *3,'Campaign Status'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'Ad Group Name'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Max Bid'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'Ad Group Status'] = active_tag
                else:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Ad Group Name'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Status'] = active_tag 
    
    elif sta == 'DE':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Kampagne'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Tagesbudget Kampagne'] = cam_budget
                    df.loc[i + j *3,'Startdatum der Kampagne'] = cam_start_date
                    df.loc[i + j *3,'Ausrichtungstyp der Kampagne'] = auto_tag
                    df.loc[i + j *3,'Kampagnenstatus'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Kampagne'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'Anzeigengruppe'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Maximales Gebot'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'Anzeigengruppe Status'] = active_tag
                else:
                    df.loc[i + j *3,'Kampagne'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Anzeigengruppe'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Status'] = active_tag
                    
    # elif sta == 'FR':
    #     for j in range(0,sku_len):
    #         for i in range(2,5):
    #             if i == 2:
    #                 df.loc[i + j *3,'Nom de la Campagne'] = station_split_df.loc[j,'广告活动']
    #                 df.loc[i + j *3,'Budget quotidien de la Campagne'] = cam_budget
    #                 df.loc[i + j *3,'Date de début de la Campagne'] = cam_start_date
    #                 df.loc[i + j *3,'Type de Ciblage de la Campagne'] = auto_tag
    #                 df.loc[i + j *3,'Statut de la campagne'] = active_tag
    #             elif i == 3:
    #                 df.loc[i + j *3,'Nom de la Campagne'] = station_split_df.loc[j,'广告活动'] 
    #                 df.loc[i + j *3,"Nom du groupe d'annonces"] = station_split_df.loc[j,'SellSKU']
    #                 df.loc[i + j *3,'Enchère Max'] = station_split_df.loc[j,'max_bid']
    #                 df.loc[i + j *3,"Statut du groupe d’annonces"] = active_tag
    #             else:
    #                 df.loc[i + j *3,'Nom de la Campagne'] = station_split_df.loc[j,'广告活动']
    #                 df.loc[i + j *3,"Nom du groupe d'annonces"] = station_split_df.loc[j,'SellSKU']
    #                 df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
    #                 df.loc[i + j *3,'Statut'] = active_tag     

    
    elif sta == 'IT':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Nome della campagna'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Budget giornaliero campagna'] = cam_budget
                    df.loc[i + j *3,'Data di inizio della campagna'] = cam_start_date
                    df.loc[i + j *3,'Tipo di targeting della campagna'] = auto_tag
                    df.loc[i + j *3,'Stato della campagna'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Nome della campagna'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,"Nome del gruppo di annunci"] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Offerta massima'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,"Stato del gruppo"] = active_tag
                else:
                    df.loc[i + j *3,'Nome della campagna'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,"Nome del gruppo di annunci"] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Stato'] = active_tag     
    
    elif sta == 'IN':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Campaign Daily Budget'] = cam_budget
                    df.loc[i + j *3,'Campaign Start Date'] = cam_start_date
                    df.loc[i + j *3,'Campaign Targeting Type'] = auto_tag
                    df.loc[i + j *3,'Campaign Status'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'Max Bid'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'Ad Group Status'] = active_tag
                else:
                    df.loc[i + j *3,'Campaign Name'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'Ad Group'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'SKU'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'Status'] = active_tag  

    elif sta == 'JP':
        for j in range(0,sku_len):
            for i in range(2,5):
                if i == 2:
                    df.loc[i + j *3,'キャンペーン名'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'1日の平均予算'] = cam_budget
                    df.loc[i + j *3,'開始日'] = cam_start_date
                    df.loc[i + j *3,'ターゲティング'] = auto_tag
                    df.loc[i + j *3,'キャンペーン ステータス'] = active_tag
                elif i == 3:
                    df.loc[i + j *3,'キャンペーン名'] = station_split_df.loc[j,'广告活动'] 
                    df.loc[i + j *3,'広告グループ名'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'入札額'] = station_split_df.loc[j,'max_bid']
                    df.loc[i + j *3,'広告グループ ステータス'] = active_tag
                else:
                    df.loc[i + j *3,'キャンペーン名'] = station_split_df.loc[j,'广告活动']
                    df.loc[i + j *3,'広告グループ名'] = station_split_df.loc[j,'SellSKU']
                    df.loc[i + j *3,'広告(SKU)'] = station_split_df.loc[j,'SellSKU']   
                    df.loc[i + j *3,'ステータス'] = active_tag                      
                    
    else:
        print('此站点不在预设站点%s之内，请检查'%sta)
            
    return df
    
#分割各站点，根据渠道来源生成对应的Excel
def split_station(origin_df):

    station = origin_df['渠道来源']    #获取渠道来源  
    
    station= list(set(station))      #渠道来源去重
    total_station = len(station)
    
    num_station = 1
    
    date = datetime.datetime.today() + datetime.timedelta(days=2)
    
    cam_budget_func = lambda x:5 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(200 if x == 'IN' or x == 'JP' else(6 if x == 'AU' else 8))
        
    cam_start_date_func = lambda x:date.strftime('%m/%d/%Y') if x == 'US' or x == 'CA'  else(date.strftime('%d/%m/%Y') if x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else date.strftime('%Y/%m/%d'))
    
    report_sequence_func = lambda x:1 if x == 'US' else(2 if x == 'CA' else(3 if x == 'MX' else(4 if x == 'UK' else(5 if x == 'DE' else(6 if x == 'FR' else(7 if x == 'IT' else(8 if x == 'ES' else(9 if x == 'JP' else('A' if x == 'IN' else('B' if x == 'AU' else('C' if x == 'AE' else ('D' if x == 'SA' else 'E'))))))))))))

    for i in range(len(origin_df)):
        origin_df.loc[i,'cam_budget'] = cam_budget_func(origin_df.loc[i,'渠道来源'][-2:])
    
    
    for sta in station:
        
        station_split_df = origin_df[origin_df['渠道来源'] == sta]  #分别获取每个渠道的对应数据
        
        station_split_df.reset_index(inplace = True)
        station_split_df = station_split_df.drop('index',axis = 1)
        
        sta_short = sta[-6:] # 6位的渠道
        
        header_df = file_header(sta_short)[0]     #根据函数生成对应的pandas标题的模板
        active_tag = file_header(sta_short)[1]
        auto_tag = file_header(sta_short)[2]
        
        country = sta[-2:]
      
        cam_start_date =  cam_start_date_func(country)        
        cam_budget = cam_budget_func(country)
        #按国别增加序号，方便在系统内进行排序后上传
        report_sequence = report_sequence_func(country)
        shop = sta_short[0:3]
        
        try:

            station_done_df = split_fill_file(station_split_df,header_df,active_tag,auto_tag,cam_budget,cam_start_date,country)
        
            print('文件正在分解，请稍后')
            
            out_path = str(shop) + '-' + str(report_sequence) + '-' + country + '_FBA新品.xlsx'   #注意此处导出为xls格式时会出错；
            station_done_df.to_excel(out_path,index = False) 
            print('第%d个站点分解完成'%num_station)
            num_station += 1
            
        except:
            print('文件分解出错，出错站点为%s'%sta_short)
                            
    print('文件分解成功,总共成功分解%d个，总共有站点%d个'%(num_station -1 ,total_station))    

#主执行程序
if __name__ == '__main__':
    
    print('输入要分解成1V1广告的文件路径（原始的从158系统中导出的）')
    origin_path = input('excel文件：')
    if '"' in origin_path:
        origin_path = origin_path.replace('"','')
    
    creat_filepath(origin_path)
    
       
    sheet = pd.read_excel(origin_path)
    suffix_df = get_suffix(sheet)
    bid_info_df = set_bid(suffix_df)
    
    ad_tag_df = split_ad_tag(bid_info_df)
    
    split_station(ad_tag_df)
    
    cam_origin_data = pd.read_excel(origin_path) 
    ad_tag_df = ad_tag_df.reindex(['渠道来源','ASIN','广告活动','SellSKU','max_bid'],axis = 1)
    writer = pd.ExcelWriter(origin_path)
    cam_origin_data.to_excel(writer,'原始数据',index = False)
    ad_tag_df.to_excel(writer,'已生成的广告活动',index = False)
    writer.save()
    
    print('文件路径已经创建好，请在%s中的‘1V1已分解的文件夹’查看'%origin_path) 
    
    os.chdir(r'E:\01工作资料')  #此处应该是关闭打开的‘1V1文件夹’,可以对文件夹进行剪切移动等操作，但目前未找到对应的操作方法

    print('\n 如果想请清理python内存，请在IPython中输入‘reset’')
