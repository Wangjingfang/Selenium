import xlwt, time, xlrd
import pandas as pd
import os




def file_name(path):
    try:
        L = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.xls':
                    L.append(os.path.join(root, file))
        return L

    except Exception as e:
        print("获取各文件路径失败", e)


def concat_excel(path, final_path):
    try:
        L = file_name(path)
        total_file = pd.DataFrame()
        for l in L:
            df = pd.read_excel(l)
            print(l, df.shape)
            total_file = pd.concat([total_file, df], axis=0)

        print(total_file.shape)
        # 写入Excel
        total_file.to_excel(excel_writer=final_path, index=None)

    except Exception as e:
        print("合并失败", e)

    else:
        print("文件已创建")
        return total_file

#读批量广告中sku
def read_excel(excel):
    global station
    try:

        # excel = pd.read_excel(excel, sheet_name = 0)

        station_set = set(map(lambda x: x[-6:], excel['渠道来源']))
        print(station_set)
        for station in station_set:
            station_name = ''.join(['Amazon-Z01', station])
            sku = list(excel.loc[excel['渠道来源'] == station_name]['SellSKU'])
            sku_len = len(sku) * 2

            station_values(station, sku, sku_len)

    except Exception as e:
        print("读取失败", e)


#根据站点获取信息填写方式
def station_values(station, sku, sku_len):

    global campaign_budget

    try:
        station_type = station[-2:]
        today_date = time.time()
        timeArray = time.localtime(today_date)

        if station[-2:] == "JP" or station[-2:] == "IN":
            campaign_budget = 1000
        elif station[-2:] == "BR" or station[-2:] =="NL":
            campaign_budget = str(10)
        else:
            campaign_budget = 10

        campaign_name_date = time.strftime("%Y%m%d", timeArray)

        station_info = {'US': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid':0.04, 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'CA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid':0.04, 'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'BR': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid': str(0.15),'Status': 'Enabled',
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'UK': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid':0.04, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bid+']},
                        'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.04, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'DE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'automatisch', 'default_bid':0.03, 'Status': 'aktiviert',
                        #        'title_name': ['Kampagne', 'Tagesbudget Kampagne', 'Startdatum der Kampagne',
                        #                       'Enddatum der Kampagne', 'Ausrichtungstyp der Kampagne', 'Anzeigengruppe',
                        #                       'Maximales Gebot', 'SKU', 'Schlüsselwort- oder Produktausrichtung',
                        #                       'übereinstimmungstyp', 'Kampagnenstatus', 'Anzeigengruppe Status', 'Status',
                        #                       'gebot+']},
                        'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.03,'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.04, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting','Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'FR': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Automatique', 'default_bid':0.04, 'Status': 'Activé',
                        #        'title_name': ['Nom de la Campagne', 'Budget quotidien de la Campagne', 'Date de début de la Campagne',
                        #                       'Date de fin de la Campagne', 'Type de Ciblage de la Campagne',
                        #                       "Nom du groupe d'annonces", 'Enchère Max', 'SKU',
                        #                       'Ciblage de mots-clés ou de produits', 'Type de correspondance',
                        #                       'Statut de la campagne', 'Statut du groupe d’annonces', 'Statut', '']},
                        # 'IT': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Automatico', 'default_bid':0.03, 'Status': 'attivo',
                        #        'title_name': ['Nome della campagna', 'Budget giornaliero campagna',
                        #                       'Data di inizio della campagna', 'Data di fine della campagna',
                        #                       'Tipo di targeting della campagna', 'Nome del gruppo di annunci',
                        #                       'Offerta massima', 'SKU', 'Targeting per parola chiave o prodotto',
                        #                       'Tipo di corrispondenza', 'Stato della campagna', 'Stato del gruppo', 'Stato']},
                        'ES': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.03,'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        'NL': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid': str(0.03),'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        'SE': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 0.2,'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type',
                                              'Campaign Status','Ad Group Status', 'Status', 'Bid+']},
                        # 'ES': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid':0.03, 'Status': 'Enabled',
                        #        'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                        #                       'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                        #                       'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type', 'Campaign Status',
                        #                       'Ad Group Status', 'Status', 'Bid+']},
                        'IN': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'default_bid': 1, 'Status': 'Enabled',
                               'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group Name',
                                              'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Product Targeting ID',
                                              'Match Type', 'Campaign Status', 'Ad Group Status', 'Status', 'Bid+']},
                        # 'IN': {'Date': time.strftime("%d/%m/%Y", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 1,
                        #        'title_name': ['Campaign Name', 'Campaign Daily Budget', 'Campaign Start Date',
                        #                       'Campaign End Date', 'Campaign Targeting Type', 'Product Targeting ID','Ad Group Name',
                        #                       'Max Bid', 'SKU', 'Keyword or Product Targeting', 'Match Type',
                        #                       'Campaign Status',
                        #                       'Ad Group Status', 'Status', 'Bid+']},
                        'AU': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 0.1,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'AE': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled', 'default_bid': 0.25,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'SA': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'default_bid': 0.25,
                               'Status': 'Enabled','title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID','Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'MX': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled','default_bid': 0.35,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        # 'JP': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'オート', 'Status': '有効','入札額':'7',
                        #        'title_name': ['キャンペーン名', '1日の平均予算', '開始日',
                        #                       '終了日', 'ターゲティング', '広告グループ名', '入札額',
                        #                       '広告(SKU)', 'キーワードまたは商品ターゲティング', 'マッチタイプ', 'キャンペーン ステータス',
                        #                       '広告グループ ステータス', 'ステータス', '入札戦略']}
                        'JP': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled', 'default_bid': 7,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']},
                        'SG': {'Date': time.strftime("%Y/%m/%d", timeArray), 'Auto': 'Auto', 'Status': 'Enabled', 'default_bid': 0.03,
                               'title_name': ['Campaign', 'Campaign Daily Budget', 'Campaign Start Date',
                                              'Campaign End Date', 'Campaign Targeting Type', 'Ad Group', 'Max Bid',
                                              'SKU', 'Keyword or Product Targeting', 'Product Targeting ID', 'Match Type', 'Campaign Status',
                                              'Ad Group Status', 'Status', 'Bidding strategy']}

                        }

        campaign_date = station_info[station_type]['Date']
        campaign_auto = station_info[station_type]['Auto']
        campaign_status = station_info[station_type]['Status']
        row0 = station_info[station_type]['title_name']
        default_bid = station_info[station_type]['default_bid']


        write_excel(station, sku, sku_len, campaign_name_date, campaign_date, campaign_auto, campaign_status, row0, campaign_budget, default_bid)

    except Exception as e:
        print("获取失败", e)


#写Excel
def write_excel(station, sku, sku_len, campaign_name_date, campaign_date, campaign_auto, campaign_status, row0, campaign_budget, default_bid):

    try:
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('Template - Sponsored Product', cell_overwrite_ok=True)
        campaign_name = '{0}-20211028-FBM批量'.format(station)
        row1 = [campaign_name, campaign_budget, campaign_date, "", campaign_auto, "",  "",  "",  "",  "",  "", campaign_status]
        excel_name = '{0}.xlsx'.format(campaign_name)

        # 写第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])

        #写第二行
        for i in range(0, len(row1)):
            sheet1.write(1, i, row1[i])

        #写A列
        for i in range(0,sku_len):
            sheet1.write(i+2, 0, campaign_name)

        #写F列 - 1
        for i in range(0,len(sku)):
            sheet1.write(i+2, 5, sku[i])

        #写F列 - 2
        for i in range(0,len(sku)):
            sheet1.write(i+len(sku)+2, 5, sku[i])

        #写G列
        for i in range(0,len(sku)):
            sheet1.write(i+2, 6, default_bid)

        #写H列
        for i in range(0,len(sku)):
            sheet1.write(i+len(sku)+2, 7, sku[i])

        #写M列
        for i in range(0,len(sku)):
            sheet1.write(i+2, 12, campaign_status)

        #写N列
        for i in range(0,len(sku)):
            sheet1.write(i+len(sku)+2, 13, campaign_status)


        f.save(excel_name)

    except Exception as e:
        print("写入失败", e)

def main():

    # 非节日路径
    path = r"D:\data\ERP每周批量\FBM"
    final_path = r"D:\data\ERP每周批量\FBM\FBM.xlsx"
    # 节日路径：
    # path = r"D:\data\ERP每周批量\FBM节日"
    # final_path = r"D:\data\ERP每周批量\FBM节日\FBM.xlsx"

    file_name(path)
    excel = concat_excel(path,final_path)
    # excel = pd.read_excel(r"D:\data\ERP每周批量\FBM\亚马逊listing导出库存2021年9月25日-452223.xls")
    # print(excel.shape)
    # campaign_budget = 10
    # excel = r"D:\data\ERP每周批量\FBM\FBM.xlsx"
    read_excel(excel)

if __name__ == '__main__':
    main()