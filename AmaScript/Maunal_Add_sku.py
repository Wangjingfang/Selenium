# -*- coding: utf-8 -*-

"""
@Author: MarlonYang

@Date  : 2021/1/19 17:12

@File  : Maunal_Add_sku.py

@Desc  : 为已有的手动广告中添加新的渠道sku
需要的数据列：'Station','Campaign Name_M','SellSKU'

此脚本是为了配合批量手动广告新增sku，因此会向6个手动组内都加入新渠道sku（ASIN,ASIN_Pending,Broad,Broad_Pending,Phrase,Exact）

"""

import pandas as pd

def main():

    path = r"D:\PycharmProjects\AmaScript\补渠道sku.xlsx"

    read_excel(path)

# 读取tableau导出的数据信息
def read_excel(path):

    global Campaign_M_info, station

    try:
        df = pd.read_excel(path, sheet_name=0)
        station_set = set(map(lambda x: x[-6:], df['Station']))

        for station in station_set:
            # 获取站点内手动活动名称（去重）
            Campaign_Name_ = list(df.loc[df['Station'] == station]['Campaign Name_M'])
            Campaign_Name_M = list(set(Campaign_Name_))
            Campaign_Name_M.sort(key=Campaign_Name_.index)

            # 列表预备接受同站点下所有手动数据dataframe
            Campaign_M_info = []

            # 循环每个手动数据
            for i in Campaign_Name_M:

                # 获取手动的sku
                SellSKU = df.loc[(df['Station'] == station) & (df['Campaign Name_M'] == i)]
                add_sellsku_step1 = SellSKU.drop(columns="Station")
                add_sellsku_step1["Ad Group"] = "Group"

                add_sellsku_step2 = pd.concat([pd.DataFrame({"Campaign Name_M":[], "SellSKU":[],"Ad Group":[]}),
                                               add_sellsku_step1.replace("Group","ASIN"),
                                               add_sellsku_step1.replace("Group","ASIN_Pending"),
                                               add_sellsku_step1.replace("Group","Broad"),
                                               add_sellsku_step1.replace("Group","Broad_Pending"),
                                               add_sellsku_step1.replace("Group","Phrase"),
                                               add_sellsku_step1.replace("Group","Exact"),], axis=0, sort=False)
                add_sellsku_step2["Status"] = "Enabled"

                # 增加剩余3列
                for b in ["Campaign ID", "Campaign_Daily_Budget", "Campaign_Start_Date", "Campaign End Date",
                     "Campaign_Targeting_Type", "Bid", "Customer_Search_Terms",
                     "Product_Targeting_ID", "Match Type", "Campaign Status", "Ad Group Status","Bidding strategy"]:
                    add_sellsku_step2[b] = ""

                add_sellsku_step3 = add_sellsku_step2[
                    ["Campaign ID", "Campaign Name_M", "Campaign_Daily_Budget", "Campaign_Start_Date", "Campaign End Date",
                     "Campaign_Targeting_Type", "Ad Group", "Bid", "SellSKU", "Customer_Search_Terms",
                     "Product_Targeting_ID", "Match Type", "Campaign Status", "Ad Group Status", "Status",
                     "Bidding strategy"]]

                # 每个手动数据传入列表储存
                Campaign_M_info.append(add_sellsku_step3)

            station_values()

    except Exception as e:
        print("读取失败", e)

#根据站点获取信息填写方式
def station_values():
    global sheet_head, campaign_status

    try:
        station_type = station[-2:]
        if station_type in ["CA", "MX","JP"]:
            station_type = "US"
        if station_type in ["DE", "FR", "IT", "ES"]:
            station_type = "UK"

        station_info = {'US': {'Manual': 'Manual', 'Status': 'Enabled',
                               'title_name': ['Campaign ID', 'Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type',
                                              'Campaign Status', 'Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Manual': 'Manual', 'Status': 'Enabled',
                               'title_name': ['Campaign ID', 'Campaign Name', 'Campaign Daily Budget',
                                              'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', "Product Targeting ID",
                                              'Match Type', 'Campaign Status', 'Ad Group Status', 'Status', 'Bid+']}}
        sheet_head = station_info[station_type]['title_name']
        campaign_status = station_info[station_type]['Status']


        write_excel()

    except Exception as e:
        print("获取失败", e)

#写Excel
def write_excel():
    try:
        pd_save = pd.DataFrame([sheet_head, ], columns=sheet_head)

        for i in Campaign_M_info:
            i.columns = sheet_head
            i.replace({"Enabled": campaign_status}, inplace=True)
            pd_save = pd.concat([pd_save, i])

        to_path = r"D:\data\addSKU\{0} 手动广告补渠道sku.xlsx".format(station)

        pd_save.to_excel(excel_writer=to_path, header=None, index=None)

    except Exception as e:
        print("写入失败", e)


if __name__ == '__main__':
    main()