# -*- coding: utf-8 -*-

"""
@Author: MarlonYang

@Date  : 2020/11/18 17:21

@File  : submit_campaign_M.py

@Desc  : 广告搜索词批量投放手动的数据处理脚本
需要的数据列：'Station','Campaign Name_M','SellSKU','Search Term Type','Customer Search Terms','Bid',"CR","Orders","ACoS"

1. 符合标准的出单词，乘以倍率后，正常投放至,ASIN,Broad,Phrase,Exact组
2. 不符合标准的出单词，将投放至ASIN_Pending,Broad_Pending组，并按照市场限制最高竞价

*** 每次批量投放手动广告时，以上6个组都会被创建并添加SellSKU，即使组内没有关键词(categories组暂时不添加)
*** 如果同station、同ASIN下不同SellSKU都有备货，则使用另一个脚本：Maunal_Add_sku.py，可以添加新SellSKU至以上6个组
*** 若不需要，可在190-193行处删除注释，即可删除不存在关键词数据的组


@2021/1/28 更新：
1. 保留每次批量投放的手动匹配类型和关键词等4个字段：'Station','Campaign Name_M','Search Term Type', 'Customer Search Terms'
    存储路径为data_to_save
2. 下一次执行手动脚本时，会于历史保留的投放数据比对，仅保留不重复的手动投放，本次数据源路径为data_to_current


"""

import time
import pandas as pd

def main():
    
    path = r"D:\data\开手动的\teableau关键词数据表.xlsx"
    data_to_save = r"D:\data\开手动的\历史手动广告投放词.xlsx"
    data_to_current = r"D:\data\开手动的\本次手动广告投放词.xlsx"
    campaign_budget = 10
    group_default_bid = 0.02
    
    #不同组的竞价增幅倍率
    asin_up = 1
    broad_up = 1
    phrase_up = 1.2
    exact_up = 1.5
    
    #手动不同匹配类型的判断标准
    base_acos = 0.18
    base_cr = 0.08
    base_order = 3
    phrase_cr = 0.1
    phrase_order = 4
    exact_cr = 0.18
    exact_order = 5

    #不符合标准的出单词（pending）将限制最高竞价
    base_bid_us_ca = 0.08
    base_bid_uk_de = 0.06
    base_bid_fr_it_es = 0.04

    keywords_data = read_excel(path,data_to_save,data_to_current,base_acos,base_cr,base_order,phrase_cr,phrase_order,exact_cr,exact_order)

    data_to_campaign(keywords_data,campaign_budget,group_default_bid,asin_up,broad_up,phrase_up,exact_up,base_bid_us_ca,base_bid_uk_de,base_bid_fr_it_es)

#读取tableau导出的数据信息
def read_excel(path,data_to_save,data_to_current,base_acos,base_cr,base_order,phrase_cr,phrase_order,exact_cr,exact_order):

    try:
        df = pd.read_excel(path, sheet_name = 0)

        # Step1：获取搜索词数据，搜索词默认Broad，待判断Phrase、Exact
        keywords_step1 = df[['Station','Campaign Name_M','SellSKU','Search Term Type', 'Customer Search Terms', 'Bid', "CR", "Orders", "Acos"]]
        keywords_step1.replace({"Keywords": "Broad"}, inplace=True)

        #获取ASIN和ASIN_pending
        keywords_step1_ASIN_total = keywords_step1[(keywords_step1["Search Term Type"] == "ASIN")]
        keywords_step1_ASIN = keywords_step1[(keywords_step1["Search Term Type"] == "ASIN") & (keywords_step1.Orders >= base_order) & (keywords_step1.CR >= base_cr) & (keywords_step1.Acos <= base_acos)]
        keywords_step1_ASIN_total_concat = pd.concat([keywords_step1_ASIN, keywords_step1_ASIN_total], axis=0)
        keywords_step1_ASIN_total_concat = keywords_step1_ASIN_total_concat.drop_duplicates()
        keywords_step1_ASIN_pending = keywords_step1_ASIN_total_concat[keywords_step1_ASIN.shape[0]:]
        keywords_step1_ASIN_pending.replace({"ASIN": "ASIN_Pending"}, inplace=True)

        #获取Broad和Broad_pending
        keywords_step1_Broad_total = keywords_step1[(keywords_step1["Search Term Type"] == "Broad")]
        keywords_step1_Broad = keywords_step1[(keywords_step1["Search Term Type"] == "Broad") & (keywords_step1.Orders >= base_order) & (keywords_step1.CR >= base_cr) & (keywords_step1.Acos <= base_acos)]
        keywords_step1_Broad_total_concat = pd.concat([keywords_step1_Broad, keywords_step1_Broad_total], axis=0)
        keywords_step1_Broad_total_concat = keywords_step1_Broad_total_concat.drop_duplicates()
        keywords_step1_Broad_pending = keywords_step1_Broad_total_concat[keywords_step1_Broad.shape[0]:]
        keywords_step1_Broad_pending.replace({"Broad": "Broad_Pending"}, inplace=True)

        #获取Phrase
        keywords_step1_Phrase = keywords_step1[(keywords_step1["Search Term Type"] == "Broad") & (keywords_step1.Orders >= phrase_order) & (keywords_step1.CR >= phrase_cr) & (keywords_step1.Acos <= base_acos)]
        keywords_step1_Phrase.replace({"Broad": "Phrase"}, inplace=True)

        #获取Exact
        keywords_step1_Exact = keywords_step1[(keywords_step1["Search Term Type"] == "Broad") & (keywords_step1.Orders >= exact_order) & (keywords_step1.CR >= exact_cr) & (keywords_step1.Acos <= base_acos)]
        keywords_step1_Exact.replace({"Broad": "Exact"}, inplace=True)

        # Step2：合并以上6个组
        keywords_step2 = pd.concat([keywords_step1_ASIN,keywords_step1_ASIN_pending,keywords_step1_Broad,keywords_step1_Broad_pending,keywords_step1_Phrase,keywords_step1_Exact], axis = 0, sort=False)

        #各项手动投放词存储
        previous_keywords = pd.read_excel(data_to_save, sheet_name=0)
        keywords_info = keywords_step2[['Station','Campaign Name_M','Search Term Type', 'Customer Search Terms']]
        keywords_info_to_save = pd.concat([previous_keywords, keywords_info], axis=0, sort=False)
        keywords_info_to_save = keywords_info_to_save.drop_duplicates()
        keywords_info_to_save.to_excel(excel_writer=data_to_save, index=None)

        # Step3：非重复关键词
        keywords_step3 = keywords_info_to_save[previous_keywords.shape[0]:]
        keywords_step3 = pd.merge(keywords_step3,keywords_step2,how="left")

        #此次手动投放的数据源
        keywords_step3.to_excel(excel_writer=data_to_current, index=None)

        return keywords_step3

    except Exception as e:
        print("读取失败", e)    

def data_to_campaign(keywords_data,campaign_budget,group_default_bid,asin_up,broad_up,phrase_up,exact_up,base_bid_us_ca,base_bid_uk_de,base_bid_fr_it_es):

    global Campaign_M_info, station

    try:
        station_set = set(map(lambda x: x[-6:], keywords_data['Station']))

        for station in station_set:
            # 获取站点内手动活动名称（去重）
            Campaign_Name_ = list(keywords_data.loc[keywords_data['Station'] == station]['Campaign Name_M'])
            Campaign_Name_M = list(set(Campaign_Name_))
            Campaign_Name_M.sort(key=Campaign_Name_.index)

            # 列表预备接受同站点下所有手动数据dataframe
            Campaign_M_info = []

            # 循环每个手动数据
            for i in Campaign_Name_M:

                # 获取手动的sku
                SellSKU = keywords_data.loc[(keywords_data['Station'] == station) & (keywords_data['Campaign Name_M'] == i)]['SellSKU'].iloc[0]

                # Step1：获取搜索词数据
                keywords_step1 = keywords_data.loc[(keywords_data['Station'] == station) & (keywords_data['Campaign Name_M'] == i)][['Search Term Type', 'Customer Search Terms', 'Bid', "CR", "Orders", "Acos"]]

                # 获取手动投放的6个组
                keywords_step1_ASIN_pending = keywords_step1[(keywords_step1["Search Term Type"] == "ASIN_Pending")]
                keywords_step1_Broad_pending = keywords_step1[(keywords_step1["Search Term Type"] == "Broad_Pending")]
                keywords_step1_ASIN = keywords_step1[(keywords_step1["Search Term Type"] == "ASIN")]
                keywords_step1_Broad = keywords_step1[(keywords_step1["Search Term Type"] == "Broad")]
                keywords_step1_Phrase = keywords_step1[(keywords_step1["Search Term Type"] == "Phrase")]
                keywords_step1_Exact = keywords_step1[(keywords_step1["Search Term Type"] == "Exact")]

                #两个ASIN组设置Targeting
                for x in [keywords_step1_ASIN_pending,keywords_step1_ASIN]:
                    x["Product Targeting ID"] = x["Customer Search Terms"].map(lambda x: 'asin="' + x.upper() + '"')
                    x.drop(["Customer Search Terms"], axis=1, inplace=True)

                #两个Pending组限制最高竞价
                for y in [keywords_step1_ASIN_pending, keywords_step1_Broad_pending]:
                    if station[-2:] in ["US", "CA"]:
                        y["Bid"] = y["Bid"].map(lambda x: base_bid_us_ca if round(x * broad_up, 2) > base_bid_us_ca else round(x * broad_up, 2))
                    elif station[-2:] in ["UK", "DE"]:
                        y["Bid"] = y["Bid"].map(lambda x: base_bid_uk_de if round(x * broad_up, 2) > base_bid_uk_de else round(x * broad_up, 2))
                    elif station[-2:] in ["FR", "IT", "ES"]:
                        y["Bid"] = y["Bid"].map(lambda x: base_bid_fr_it_es if round(x * broad_up, 2) > base_bid_fr_it_es else round(x * broad_up, 2))
                    else:
                        y["Bid"] = y["Bid"].map(lambda x: round(x * broad_up, 2))

                #正常四组设置竞价增幅
                keywords_step1_ASIN["Bid"] = keywords_step1_ASIN["Bid"].map(lambda x: round(x * asin_up, 2))
                keywords_step1_Broad["Bid"] = keywords_step1_Broad["Bid"].map(lambda x: round(x * broad_up, 2))
                keywords_step1_Phrase["Bid"] = keywords_step1_Phrase["Bid"].map(lambda x: round(x * phrase_up, 2))
                keywords_step1_Exact["Bid"] = keywords_step1_Exact["Bid"].map(lambda x: round(x * exact_up, 2))

                # 组信息
                keywords_step1_group = pd.DataFrame({"Search Term Type": ["Type", "Type"], "Bid": [group_default_bid, ""], "SKU": ["_", SellSKU]})

                # Step2：以活动+组名+组手动词的顺序拼接dataframe,然后添加其他列信息
                keywords_step2 = pd.concat([pd.DataFrame({"Campaign": [i, ""], "Campaign Daily Budget": [campaign_budget, ""], "Campaign Start Date": ["", ""], "Campaign Targeting Type": ["Manual", ""]}),
                                            keywords_step1_group.replace("Type", "ASIN"), keywords_step1_ASIN,
                                            keywords_step1_group.replace("Type", "ASIN_Pending"), keywords_step1_ASIN_pending,
                                            keywords_step1_group.replace("Type", "Broad"), keywords_step1_Broad,
                                            keywords_step1_group.replace("Type", "Broad_Pending"), keywords_step1_Broad_pending,
                                            keywords_step1_group.replace("Type", "Phrase"), keywords_step1_Phrase,
                                            keywords_step1_group.replace("Type", "Exact"), keywords_step1_Exact], axis=0, sort=False)
                keywords_step2.index = range(len(keywords_step2))
                keywords_step2.drop([1], inplace=True)
                keywords_step2.drop(["CR", "Orders"], axis=1, inplace=True)

                # 判断哪个组不存在数据，删除组
                # for j, element in enumerate([keywords_step1_ASIN,keywords_step1_ASIN_pending,keywords_step1_Broad,keywords_step1_Broad_pending,keywords_step1_Phrase,keywords_step1_Exact]):
                #     if len(element) == 0:
                #         keywords_step2 = keywords_step2.drop(index = (keywords_step2.loc[(keywords_step2["Search Term Type"]==["ASIN","ASIN_Pending","Broad","Broad_Pending","Phrase","Exact"][j])].index))

                # 替换列标题空格，替换None值，方便定位
                keywords_step2.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
                keywords_step2.replace({None: "_"}, inplace=True)

                # 增加活动名字列
                keywords_step2["Campaign"] = i

                # 增加Match Type
                keywords_step2.loc[keywords_step2.Product_Targeting_ID != "_", "Match Type"] = "Targeting Expression"
                for z in ["Broad", "Phrase", "Exact"]:
                    keywords_step2.loc[(keywords_step2.Search_Term_Type == z) & (keywords_step2.Customer_Search_Terms != "_"), "Match Type"] = z
                keywords_step2.loc[(keywords_step2.Search_Term_Type == "Broad_Pending") & (keywords_step2.Customer_Search_Terms != "_"), "Match Type"] = "Broad"

                # 增加Campaign Status列
                keywords_step2.loc[keywords_step2.Campaign_Targeting_Type == "Manual", "Campaign Status"] = "Enabled"

                # 增加Ad Group Status列
                keywords_step2.loc[keywords_step2.Bid == group_default_bid, "Ad Group Status"] = "Enabled"

                # 增加Status列
                for a in [keywords_step2.Customer_Search_Terms, keywords_step2.Product_Targeting_ID, keywords_step2.SKU]:
                    keywords_step2.loc[a != "_", "Status"] = "Enabled"

                # 增加剩余3列
                for b in ["Campaign ID", "Campaign End Date", "Bidding strategy"]:
                    keywords_step2[b] = ""

                # 变更组名：SellSKU + targeting
                # keywords_step2["Search_Term_Type"] = keywords_step2["Search_Term_Type"].map(lambda x:"_" if x == "_" else (SellSKU+" ASIN" if x=="ASIN" else SellSKU+" Keywords"))

                # 清除多余值
                for c in [None, "_"]:
                    keywords_step2.replace({c: ""}, inplace=True)

                keywords_step3 = keywords_step2[
                    ["Campaign ID", "Campaign", "Campaign_Daily_Budget", "Campaign_Start_Date", "Campaign End Date",
                     "Campaign_Targeting_Type", "Search_Term_Type", "Bid", "SKU", "Customer_Search_Terms",
                     "Product_Targeting_ID", "Match Type", "Campaign Status", "Ad Group Status", "Status",
                     "Bidding strategy"]]

                # 每个手动数据传入列表储存
                Campaign_M_info.append(keywords_step3)

            station_values()

    except Exception as e:
        print("计算失败", e)

#根据站点获取信息填写方式
def station_values():
    
    global campaign_date,sheet_head,campaign_budget,Campaign_Start_Date,campaign_type,campaign_status
    
    try:
        station_type = station[-2:]
        if station_type in ["CA","MX"]:
            station_type = "US"
        if station_type in ["DE","FR","IT","ES"]:
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
        campaign_date = station_info[station_type]['Date']
        sheet_head = station_info[station_type]['title_name']
        campaign_type = station_info[station_type]['Manual']
        campaign_status = station_info[station_type]['Status']
        Campaign_Start_Date = station_info[station_type]['title_name'][3]

        write_excel()

    except Exception as e:
        print("获取失败", e)       

#写Excel
def write_excel():
    try:
        pd_save = pd.DataFrame([sheet_head,], columns=sheet_head)

        for i in Campaign_M_info:
            
            i.columns = sheet_head
            i.loc[0,Campaign_Start_Date] = campaign_date
            i.replace({"Enabled":campaign_status}, inplace = True)
            i.replace({"Manual":campaign_type}, inplace = True)
            pd_save = pd.concat([pd_save, i])

        to_path = r"D:\data\开手动的\手动结果\{0}-手动广告.xlsx".format(station)

        pd_save.to_excel(excel_writer = to_path, header = None, index = None)

    except Exception as e:
        print("写入失败", e)

if __name__ == '__main__':
    main()