# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:26:08 2019

@author: Administrator
"""

'''
月日年	US	CA  		
年月日	MX IN 	AU 	JP 	AE
日月年	UK 	DE	FR	IT	ES
测试已通过
'''

import pandas as pd
import os
import datetime
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
'''
#创建文件夹
def creat_filename():
    os.mkdir('拆解完成后的文件')
    print('文件夹创建成功')

#获取要分解的文件
def get_file(path):
    
    try:
        origin_df = pd.read_excel(path)
    except Exception as e:
        print('获取要分解的文件失败',e)  
        
    print('文件读取成功')   
    return origin_df

#根据不同国别生成对应的站点报告的表头格式
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

    
    if station == 'US':      
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
        station_lis = fr_lis
        active_tag = 'Enabled'#'Activé'
        auto_tag = 'Auto'# 'Automatique'
                
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

#根据表头文件和对应站点参数进行文件的拆分
def split_file(sta,header_df,active_tag,auto_tag,cam_budget,cam_name,max_bid,cam_start_date,get_sellerSKU):
    sta = sta[-2:]
    i = 0
    j = 2
    header_df = header_df
    sku_len = len(get_sellerSKU)
    if sta == 'US' or sta == 'MX' or sta == 'AU' or sta == 'AE':
        header_df.loc[i,'Campaign'] =  cam_name
        header_df.loc[i,'Campaign Daily Budget'] = cam_budget  
        header_df.loc[i,'Campaign Start Date'] = cam_start_date
        header_df.loc[i,'Campaign Targeting Type'] = auto_tag
        header_df.loc[i,'Campaign Status'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Campaign'] =  cam_name
            header_df.loc[i,'Ad Group'] = sku
            header_df.loc[i,'Max Bid'] = max_bid
            header_df.loc[i,'Ad Group Status'] = active_tag
            i = i +1

        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Campaign'] =  cam_name
            header_df.loc[sku_len + j,'Ad Group'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Status'] = active_tag
            j += 1
    
    elif sta == 'CA':
        header_df.loc[i,'Campaign Name'] =  cam_name
        header_df.loc[i,'Campaign Daily Budget'] = cam_budget  
        header_df.loc[i,'Campaign Start Date'] = cam_start_date
        header_df.loc[i,'Campaign Targeting Type'] = auto_tag
        header_df.loc[i,'Campaign Status'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Campaign Name'] =  cam_name
            header_df.loc[i,'Ad Group'] = sku
            header_df.loc[i,'Max Bid'] = max_bid
            header_df.loc[i,'Ad Group Status'] = active_tag
            i = i +1

        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Campaign Name'] =  cam_name
            header_df.loc[sku_len + j,'Ad Group'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Status'] = active_tag
            j += 1
        
    elif sta == 'UK'or sta == 'ES' or sta == 'FR':   
        header_df.loc[i,'Campaign Name'] =  cam_name
        header_df.loc[i,'Campaign Daily Budget'] = cam_budget  
        header_df.loc[i,'Campaign Start Date'] = cam_start_date   #日期要求格式不一样，可能此处会出错  17/10/2019
        header_df.loc[i,'Campaign Targeting Type'] = auto_tag
        header_df.loc[i,'Campaign Status'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Campaign Name'] =  cam_name
            header_df.loc[i,'Ad Group Name'] = sku
            header_df.loc[i,'Max Bid'] = max_bid
            header_df.loc[i,'Ad Group Status'] = active_tag
            i = i +1
    
        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Campaign Name'] =  cam_name
            header_df.loc[sku_len + j,'Ad Group Name'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Status'] = active_tag
            j += 1

        
    elif sta == 'DE':   
        header_df.loc[i,'Kampagne'] =  cam_name
        header_df.loc[i,'Tagesbudget Kampagne'] = cam_budget  
        header_df.loc[i,'Startdatum der Kampagne'] = cam_start_date   #日期要求格式不一样，可能此处会出错
        header_df.loc[i,'Ausrichtungstyp der Kampagne'] = auto_tag
        header_df.loc[i,'Kampagnenstatus'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Kampagne'] =  cam_name
            header_df.loc[i,'Anzeigengruppe'] = sku
            header_df.loc[i,'Maximales Gebot'] = max_bid
            header_df.loc[i,'Anzeigengruppe Status'] = active_tag
            i = i +1
    
        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Kampagne'] =  cam_name
            header_df.loc[sku_len + j,'Anzeigengruppe'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Status'] = active_tag
            j += 1
              
    # elif sta == 'FR':   
    #     header_df.loc[i,'Nom de la Campagne'] =  cam_name
    #     header_df.loc[i,'Budget quotidien de la Campagne'] = cam_budget  
    #     header_df.loc[i,'Date de début de la Campagne'] = cam_start_date   #日期要求格式不一样，可能此处会出错
    #     header_df.loc[i,'Type de Ciblage de la Campagne'] = auto_tag
    #     header_df.loc[i,'Statut de la campagne'] = active_tag
    #     i += 1
    #     for sku in get_sellerSKU:
    #         header_df.loc[i,'Nom de la Campagne'] =  cam_name
    #         header_df.loc[i,"Nom du groupe d'annonces"] = sku
    #         header_df.loc[i,'Enchère Max'] = max_bid
    #         header_df.loc[i,"Statut du groupe d’annonces"] = active_tag
    #         i = i +1
    
    #     for sku in get_sellerSKU:
    #         header_df.loc[sku_len + j,'Nom de la Campagne'] =  cam_name
    #         header_df.loc[sku_len + j,"Nom du groupe d'annonces"] = sku
    #         header_df.loc[sku_len + j,'SKU'] = sku
    #         header_df.loc[sku_len + j,'Statut'] = active_tag
            j += 1
             
    elif sta == 'IT':   
        header_df.loc[i,'Nome della campagna'] =  cam_name
        header_df.loc[i,'Budget giornaliero campagna'] = cam_budget  
        header_df.loc[i,'Data di inizio della campagna'] = cam_start_date   #日期要求格式不一样，可能此处会出错
        header_df.loc[i,'Tipo di targeting della campagna'] = auto_tag
        header_df.loc[i,'Stato della campagna'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Nome della campagna'] =  cam_name
            header_df.loc[i,'Nome del gruppo di annunci'] = sku
            header_df.loc[i,'Offerta massima'] = max_bid
            header_df.loc[i,'Stato del gruppo'] = active_tag
            i = i +1
    
        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Nome della campagna'] =  cam_name
            header_df.loc[sku_len + j,'Nome del gruppo di annunci'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Stato'] = active_tag
            j += 1
    
    elif sta == 'IN':   
        header_df.loc[i,'Campaign Name'] =  cam_name
        header_df.loc[i,'Campaign Daily Budget'] = cam_budget  
        header_df.loc[i,'Campaign Start Date'] = cam_start_date   #日期要求格式不一样，可能此处会出错
        header_df.loc[i,'Campaign Targeting Type'] = auto_tag
        header_df.loc[i,'Campaign Status'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'Campaign Name'] =  cam_name
            header_df.loc[i,'Ad Group'] = sku
            header_df.loc[i,'Max Bid'] = max_bid
            header_df.loc[i,'Ad Group Status'] = active_tag
            i = i +1
    
        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'Campaign Name'] =  cam_name
            header_df.loc[sku_len + j,'Ad Group'] = sku
            header_df.loc[sku_len + j,'SKU'] = sku
            header_df.loc[sku_len + j,'Status'] = active_tag
            j += 1

    elif sta == 'JP':   
        header_df.loc[i,'キャンペーン名'] =  cam_name
        header_df.loc[i,'1日の平均予算'] = cam_budget  
        header_df.loc[i,'開始日'] = cam_start_date   #日期要求格式不一样，可能此处会出错
        header_df.loc[i,'ターゲティング'] = auto_tag
        header_df.loc[i,'キャンペーン ステータス'] = active_tag
        i += 1
        for sku in get_sellerSKU:
            header_df.loc[i,'キャンペーン名'] =  cam_name
            header_df.loc[i,'広告グループ名'] = sku
            header_df.loc[i,'入札額'] = max_bid
            header_df.loc[i,'広告グループ ステータス'] = active_tag
            i = i +1
    
        for sku in get_sellerSKU:
            header_df.loc[sku_len + j,'キャンペーン名'] =  cam_name
            header_df.loc[sku_len + j,'広告グループ名'] = sku
            header_df.loc[sku_len + j,'広告(SKU)'] = sku
            header_df.loc[sku_len + j,'ステータス'] = active_tag
            j += 1
        
    else:
        print('此站点不在预设站点%s之内，请检查'%sta)
            
    return header_df
         
    
#文件表头信息生产，并返回成功分解后的文件    
def table_info_file(file_path):
    
    origin_df = get_file(file_path)
    
    station = origin_df['渠道来源']    #获取渠道来源
    
    station= list(set(station))      #渠道来源去重
    
    #station_short = station[-6:]
    date = datetime.datetime.today() + datetime.timedelta(days=2)
    
    cam_budget_func = lambda x:200 if x == 'US' or x == 'CA' or x == 'MX' or x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' or x == 'AU' or x == 'AE' else(5000 if x == 'IN' else 6000)
    
    max_bid_func = lambda x:0.06 if x == 'US' or x == 'CA' else(0.05 if x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else(1 if x == 'IN' else (5 if x == 'JP' else (0.12 if x == 'AU' else(0.24 if x == 'AE' else 0.7)))))
    
    cam_start_date_func = lambda x:date.strftime('%m/%d/%Y') if x == 'US' or x == 'CA'   else(date.strftime('%d/%m/%Y') if x == 'UK' or x == 'DE' or x == 'FR' or x == 'IT' or x == 'ES' else date.strftime('%Y/%m/%d'))

    report_sequence_func = lambda x:1 if x == 'US' else(2 if x == 'CA' else(3 if x == 'MX' else(4 if x == 'UK' else(5 if x == 'DE' else(6 if x == 'FR' else(7 if x == 'IT' else(8 if x == 'ES' else(9 if x == 'JP' else('A' if x == 'IN' else('B' if x == 'AU' else('C' if x == 'AE' else 'D')))))))))))

    for sta in station:
        
        station_split_df = origin_df[origin_df['渠道来源'] == sta]  #分别获取每个渠道的对应数据
        
        sta_short = sta[-6:]
        
        header_df = file_header(sta_short)[0]     #根据函数生成对应的pandas标题的模板
        active_tag = file_header(sta_short)[1]
        auto_tag = file_header(sta_short)[2]
        
        cam_name = sta_short + '-2020_万圣节' 
        
        cam_budget = cam_budget_func(sta[-2:])
        
        max_bid = max_bid_func(sta[-2:])
        
        cam_start_date =  cam_start_date_func(sta[-2:])    #此处的日期可能有问题先暂时考虑
        
        get_sellerSKU = station_split_df['SellSKU']    #提取渠道sku
        
        #按国别增加序号，方便在系统内进行排序后上传
        country = sta_short[-2:]
        report_sequence = report_sequence_func(country)
        shop = sta_short[0:3]
        
        station_done_df = split_file(sta,header_df,active_tag,auto_tag,cam_budget,cam_name,max_bid,cam_start_date,get_sellerSKU)
        
        print('文件正在分解，请稍后')
          
        out_path = str(shop) + '-' + str(report_sequence) + '-' + country  + '-万圣' + '.xlsx'  
      
        station_done_df.to_excel(out_path,index = False)    
        
        print('文件分解成功')
        
if __name__ == '__main__':
    
    print('\n请不要修改广告活动名称（后续新增会在原广告活动中添加），原始158导出文件;\n')
    path = input('文件：')
    if '"' in path:
        path = path.replace('"','')
    
    current_path = os.path.dirname(path)
    os.chdir(current_path)
    if not os.path.exists('万圣-1VN已分解文件'):
        os.mkdir('万圣-1VN已分解文件')
    
    os.chdir('万圣-1VN已分解文件')
    table_info_file(path)
    print('文件分解成功，请在路径中%s的‘1VN已分解文件’查看'%current_path)
    os.chdir(r'E:\01工作资料')

