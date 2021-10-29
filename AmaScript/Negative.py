import xlwt, time, xlrd
import pandas as pd

def main():
    
    path = r"D:\data\否定ASIN和关键词\否定关键词ASIN.xlsx"
    
    read_excel(path) 

#读取tableau导出的数据信息
def read_excel(path):
    
    global Campaign_N_info, station
    
    try:
        df = pd.read_excel(path, sheet_name = 0)
        station_set = set(map(lambda x: x[-6:], df['Station']))  
        
        for station in station_set:     
            #获取站点内否定活动名称（去重）
            Campaign_Name_ = list(df.loc[df['Station'] == station]['Campaign Name'])
            
            Campaign_Name_N = list(set(Campaign_Name_))
            Campaign_Name_N.sort(key = Campaign_Name_.index)

            #列表预备接受同站点下所有否定数据dataframe
            Campaign_N_info = []
            
            #循环每个否定数据
            for i in Campaign_Name_N:
                #Step1：获取搜索词数据            
                keywords_step1 = df.loc[(df['Station'] == station) & (df['Campaign Name'] == i)][['Campaign Name',
                                'Ad Group Name','Search Term Type',"Customer Search Terms"]]
            
                #获取ASIN
                keywords_step1_ASIN = keywords_step1[(keywords_step1["Search Term Type"]=="ASIN")]
                keywords_step1_ASIN["Product Targeting ID"] = keywords_step1_ASIN["Customer Search Terms"].map(lambda x:'asin="'+x.upper()+'"')
                keywords_step1_ASIN.drop(["Customer Search Terms"],axis = 1,inplace = True)
                keywords_step1_ASIN["Match Type"]="Negative Targeting Expression"
            
                #获取关键词
                keywords_step1_Keywords = keywords_step1[(keywords_step1["Search Term Type"]=="Keywords")]
                keywords_step1_Keywords["Match Type"]="Negative Exact"

                #合并
                keywords_step2 = pd.concat([keywords_step1_ASIN,keywords_step1_Keywords], axis = 0, sort=False)
                keywords_step2.drop(['Search Term Type'],axis = 1,inplace = True)
                keywords_step2["Status"]="Enabled"

                #增加剩余列
                for b in ["Campaign ID","Campaign_Daily_Budget","Campaign_Start_Date","Campaign End Date",
                       "Campaign_Targeting_Type","Bid","SKU","Campaign Status","Ad Group Status","Bidding strategy"]:

                    keywords_step2[b]=""

                keywords_step3 = keywords_step2[["Campaign ID","Campaign Name","Campaign_Daily_Budget","Campaign_Start_Date",
                                      "Campaign End Date","Campaign_Targeting_Type","Ad Group Name","Bid","SKU",
                                      "Customer Search Terms","Product Targeting ID","Match Type",
                                      "Campaign Status","Ad Group Status","Status","Bidding strategy"]]

                #每个否定数据传入列表储存
                Campaign_N_info.append(keywords_step3)
            
            station_values()
         
    except Exception as e:
        print("读取失败", e)    

#根据站点获取信息填写方式
def station_values():
    
    global sheet_head
    
    try:
        station_type = station[-2:]
        if station_type in ["CA","AU","AE","JP","MX"]:
            station_type = "US"
        if station_type in ["DE","FR","IT","ES","NL","IN"]:
            station_type = "UK"
            
        timeArray = time.localtime(time.time())
        
        station_info = {'US': {'Date': time.strftime("%Y/%m/%d", timeArray),'Manual': 'Manual', 'Status': 'Enabled',
                               'title_name': ['Campaign ID', 'Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', "Product Targeting ID", 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Date': time.strftime("%d/%m/%Y", timeArray),'Manual': 'Manual', 'Status': 'Enabled',
                               'title_name': ['Campaign ID', 'Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type', 'Campaign Status','Ad Group Status', 'Status', 'Bid+']}}
        
        sheet_head = station_info[station_type]['title_name']
   
        write_excel()

    except Exception as e:
        print("获取失败", e)          

#写Excel
def write_excel():
    try:
        pd_save = pd.DataFrame([sheet_head,], columns=sheet_head)

        for i in Campaign_N_info:
            
            i.columns = sheet_head
            pd_save = pd.concat([pd_save, i])

        to_path = r"D:\data\否定ASIN和关键词\否定\{0} 否定广告.xlsx".format(station)

        pd_save.to_excel(excel_writer = to_path, header = None, index = None)

    except Exception as e:
        print("写入失败", e)        
        
        
        

if __name__ == '__main__':
    main()