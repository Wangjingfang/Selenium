# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:54:17 2019

@author: Administrator
"""
'''
由于会下载400个excel左右，此脚本是检查搜索词报告是否下错

检查的逻辑为：
1.搜索词报告的文件名是否存在在广告活动中，一般批量广告活动一定会存在文件名，如075-us
2.搜索词报告中的货币，是否与国家对应的货币一致
3.判断是否有广告（有数据），判断长度
4.判断下载是否是英文报告（区分中文和英文），区分daily和total报告的区别， 根据表头是否一致来判断

update20210121:采用for else语法对  站点是否存在广告活动中的判断;可以减少代码数量

请在检查结果文件中查看以下事项，否则容易出现导入出错：
1.文件数据长度为0时，excel大小为4KB,可以直接将原excel删除掉
2.文件的最小日期，一定要为  本周的上一个周日的日期-30天，   若最小日期小于这个日期，一定是下载过程中出错，请查明原因
'''
import os
import re
import pandas as pd

def get_file_list(path):
    try:
        filenames = []
        for root,dirs,files in os.walk(path):
                for file in files:
                    filenames.append(os.path.join(root,file))
        print('获取文件成功,待进行检查中；')
        return filenames
        
    except Exception as e:
        print('获取文件失败',e)
    
def file_judge(filenames):
    
    result_df = pd.DataFrame()
        
    x = -1
    
    try:
    
        for filename in filenames:
            
            x = x + 1
                   
            df = pd.read_excel(filename)
            
            file_station = filename.split('\\')[-1][0:6]
            file_country = filename.split('\\')[-1][4:6].lower()
            
            length = len(df)
                    
            result_df.loc[x,'站点'] = file_station
            result_df.loc[x,'数据量'] = length
            
            print('当前检查站点为：%s'%file_station)
            
            if df.columns[0] != 'Date':
                error_list2 = '文件表头不一致，请确认是否是在英文界面下下载的报告或着下载的是否为daily报告'
                #print(error_list2)
                result_df.loc[x,'错误原因'] = error_list2
                continue
            
            else:
                #print('文件表头一致')
            
                if length == 0:
                    result_df.loc[x,'错误原因'] = '文件内无数据，可以忽略！'
                    #print('文件内无数据，可以忽略！')
                    
                else:
                    result_df.loc[x,'最小日期'] = min(df['Date'])
                    result_df.loc[x,'最大日期'] = max(df['Date'])
        
                    #判断货币是否正确
                    if currency_dict[file_country] != df.loc[0,'Currency']:
                        error_list = '文件国家名称与广告活动内货币对应不上，可能原因为下载报告时文件名称命名错误，请检查'
                        #print(error_list)
                        result_df.loc[x,'错误原因'] = error_list
                        continue
                                
                    else:                       
                        #20210121 采用for else语法对  站点是否存在广告活动中的判断;可以减少代码数量
                        for i in range(0,length):
                            pattern = '.*?' + file_station + '.*?'
                            if re.search(pattern,df.loc[i,'Campaign Name'],re.I):
                                result_df.loc[x,'错误原因'] = '无错误'
                                break
                        else:
                            result_df.loc[x,'错误原因'] = '站点不在广告活动中，请检查此报告是否有问题'
                    
            #print('\n')
    
    except  Exception:
        error_reason = '文件名称不符合规范或出现其他错误（文件内无数据）'
        result_df.loc[x,'错误原因'] = error_reason
                             
    return result_df
              
print('请输入要检查的搜索词报告的文件夹名称')
origin_path = input('文件夹名称：')
origin_path = origin_path.replace('"','')

os.chdir(origin_path) 


currency_dict = {'us':'USD',
                'ca':'CAD',
                'mx':'MXN',
                'br':'BRL',
                'uk':'GBP',
                'de':'EUR',
                'fr':'EUR',
                'it':'EUR',
                'es':'EUR',
                'nl':'EUR',
                'jp':'JPY',
                'in':'INR',
                'au':'AUD',
                'ae':'AED',
                'sa':'SAR',
                'sg':'SGD'}

file_list = get_file_list(origin_path)
result_df = file_judge(file_list)    
os.chdir(r'D:\01工作资料') 
result_df.to_excel(r'C:\Users\Administrator\Desktop\检查结果文件.xlsx',index = False)
  
print('文件检查完成，请在桌面上查看《检查结果文件》;')
        
