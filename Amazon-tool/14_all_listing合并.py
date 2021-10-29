# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
1.请以站点命名，如   341-de.txt ;all_listing报告在中英文界面下载均可；
2.将要合并的文件放在同一个文件夹下
3.合并和请采用脚本 “1VN批量广告”  渠道来源与SKU中间隔5行，这为了与158listing下载下来的位置（渠道来源，SellSKU）保持一致；
4.JP的sellerSKU在第三方，且名称为“出品者SKU”，已做出判断；

提醒：
若出现“'utf-8' codec can't decode byte 0xa1 in position 69: invalid start byte”错误，则可能是该txt文档不是以utf-8编码的，可以在notepad里面修改编码方式；
'''

import os
import pandas as pd
print('请输入要合并的all_listing文件夹路径（将文件放入文件夹内）')
path = input('文件夹：')
if '"' in path:
    path = path.replace('"','')
    
    
filenames = []
for root,dirs,files in os.walk(path):
    for file in files:
        filenames.append(os.path.join(root,file))

alllisting_df = pd.DataFrame()

for filename in filenames:
    origin_df = pd.read_table(filename)
    short_station = filename.split('\\')[-1].split('.')[0].upper()
    long_station = 'Amazon-Z01' + short_station
    if short_station[-2:].upper() == "JP":
        new_df = pd.DataFrame({'渠道来源':long_station,
                           'SellSKU':origin_df['出品者SKU']})
       
    elif 'seller-sku' in origin_df.columns:
        new_df = pd.DataFrame({'渠道来源':long_station,
                          'SellSKU':origin_df['seller-sku']})
    
    elif '卖家 SKU' in origin_df.columns:
        new_df = pd.DataFrame({'渠道来源':long_station,
                          'SellSKU':origin_df['卖家 SKU']})

    elif 'sku' in origin_df.columns:
        new_df = pd.DataFrame({'渠道来源':long_station,
                          'SellSKU':origin_df['sku']})        
    
        
    alllisting_df = pd.concat([alllisting_df,new_df])

alllisting_df = pd.concat([alllisting_df,pd.DataFrame(columns = list('ABCDE'))])   #增加空列
alllisting_df = alllisting_df.reindex(['渠道来源','A','B','C','D','E','SellSKU'],axis = 1)   #按一定顺序对列进行排序
final_name = path + 'all_listing合并.xlsx'
alllisting_df.to_excel(final_name,index = False)


