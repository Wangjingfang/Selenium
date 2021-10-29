import xlwt, time, xlrd
import pandas as pd

def main():
    
    path = r"D:\data\开手动的\手动模板.xlsx"
    campaign_budget = 8.07
    group_default_bid = 0.03
    
    #不同组的竞价增幅倍率
    asin_up = 1
    broad_up = 1
    phrase_up = 1.2
    exact_up = 1.5
    
    #词组和精确的判断标准：>=
    phrase_cr = 0.12
    phrase_order = 3
    exact_cr = 0.2
    exact_order = 3
    
    read_excel(path,campaign_budget,group_default_bid,asin_up,broad_up,phrase_up,exact_up,phrase_cr,phrase_order,exact_cr,exact_order) 

#读取tableau导出的数据信息
def read_excel(path,campaign_budget,group_default_bid,asin_up,broad_up,phrase_up,exact_up,phrase_cr,phrase_order,exact_cr,exact_order):
    
    global Campaign_M_info, station
    
    try:
        df = pd.read_excel(path, sheet_name = 0)
        station_set = set(map(lambda x: x[-6:], df['Station']))  
        
        for station in station_set:     
            #获取站点内手动活动名称（去重）
            Campaign_Name_ = list(df.loc[df['Station'] == station]['Campaign Name_M'])
            Campaign_Name_M = list(set(Campaign_Name_))
            Campaign_Name_M.sort(key = Campaign_Name_.index)
            
            #列表预备接受同站点下所有手动数据dataframe
            Campaign_M_info = []
            
            #循环每个手动数据
            for i in Campaign_Name_M:
                
                #获取手动的sku
                SellSKU = df.loc[(df['Station'] == station) & (df['Campaign Name_M'] == i)]['SellSKU'].iloc[0]
                
                #Step1：获取搜索词数据，搜索词默认Broad，待判断Phrase、Exact              
                keywords_step1 = df.loc[(df['Station'] == station) & (df['Campaign Name_M'] == i)][['Search Term Type',
                                'Customer Search Terms','Bid',"CR","Orders"]]
                keywords_step1.replace({"Keywords":"Broad"}, inplace = True)                                       
                
                #获取ASIN,搜索词值改到Product Targeting ID列
                keywords_step1_ASIN = keywords_step1[(keywords_step1["Search Term Type"]=="ASIN")]
                keywords_step1_ASIN["Product Targeting ID"] = keywords_step1_ASIN["Customer Search Terms"]
                keywords_step1_ASIN.drop(["Customer Search Terms"],axis = 1,inplace = True)
                keywords_step1_ASIN["Bid"] = keywords_step1_ASIN["Bid"].map(lambda x:x*asin_up)
                keywords_step1_ASIN["Product Targeting ID"] = keywords_step1_ASIN["Product Targeting ID"].map(lambda x:'asin="'+x.upper()+'"')
                
                #获取Broad
                keywords_step1_Broad = keywords_step1[(keywords_step1["Search Term Type"]=="Broad")]
                keywords_step1_Broad["Bid"] = keywords_step1_Broad["Bid"].map(lambda x:x*broad_up)
                
                #获取Phrase
                keywords_step1_Phrase = keywords_step1[(keywords_step1["Search Term Type"]=="Broad") & (keywords_step1.Orders>=phrase_order)&
                                                       (keywords_step1.CR>=phrase_cr)]
                keywords_step1_Phrase.replace({"Broad":"Phrase"}, inplace = True)
                keywords_step1_Phrase["Bid"] = keywords_step1_Phrase["Bid"].map(lambda x:x*phrase_up)
                
                #获取Exact
                keywords_step1_Exact = keywords_step1[(keywords_step1["Search Term Type"]=="Broad") & (keywords_step1.Orders>=exact_order)&
                                                      (keywords_step1.CR>=exact_cr)]
                keywords_step1_Exact.replace({"Broad":"Exact"}, inplace = True)
                keywords_step1_Exact["Bid"] = keywords_step1_Exact["Bid"].map(lambda x:x*exact_up)
                
                #组信息
                keywords_step1_group = pd.DataFrame({"Search Term Type":["Type","Type"],"Bid":[group_default_bid,""],"SKU":["_",SellSKU]})
                keywords_step1_group_ASIN = keywords_step1_group.replace("Type","ASIN")
                keywords_step1_group_Broad = keywords_step1_group.replace("Type","Broad")
                keywords_step1_group_Phrase = keywords_step1_group.replace("Type","Phrase")
                keywords_step1_group_Exact = keywords_step1_group.replace("Type","Exact")
                
                #活动信息
                keywords_step1_campaign = pd.DataFrame({"Campaign":[i,""],
                                           "Campaign Daily Budget":[campaign_budget,""],
                                           "Campaign Start Date":[time.strftime("%Y/%m/%d", time.localtime(time.time())),""],
                                           "Campaign Targeting Type":["Manual",""]})
                
                
                #Step2：以活动+组名+组手动词的顺序拼接dataframe,然后添加其他列信息
                keywords_step2 = pd.concat([keywords_step1_campaign,
                                   keywords_step1_group_ASIN,keywords_step1_ASIN,
                                   keywords_step1_group_Broad,keywords_step1_Broad,
                                   keywords_step1_group_Phrase,keywords_step1_Phrase,
                                   keywords_step1_group_Exact,keywords_step1_Exact], axis = 0, sort=False)  
                keywords_step2.index = range(len(keywords_step2))
                keywords_step2.drop([1],inplace = True)
                keywords_step2.drop(["CR","Orders"],axis = 1, inplace = True)
                
                #判断哪个组不存在数据，删除组
                for j, element in enumerate([keywords_step1_ASIN,keywords_step1_Broad,keywords_step1_Phrase,keywords_step1_Exact]):
                    if len(element) == 0:
                        keywords_step2 = keywords_step2.drop(index = (keywords_step2.loc[(keywords_step2["Search Term Type"]==
                                    ["ASIN","Broad","Phrase","Exact"][j])].index))
                #替换列标题空格，替换None值，方便定位
                keywords_step2.rename(columns=lambda x:x.replace(' ','_'), inplace=True)
                keywords_step2.replace({None:"_"}, inplace = True)
                
                #增加活动名字列
                keywords_step2["Campaign"] = i
                
                #增加Match Type
                keywords_step2.loc[keywords_step2.Product_Targeting_ID!="_","Match Type"]="Targeting Expression"
                for x in ["Broad","Phrase","Exact"]:
                    keywords_step2.loc[(keywords_step2.Search_Term_Type==x)&(keywords_step2.Customer_Search_Terms!="_"),"Match Type"]=x
                
                #增加Campaign Status列
                keywords_step2.loc[keywords_step2.Campaign_Targeting_Type=="Manual","Campaign Status"]="Enabled"
                
                #增加Ad Group Status列
                keywords_step2.loc[keywords_step2.Bid==group_default_bid,"Ad Group Status"]="Enabled"
                
                #增加Status列
                for a in [keywords_step2.Customer_Search_Terms,keywords_step2.Product_Targeting_ID,keywords_step2.SKU]:
                    keywords_step2.loc[a!="_","Status"]="Enabled"
                
                #增加剩余3列
                for b in ["Campaign ID","Campaign End Date","Bidding strategy"]:
                    keywords_step2[b]=""
                
                #清除多余值
                for c in [None,"_"]:
                    keywords_step2.replace({c:""}, inplace = True)
                    
                keywords_step3 = keywords_step2[["Campaign ID","Campaign","Campaign_Daily_Budget","Campaign_Start_Date","Campaign End Date","Campaign_Targeting_Type","Search_Term_Type","Bid","SKU","Customer_Search_Terms","Product_Targeting_ID","Match Type","Campaign Status","Ad Group Status","Status","Bidding strategy"]]

                #每个手动数据传入列表储存
                Campaign_M_info.append(keywords_step3)
                
            station_values()

    except Exception as e:
        print("读取失败", e)    

        
#根据站点获取信息填写方式
def station_values():
    
    global campaign_date,sheet_head,campaign_budget
    
    try:
        station_type = station[-2:]
        if station_type in ["CA","AU","AE","JP","MX"]:
            station_type = "US"
        if station_type in ["DE","FR","IT","ES","IN"]:
            station_type = "UK"
            
        timeArray = time.localtime(time.time())
        
        station_info = {'US': {'Date': time.strftime("%Y/%m/%d", timeArray),
                               'title_name': ['Campaign ID', 'Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', "Product Targeting ID", 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Date': time.strftime("%d/%m/%Y", timeArray),
                               'title_name': ['Campaign ID', 'Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type', 'Campaign Status','Ad Group Status', 'Status', 'Bid+']}}
        campaign_date = station_info[station_type]['Date']
        sheet_head = station_info[station_type]['title_name']
            
        write_excel()

    except Exception as e:
        print("获取失败", e)       
    
    
#写Excel
def write_excel():
    try:
        pd_save = pd.DataFrame([sheet_head,], columns=sheet_head)

        for i in Campaign_M_info:
            
            i.columns = sheet_head
            i.loc[0,"Campaign Start Date"] = campaign_date
            pd_save = pd.concat([pd_save, i])

        to_path = r"D:\data\开手动的\手动结果\{0}-手动广告.xlsx".format(station)

        pd_save.to_excel(excel_writer = to_path, header = None, index = None)

    except Exception as e:
        print("写入失败", e)


if __name__ == '__main__':
    main()