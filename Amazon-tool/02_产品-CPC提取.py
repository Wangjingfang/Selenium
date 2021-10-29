# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:32:37 2020

@author: Administrator
"""
#问题点：由于从CPC系统产品页面复制的数据中有些是12行，有些是11行，获取产品SKU时未获取到
#这里采用判断一下是否是12行，12行写入某个块block，再从块中提取数据；否则从不提取数据
#update20201023:近期出现读取来源渠道为姓名，在block.loc[1,'来源渠道']修改为1或着2，具体根据情况分析
    
    
    
import datetime
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

def get_data(path):
    
    filename = path.split('\\')[-1].split('.')[0]
    
    data = pd.read_excel(path) #,sheet_name = 'CPC'
    print('数据正在提取中，请稍后')

    block = pd.DataFrame()
    df = pd.DataFrame()
    block_others = []
    i = 0
    x = 0
    for row in range(0,len(data)):
        if data.loc[row,'状态'] == '启用' or data.loc[row,'状态'] == '暂停' or data.loc[row,'状态'] == '归档':
            x = row
        # 此处的作用为判断是否为日期，用if判断的话遇到非日期会报错，只能采用try，except,else的方式
        try:
            datetime.datetime.strftime(data.loc[row,'产品标题'],'%Y-%m-%d')     
        except:
            y = 0
        else:
            y = row
                
        if y > x:
            block = data.ix[x:y,:]
            block.reset_index(inplace = True)
            
            if len(block) == 12:     
                df.loc[i,'来源渠道_1'] = block.loc[1,'来源渠道']
                df.loc[i,'sellerSKU_1'] = block.loc[5,'产品标题']
                df.loc[i,'ASIN_1'] = block.loc[8,'产品标题']
                df.loc[i,'状态_1'] = block.loc[1,'状态']
                df.loc[i,'广告活动_1'] = block.loc[1,'广告活动']
                df.loc[i,'广告组_1'] = block.loc[4,'广告活动']
                df.loc[i,'曝光量_1'] = block.loc[0,'曝光量']
                df.loc[i,'点击量_1'] = block.loc[0,'点击量']
                df.loc[i,'花费_1'] = block.loc[0,'花费']
                df.loc[i,'点击率_1'] = block.loc[0,'点击率']
                df.loc[i,'CPC_1'] = block.loc[0,'CPC']
                df.loc[i,'出单数_1'] = block.loc[0,'出单数']
                df.loc[i,'贡献毛利润_1'] = block.loc[0,'贡献毛利润']
                df.loc[i,'销售额_1'] = block.loc[1,'贡献毛利润']
                df.loc[i,'转化率_1'] = block.loc[0,'转化率']
                df.loc[i,'Acos_1'] = block.loc[0,'ACoS']
            
            elif len(block) == 9:
                df.loc[i,'来源渠道_1'] = block.loc[1,'来源渠道']
                df.loc[i,'sellerSKU_1'] = block.loc[4,'产品标题']
                df.loc[i,'ASIN_1'] = block.loc[8,'产品标题']
                df.loc[i,'状态_1'] = block.loc[1,'状态']
                df.loc[i,'广告活动_1'] = block.loc[1,'广告活动']
                df.loc[i,'广告组_1'] = block.loc[4,'广告活动']
                df.loc[i,'曝光量_1'] = block.loc[0,'曝光量']
                df.loc[i,'点击量_1'] = block.loc[0,'点击量']
                df.loc[i,'花费_1'] = block.loc[0,'花费']
                df.loc[i,'点击率_1'] = block.loc[0,'点击率']
                df.loc[i,'CPC_1'] = block.loc[0,'CPC']
                df.loc[i,'出单数_1'] = block.loc[0,'出单数']
                df.loc[i,'贡献毛利润_1'] = block.loc[0,'贡献毛利润']
                df.loc[i,'销售额_1'] = block.loc[1,'贡献毛利润']
                df.loc[i,'转化率_1'] = block.loc[0,'转化率']
                df.loc[i,'Acos_1'] = block.loc[0,'ACoS']
                
            elif len(block) == 10:
                df.loc[i,'来源渠道_1'] = block.loc[1,'来源渠道']
                df.loc[i,'sellerSKU_1'] = block.loc[4,'产品标题']
                df.loc[i,'ASIN_1'] = block.loc[8,'产品标题']
                df.loc[i,'状态_1'] = block.loc[1,'状态']
                df.loc[i,'广告活动_1'] = block.loc[1,'广告活动']
                df.loc[i,'广告组_1'] = block.loc[4,'广告活动']
                df.loc[i,'曝光量_1'] = block.loc[0,'曝光量']
                df.loc[i,'点击量_1'] = block.loc[0,'点击量']
                df.loc[i,'花费_1'] = block.loc[0,'花费']
                df.loc[i,'点击率_1'] = block.loc[0,'点击率']
                df.loc[i,'CPC_1'] = block.loc[0,'CPC']
                df.loc[i,'出单数_1'] = block.loc[0,'出单数']
                df.loc[i,'贡献毛利润_1'] = block.loc[0,'贡献毛利润']
                df.loc[i,'销售额_1'] = block.loc[1,'贡献毛利润']
                df.loc[i,'转化率_1'] = block.loc[0,'转化率']
                df.loc[i,'Acos_1'] = block.loc[0,'ACoS']

            elif len(block) == 11:
                df.loc[i,'来源渠道_1'] = block.loc[1,'来源渠道']
                df.loc[i,'sellerSKU_1'] = block.loc[4,'产品标题']
                df.loc[i,'ASIN_1'] = block.loc[7,'产品标题']
                df.loc[i,'状态_1'] = block.loc[1,'状态']
                df.loc[i,'广告活动_1'] = block.loc[1,'广告活动']
                df.loc[i,'广告组_1'] = block.loc[4,'广告活动']
                df.loc[i,'曝光量_1'] = block.loc[0,'曝光量']
                df.loc[i,'点击量_1'] = block.loc[0,'点击量']
                df.loc[i,'花费_1'] = block.loc[0,'花费']
                df.loc[i,'点击率_1'] = block.loc[0,'点击率']
                df.loc[i,'CPC_1'] = block.loc[0,'CPC']
                df.loc[i,'出单数_1'] = block.loc[0,'出单数']
                df.loc[i,'贡献毛利润_1'] = block.loc[0,'贡献毛利润']
                df.loc[i,'销售额_1'] = block.loc[1,'贡献毛利润']
                df.loc[i,'转化率_1'] = block.loc[0,'转化率']
                df.loc[i,'Acos_1'] = block.loc[0,'ACoS']
    
            else:
                print('有其他行列数据，请检查，对应行为(%d,%d)'%(x,y))
                print('请仔细检查，并修改源代码')
                continue
          
            i += 1
    
    df.columns = ['来源渠道','sellerSKU','ASIN','状态','广告活动','广告组','曝光量','点击量','花费','点击率','CPC','出单数','贡献毛利润','销售额_1','转化率','Acos']     
    
    origin_158_data = pd.read_excel(path)       # ,sheet_name = 'sheet1'
    writer = pd.ExcelWriter(path)
    origin_158_data.to_excel(writer,'原始CPC产品页面数据',index = False)
    data.to_excel(writer,'CPC复制数据',index = False)
    df.to_excel(writer,'已提取数据',index = False)
    writer.save()

print('请输入CPC中产品页面要提取的文件:')
file_path = input('excel文件:')
#去除输入路径时带入的双引号
if '"' in file_path:
    file_path = file_path.replace('"','')


f_path = os.path.dirname(file_path)
os.chdir(f_path)

get_data(file_path)

print('数据提取成功，路径为:%s'%f_path)

