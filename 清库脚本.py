#  UTF-8
import xlwt, time, xlrd
import pandas as pd

# df = pd.read_excel(r"C:\Users\Administrator\Desktop\练习.xlsx",sheet_name=0)
# station_set = set(map(lambda x:x[-6:], df["渠道来源"]))
# campagin_list = list(df["产品中文名称"])
# asin_list = list(df["ASIN"])
# print(station_set)
#
# print(campagin_list)
# print(asin_list)
# print(len(asin_list))
#
# campagin_name=[]
# for i in station_set:
#     campagin_name.append(asin_list[i] + " "+ campagin_list[i])
#
#
# print(campagin_name)

# 1V1VN 清库脚本
def main():
    path = r"D:\data\清库的\清库.xlsx"
    # campaign_budget = 10
    read_excel(path)


#读批量广告中sku

# Station	Seller Sku	广告活动
# path = r"C:\Users\Administrator\Desktop\练习.xlsx"
# df = pd.read_excel(path, sheet_name = 0)
# sku1 = df.loc[df['渠道来源']=="Amazon-Z01370-UK"]['SellSKU']
# # 0    X17FZCER0322A066Z4KUK7
# # 6                       123
# # 7                       345
# print(sku1)


def read_excel(path):
    global station
    try:

        df = pd.read_excel(path, sheet_name = 0)
        station_set = set(map(lambda x: x[-6:], df['渠道来源']))
        for station in station_set:
            # join 连接字符串
            station_name = ''.join(['Amazon-Z01', station])
            print(station_name)
            sku = list(df.loc[df['渠道来源'] == station_name]['SellSKU'])
            # print(sku)

            sku_len = len(sku)

            station_values(station, sku, sku_len)

    except Exception as e:
        print("读取失败", e)

#
# #根据站点获取信息填写方式
def station_values(station, sku, sku_len):

    global campaign_budget

    try:
        station_type = station[-2:]
        today_date = time.time()
        timeArray = time.localtime(today_date)

        if station[-2:] == "JP" or station[-2:] == "IN":
            campaign_budget = 1000.37
        else:
            campaign_budget = 10.37

        campaign_name_date = time.strftime("%Y%m%d", timeArray)

        station_info = {'US': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid':0.1, 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'CA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid':0.1, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid':0.08, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.08,'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'automatisch', 'default_bid':0.08, 'Status': 'aktiviert',
                        #        'title_name': ['Kampagne', 'Tagesbudget Kampagne', 'Startdatum der Kampagne',
                        #                       'Enddatum der Kampagne', 'Ausrichtungstyp der Kampagne', 'Anzeigengruppe',
                        #                       'Maximales Gebot', 'SKU', 'Schlüsselwort- oder Produktausrichtung',
                        #                       'übereinstimmungstyp', 'Kampagnenstatus', 'Anzeigengruppe Status', 'Status',
                        #                       'gebot+']},
                        'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.06, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Automatique', 'default_bid':0.04, 'Status': 'Activé',
                        #        'title_name': ['Nom de la Campagne', 'Budget quotidien de la Campagne', 'Date de début de la Campagne',
                        #                       'Date de fin de la Campagne', 'Type de Ciblage de la Campagne',
                        #                       "Nom du groupe d'annonces", 'Enchère Max', 'SKU',
                        #                       'Ciblage de mots-clés ou de produits', 'Type de correspondance',
                        #                       'Statut de la campagne', 'Statut du groupe d’annonces', 'Statut', '']},
                        # 'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Automatico', 'default_bid':0.06, 'Status': 'attivo',
                        #        'title_name': ['Nome della campagna', 'Budget giornaliero campagna',
                        #                       'Data di inizio della campagna', 'Data di fine della campagna',
                        #                       'Tipo di targeting della campagna', 'Nome del gruppo di annunci',
                        #                       'Offerta massima', 'SKU', 'Targeting per parola chiave o prodotto',
                        #                       'Tipo di corrispondenza', 'Stato della campagna', 'Stato del gruppo', 'Stato']},
                        'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.08,'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        'ES': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid':0.06, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'IN': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 4,
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type','Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'AU': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 0.1,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'AE': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled', 'default_bid': 0.5,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'SA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid': 0.08,
                               'Status': 'Enabled','title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        # 'BR': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid': 0.07, 'Status': 'Enabled',
                        #        'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                        #                       'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                        #                       'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                        #                       'Ad Group Status', 'Status', 'Bidding strategy']},
                        'MX': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 0.5,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        # 'JP': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'オート', 'Status': '有効','入札額':'7',
                        #        'title_name': ['キャンペーン名', '1日の平均予算', '開始日',
                        #                       '終了日', 'ターゲティング', '広告グループ名', '入札額',
                        #                       '広告(SKU)', 'キーワードまたは商品ターゲティング', 'マッチタイプ', 'キャンペーン ステータス',
                        #                       '広告グループ ステータス', 'ステータス', '入札戦略']}
                        'JP': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled', 'default_bid': 10,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']}
                        }

        campaign_date = station_info[station_type]['Date']
        campaign_auto = station_info[station_type]['Auto']
        campaign_status = station_info[station_type]['Status']
        row0 = station_info[station_type]['title_name']
        default_bid = station_info[station_type]['default_bid']
        # campaign_group = station_info[station_type]['Ad Group']


        write_excel(station, sku, sku_len, campaign_name_date, campaign_date, campaign_auto, campaign_status, row0, campaign_budget, default_bid)

    except Exception as e:
        print("获取失败", e)


#写Excel
def write_excel(station, sku, sku_len, campaign_name_date, campaign_date, campaign_auto, campaign_status, row0, campaign_budget, default_bid):

    try:
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('Template - Sponsored Product', cell_overwrite_ok=True)
        campaign_name = '{0}-清库'.format(station)
        campaign_group = "20201224"
        row1 = [campaign_name, campaign_budget, campaign_date, "", campaign_auto, "",  "",  "",  "",  "", campaign_status]
        row2 = [campaign_name, "", "", "", "", campaign_group, default_bid, "", "","", "",campaign_status]
        excel_name = '{0}.xlsx'.format(campaign_name)

        # 写第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])

        #写第二行
        for i in range(0, len(row1)):
            # print(row1[i])
            sheet1.write(1, i, row1[i])


        #写第三行
        for i in range(0, len(row2)):
            sheet1.write(2, i, row2[i])

        #写A列
        for i in range(0,sku_len):
            sheet1.write(i+3, 0, campaign_name)
        # 写F列
        # for i in range(0,sku_len):
        #     sheet1.write(i+3,5,campaign_group)

        #写F列
        for i in range(0,sku_len):
            sheet1.write(i+3, 5, campaign_group)

        #写F列 - 2  i +len(sku)+2 : i行+长度+前两行
        # for i in range(0,len(sku)):
        #     sheet1.write(i+len(sku)+2, 5, sku[i])

        # #写G列
        # for i in range(0,len(sku)):
        #     sheet1.write(i+2, 6, default_bid)

        #写H列
        for i in range(0,len(sku)):
            sheet1.write(i+3, 7, sku[i])

        # #写L列
        # for i in range(0,len(sku)):
        #     sheet1.write(i+2, 11, campaign_status)

        #写M列
        for i in range(0,len(sku)):
            sheet1.write(i+3, 12, campaign_status)


        f.save(excel_name)

    except Exception as e:
        print("写入失败", e)




if __name__ == '__main__':
    main()