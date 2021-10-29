# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:38:58 2019
#此处删除一行  ‘不导入FBA原因’
"""

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import jieba.analyse
import jieba
import warnings
warnings.filterwarnings('ignore')

connect = create_engine('mysql+pymysql://root:123456@localhost:3306/ad_mysql?charset=utf8')  #注意此处不能写成utf-8

#数据导入部分
print('请输入要导入的fba报告的路径：')
path = input('excel路径：')
if '"' in path:
    path = path.replace('"','')
    
fba_listing = pd.read_excel(path)

fba_listing.columns = ['station','stocking_warehouse','asin','sku','custom_sku','fnsku','sellsku','online_status', \
                       'active_state','product_category','type_of_sales','sales_team_level','sales_team_leve2', \
                       'sales_team_leve3','salesperson','shelves','added_time','product_chinese_name', \
                       'default_shipping_method','stocking_days','transportation_time','safe_days','purchase_days', \
                       'purchase_prices','purchasing','purchase_amount','delivering','shipping_amount', \
                       'available_inventory','inventory_amount','estimated_sales','sales_today','yesterday_sales', \
                       'sales_the_day_before_yesterday','previous_sales','weekly_sales','two_week_sales', \
                       'days_30_sales','days_90_sales','todays_ranking','ranking_yesterday','ranking_the_day_before_yesterday', \
                       'top_ranking','review_score','number_of_reviews','storage_age','occupy_funds','original_price', \
                       'price_after_discount','average_monthly_profit_rate','current_inventory','local_warehouse_inventory', \
                       'alert_inventory','shopping_cart_lock','transfer_warehouse_lock','lock_in_warehouse','available_days', \
                       'available_quantity','estimated_sold_out_date','product_status','product_logistics_attributes', \
                       'whether_efn_product','label','whether_to_switch_to_fba','reasons_for_not_transferring_to_fba','holiday_logo']

fba_listing['date'] = "2020-09-01"
fba_listing['date'] = pd.to_datetime(fba_listing['date'])
fba_listing['short_station'] = fba_listing['station'].apply(lambda x: x[-6:])
fba_listing['short_station_sku'] = fba_listing['short_station'] + '_' + fba_listing['sellsku']

for i in range(0,len(fba_listing)):
    ad_tag = jieba.analyse.extract_tags(fba_listing.loc[i,'product_chinese_name'],topK = 3,allowPOS=('n','nr','ns')) 
    fba_listing.loc[i,'ad_tag'] = ''.join(ad_tag)

print('表头处理完成，等待导入数据库中')
fba_listing.drop('reasons_for_not_transferring_to_fba',axis = 1,inplace = True)

db_table = 'fba_listing'   #请输入想导入的数据库的表名称，若没有的话，数据库会新建

try:
    print('正在写入mysql中，请稍后：')
    fba_listing.to_sql(db_table,connect,index = False,if_exists = 'append')
    print('业绩报告导入mysql成功，请在数据库中检查；')
except Exception as e:
    print('导入出错，出错原因为',e)
