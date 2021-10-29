# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:54:17 2019

@author: Administrator
"""
'''
检查的逻辑为：
1.关键词报告的文件名是否存在在广告活动中，一般批量广告活动一定会存在文件名，如075-us
2.关键词报告中的货币，是否与国家对应的货币一致
3.判断是否有广告，判断长度
4.判断下载是否是英文报告（区分中文和英文），区分daily和total报告的区别，此处容易下错  根据表头是否一致来判断
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
    
def file_judge(path):
    
    result_df = pd.DataFrame()
    
    filenames = get_file_list(path)
    
    x = -1
    
    try:
    
        for filename in filenames:
            
            x = x + 1
            
            print('第%d文件检查中，请稍后；'%(x + 1))
        
            df = pd.read_excel(filename)
            
            file_station = filename.split('\\')[-1][0:6]
            file_country = filename.split('\\')[-1][4:6].lower()
            
            length = len(df)
                    
            result_df.loc[x,'站点'] = file_station
            result_df.loc[x,'数据量'] = length
            
            print('当前检查站点为：%s'%file_station)
            
            if df.columns[0] != 'Date':
                error_list2 = '文件表头不一致，请确认是否是在英文界面下下载的报告或着下载的是否为daily报告'
                print(error_list2)
                result_df.loc[x,'错误原因'] = error_list2
                continue
            
            else:
                print('文件表头一致')
            
                if length == 0:
                    result_df.loc[x,'错误原因'] = '文件内无数据，可以忽略！'
                    print('文件内无数据，可以忽略！')
                    
                else:
                    result_df.loc[x,'最小日期'] = min(df['Date'])
                    result_df.loc[x,'最大日期'] = max(df['Date'])
        
                    #判断货币是否正确
                    if currency_dict[file_country] != df.loc[0,'Currency']:
                        error_list = '文件国家名称与广告活动内货币对应不上，可能原因为下载报告时文件名称命名错误，请检查'
                        print(error_list)
                        result_df.loc[x,'错误原因'] = error_list
                        continue
                                
                    else:
                        #continue
                        print('货币对应国家没错，继续检查对应站点')
                    
                    #判断文件名是否在广告活动中
                        n = 0
                        for i in range(0,length):
                            pattern = '.*?' + file_station + '.*?'
                            if re.search(pattern,df.loc[i,'Campaign Name'],re.I):
                                print('站点位于广告活动中')
                                n += 1
                                break
                            else:
                                continue
                                
                        if n==0:
                            error_tag = '站点不在广告活动中，请检查此报告是否有问题'
                            print(error_tag)
                            result_df.loc[x,'错误原因'] = error_tag
                        else:
                            print('站点位于广告活动中')
                            result_df.loc[x,'错误原因'] = '无错误'
                    
            print('\n')
    
    except  Exception as e:
        error_reason = '文件名称不符合规范或出现其他错误（文件内无数据）'
        result_df.loc[x,'错误原因'] = error_reason
                             
    return result_df
              
print('请输入要检查的搜索词报告的文件夹名称')
origin_path = input('文件夹名称：')

if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path) 


currency_dict = {'us':'USD',
                'ca':'CAD',
                'mx':'MXN',
                'uk':'GBP',
                'de':'EUR',
                'fr':'EUR',
                'it':'EUR',
                'es':'EUR',
                'jp':'JPY',
                'in':'INR',
                'au':'AUD',
                'ae':'AED',
                'sa':'SAR'}
   
result_df = merge = file_judge(origin_path)    
os.chdir(r'E:\01工作资料') 
result_df.to_excel(r'C:\Users\Administrator\Desktop\检查结果文件.xlsx',index = False)
  
print('文件检查完成，请在桌面上查看《检查结果文件》;')
        
