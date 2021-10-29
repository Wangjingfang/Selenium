# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:32:54 2019

@author: Administrator
"""
'''
#经验总结：后续由于需要维护，可以采用断点调试，直接执行每步函数的运行过程，修改函数内部的源代码
'''
# update
# 20200929:CPC的广告活动页面调整，出现在“花费”栏，float无法split的错误，循环中由4行改为5行即可解决；
# 20201023:CPC的广告活动页面调整，出现在“花费”栏，float无法split的错误，循环中由5行改为4行即可解决；我艹赛盒啊，坑爹

import pandas as pd
import os

def get_data(path):
    
    filename = path.split('\\')[-1].split('.')[0]
    
    df = pd.read_excel(path)

    df.reset_index(inplace = True)
    
    print('数据提取中，请稍等：')
    
    for i in range(0,len(df)//4):
        df.loc[i,'来源渠道_1'] = df.loc[i * 4 + 4,'来源渠道']
        df.loc[i,'状态_1'] = df.loc[i * 4 + 3,'状态']
        df.loc[i,'活动名称_1'] = df.loc[i * 4 + 5,'活动名称']
        df.loc[i,'竞价策略_1'] = df.loc[i * 4 + 3,'竞价策略']
        df.loc[i,'曝光量_1'] = df.loc[i * 4 + 3,'曝光量']
        df.loc[i,'点击量_1'] = df.loc[i * 4 + 3,'点击量']
        df.loc[i,'花费_1'] = df.loc[i * 4 + 3,'花费'] #.split(' ')[-1]
        df.loc[i,'点击率_1'] = df.loc[i * 4 + 3,'点击率']
        df.loc[i,'CPC_1'] = df.loc[i * 4 + 3,'CPC']
        df.loc[i,'出单数_1'] = df.loc[i * 4 + 3,'出单数']
        df.loc[i,'贡献毛利润_1'] = df.loc[i * 4 + 3,'贡献毛利润'] #.split(' ')[-1]
        df.loc[i,'贡献销售额_1'] = df.loc[i * 4 + 4,'贡献毛利润'] #.split(' ')[-1]
        df.loc[i,'转化率_1'] = df.loc[i * 4 + 3,'转化率']
        df.loc[i,'Acos_1'] = df.loc[i * 4 + 3,'ACoS']
      
    datadf = df[['来源渠道_1','状态_1','活动名称_1','竞价策略_1','曝光量_1','点击量_1','花费_1','点击率_1','CPC_1','出单数_1','贡献毛利润_1','贡献销售额_1','转化率_1','Acos_1']]
    datadf.columns = ['来源渠道','状态','活动名称','竞价策略','曝光量','点击量','花费','点击率','CPC','出单数','贡献毛利润','贡献销售额','转化率','Acos']
    datadf = datadf[~datadf['来源渠道'].isnull()] #删除来源渠道中为空值的行
    
    #去掉3个列中的货币符号，三个写在一起会报错，  采用split(' ')这种方式也会报错
    datadf['花费'] = datadf['花费'].apply(lambda x:x.split()[-1])
    datadf['贡献毛利润'] = datadf['贡献毛利润'].apply(lambda x:x.split()[-1])
    datadf['贡献销售额'] = datadf['贡献销售额'].apply(lambda x:x.split()[-1])
    
    datadf = datadf.replace('-',0) #将未有值全部替换成0，此处Acos栏替换不准
    datadf[['花费','贡献毛利润','贡献销售额']] = datadf[['花费','贡献毛利润','贡献销售额']].astype('float')
    
    #datadf[['花费','贡献毛利润','贡献销售额']] = datadf[['花费','贡献毛利润','贡献销售额']].apply(lambda x:x.split()[-1])

    #datadf[['花费','贡献毛利润','贡献销售额']] = datadf[['花费','贡献毛利润','贡献销售额']].apply(pd.to_numeric,errors='coerce').fillna(0)
    #datadf[['花费','贡献毛利润','贡献销售额']] = datadf[['花费','贡献毛利润','贡献销售额']].astype('float')
      
    #output_path = filename + '_数据已提取' + '.xlsx'
    #datadf.to_excel(output_path,index = False)
    
    #对广告活动进行汇总类处理
    datadf['国家'] = datadf['来源渠道'].apply(lambda x : x.split('-')[-1])
    datadf_group = datadf.groupby('国家',as_index = False)[['出单数','花费','贡献毛利润','贡献销售额']].sum()
    Exchange = {'US':1,
                'CA':0.7319,
                'MX':0.0434,
                'UK':1.2305,
                'DE':1.1243,
                'FR':1.1243,
                'IT':1.1243,
                'ES':1.0972,
                'IN':0.0132,
                'JP':0.009319,
                'AU':0.6878,
                'AE':0.2723}
    
    for i in range(len(datadf_group)):
        datadf_group.loc[i,'花费$'] = datadf_group.loc[i,'花费'] * Exchange[datadf_group.loc[i,'国家']]
        datadf_group.loc[i,'贡献毛利润$'] = datadf_group.loc[i,'贡献毛利润'] * Exchange[datadf_group.loc[i,'国家']]
        datadf_group.loc[i,'贡献销售额$'] = datadf_group.loc[i,'贡献销售额'] * Exchange[datadf_group.loc[i,'国家']]
        
    writer = pd.ExcelWriter(path)
    df.to_excel(writer,'原始数据',index = False)
    datadf.to_excel(writer,'已提取数据',index = False)
    datadf_group.to_excel(writer,'汇总数据',index = False)
    writer.save()

    # datadf['国家'] = datadf['来源渠道'].apply(lambda x : x.split('-')[-1])
    # datadf_group = datadf.groupby('国家')[['花费','贡献毛利润','贡献销售额']].sum()    #此程序可以再优化优化
    # output_path = filename + '_数据已提取' + '.xlsx'
    # writer = pd.ExcelWriter(output_path)
    # datadf.to_excel(writer,'sheet1',index = False)
    # datadf_group.to_excel(writer,'data_group')
    # writer.save()
    
    #return(datadf,datadf_group)    
    return datadf

print('请输入CPC中广告活动页面中要提取的文件:')
file_path = input('excel文件:')
#去除输入路径时带入的双引号
if '"' in file_path:
    file_path = file_path.replace('"','')
    
f_path = os.path.dirname(file_path)
os.chdir(f_path)
clean_data = get_data(file_path)

print('数据提取成功，路径为:%s'%f_path)





