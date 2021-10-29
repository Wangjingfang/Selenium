

import time
import random
import string
import pandas as pd

## 单个开的自动广告脚本
#写Excel
def write_excel():
    try:
        pd_save = pd.DataFrame([sheet_head,], columns=sheet_head)

        for i in sku_info:

            campaign_name = '{0} {1}'.format(i[1], i[2])

            row1 = [campaign_name, campaign_budget, campaign_date, "", campaign_auto, "", "", "", "", "","", campaign_status,'','','']
            row2 = [campaign_name,'','','','',i[0],default_bid,'','','','','', campaign_status,'','']
            row3 = [campaign_name,'','','','',i[0],'',i[0],'','','','','', campaign_status,'']

            pd1 = pd.DataFrame([row1, row2, row3], columns = sheet_head)

            pd_save = pd.concat([pd_save, pd1])
        to_path = r"D:\data\Submitlisting\{0} 提报广告FBA.xlsx".format(station)
        # to_path = r"D:\data\festival\圣诞节日提报\20191017\{0} 提报广告.xls".format(station)
        # to_path = r"D:\data\周四批量\festival\圣诞节日提报\20191128\{0} 提报广告.xls".format(station)
        # D:\Ad\F\079-US   D:\data\Submitlisting
        pd_save.to_excel(excel_writer = to_path, header = None, index = None)

    except Exception as e:
        print("写入失败", e)


#根据站点获取信息填写方式
def station_values():

    global campaign_date, campaign_auto, campaign_status, sheet_head, campaign_budget, default_bid

    try:
        # country
        station_type = station[-2:]

        if station[-2:] == "JP" :
            campaign_budget = 300
            default_bid = 14
        elif station[-2:] == "US" or station[-2:] == "CA" or station[-2:] == "AU" or station[-2:] == "SG":
            campaign_budget = 5
            default_bid = 0.18
        elif station[-2:] == "BR":
            campaign_budget = str(5)
            default_bid = str(0.2)
        elif station[-2:] == "MX" or station[-2:] == "IN" or station[-2:] == "AE" or station[-2:] == "SA":
            campaign_budget = 50
            default_bid = 2
        elif station[-2:]== "UK" or station[-2:] == "DE":
            campaign_budget = 5
            default_bid = 0.16
        elif station[-2:]=="NL":
            campaign_budget = str(5)
            default_bid = str(0.12)
        elif station[-2:] == "FR":
            campaign_budget = 5
            default_bid = 0.13
        else:
            campaign_budget = 3
            default_bid = 0.10

        # default_bid = lambda x: 0.18 if x == 'US' or x == "CA" else (2 if x == 'MX' else (str(0.2) if x == "BR" else (0.2 if x == "AU" else (
        #     0.16 if x == 'UK' or x == 'DE' else (0.12 if x == 'ES' else (0.14 if x == "IT" or x == "FR" else (str(0.14) if x == "NL" else (12 if x == 'JP' else (3 if x == 'IN' else 0.3)))))))))

        timeArray = time.localtime(time.time())

        station_info = {'US': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'CA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'automatisch', 'Status': 'aktiviert',
                        #        'title_name': ['Kampagne', 'Tagesbudget Kampagne', 'Startdatum der Kampagne',
                        #                       'Enddatum der Kampagne', 'Ausrichtungstyp der Kampagne', 'Anzeigengruppe',
                        #                       'Maximales Gebot', 'SKU',
                        #                       'Schlüsselwort- oder Produktausrichtung', 'übereinstimmungstyp', 'Kampagnenstatus',
                        #                       'Anzeigengruppe Status', 'Status', 'gebot+']},
                        'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                        #        'title_name': ['Nom de la Campagne', 'Budget quotidien de la Campagne', 'Date de début de la Campagne',
                        #                       'Date de fin de la Campagne', 'Type de Ciblage de la Campagne',
                        #                       "Nom du groupe d'annonces", 'Enchère Max', 'SKU',
                        #                       'Ciblage de mots-clés ou de produits', 'Type de correspondance',
                        #                       'Statut de la campagne', 'Statut du groupe d’annonces', 'Statut', '']},
                        'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Automatico', 'Status': 'attivo',
                        #        'title_name': ['Nome della campagna', 'Budget giornaliero campagna',
                        #                       'Data di inizio della campagna', 'Data di fine della campagna',
                        #                       'Tipo di targeting della campagna', 'Nome del gruppo di annunci',
                        #                       'Offerta massima', 'SKU', 'Targeting per parola chiave o prodotto',
                        #                       'Tipo di corrispondenza', 'Stato della campagna', 'Stato del gruppo', 'Stato',""]},
                        'ES': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        'NL': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'ES': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                        #        'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                        #                       'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                        #                       'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                        #                       'Ad Group Status', 'Status', 'Bid+']},
                        'IN': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'AU': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'AE': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'SA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'BR': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'JP': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'MX': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'SG': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']}
                        }

        campaign_date = station_info[station_type]['Date']
        campaign_auto = station_info[station_type]['Auto']
        campaign_status = station_info[station_type]['Status']
        sheet_head = station_info[station_type]['title_name']


        write_excel()

    except Exception as e:
        print("获取失败，可能渠道SKU有重复值", e)

'''
# 对广告描述栏进行分词和合并，并进行后缀(suffix)公式合并标识 ,已完善
# def split_ad_tag(name, suffix):
#     ad_tag = jieba.analyse.extract_tags(name, topK=3, allowPOS=('n', 'nr', 'ns'))
#     df['ad_tag'] = ''.join(ad_tag)
#
#     # 将df中的空值复制为缺失值
#     if df['ad_tag'] == '':
#         df['ad_tag'] = np.nan
#
#     # for i in range(0, len(df)):
#     #     ad_tag = jieba.analyse.extract_tags(df.loc[i, '产品中文名称'], topK=3, allowPOS=('n', 'nr', 'ns'))
#     #     df.loc[i, 'ad_tag'] = ''.join(ad_tag)
#     #
#     # # 将df中的空值复制为缺失值
#     # for i in range(0, len(df)):
#     #     if df.loc[i, 'ad_tag'] == '':
#     #         df.loc[i, 'ad_tag'] = np.nan
#
#             # 将缺失值填充前一个值
#     df[['产品中文名称', 'ad_tag']] = df[['产品中文名称', 'ad_tag']].fillna(method='ffill', axis=1)  # 此处不可用inplace = true
#
#     # 去除ad_tag中字符串×，在亚马逊后台系统并不识别,
#     df['ad_tag'] = df['ad_tag'].apply(lambda x: x.replace('×', ''))
#     # 去除空格
#     df['ad_tag'] = df['ad_tag'].apply(lambda x: x.replace(' ', ''))
#
#     # df['广告活动'] = df['ASIN'] + ' ' + df['ad_tag'] + '-' + suffix
#     df = df.drop('产品中文名称', axis=1)
#     # df = df.drop('ad_tag', axis=1)
#     print('广告tag分词已完成，可以直接进行下一步的分解')
#     return df
'''


#读批量广告中sku
def read_excel():

    global sku_info, station

    try:
        df = pd.read_excel(path, sheet_name = 0)
        station_set = set(map(lambda x: x[-6:], df['渠道来源']))
        # {'128-ES', '175-DE', '178-CA'}
        for station in station_set:

            station_name = ''.join(['Amazon-Z01', station])
            sku_set = list(df.loc[df['渠道来源'] == station_name]['SellSKU'])
            # print(list(sku_set))
            sku_info = []
            # suffix = 'FBA'

            for s in sku_set:
                asin = list(df.loc[df['SellSKU'] == s]['ASIN'])[0]
                # default_bid = float(df.loc[(df['SellSKU'] == s) & (df['渠道来源'] == station_name)]['建议出价'])
                #print(type(df.loc[df['SellSKU'] == s]['建议出价']))

                name = list(df.loc[df['SellSKU'] == s]['产品中文名称'])[0]

                # 化简产品中文名称
                # newname = jieba.analyse.extract_tags(name, topK=4, allowPOS=('n', 'nr', 'ns'))
                # newname = ''.join(newname)
                #
                # if newname == '':
                #     newname = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                #
                # newname = newname.replace('*','')
                # newname = newname.replace(' ','')
                # newname = newname + "-FBA"

                sku_info.append([s,asin,name])
                # sku_info.append([s, asin, default_bid, name])

            station_values()

    except Exception as e:
        print("读取失败", e)


def main():

    global path
    # D:\data\Submit
    path = r"D:\data\Submit\提报开广告.xlsx"
    #path = r"D:\data\周四批量\festival\提报开广告.xlsx"
    # D:\Ad\F\079-US    D:\data\Submit  D:\data\festival\提报开广告.xlsx
    # campaign_budget = 8

    read_excel()


if __name__ == '__main__':
    main()