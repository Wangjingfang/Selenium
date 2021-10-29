# -*- coding: utf-8 -*-

'''
脚本作用：从各站点下载的业绩报告格式不一样（数据类型不一样，表头格式不一样），通过批量处理将其进行整理成一样的格式（清洗），最终为各站点单独csv文件格式，可以成单表导入，也可用下一个脚本程序，合并导入；
1.注意，业绩报告中US,UK,DE中有的标头有17列，有的只有13列，需要添加对应4列，添加日期后18列；
2.为检查无误的报告添加Date,格式要求会提示；
3.由于UK站点存在销售额一栏带有英镑符号，所以对所有销售额一栏进行检查，遇到替换成正常数据；--调试不出来
4.带有B2B的字段中含有一个符“-”，实际不知道是什么输入法输入的，只能通过复制的方法进行程序替换，该符号的字符宽度与正常的英文状态下的横杆字符宽度不一样；但是US站点又是正常的
5.不同表中的同一字段可能是float,可能是int，需要先作判断，再进行清洗；
6.由于excel中识别货币符号，千分位逗号等，python不识别，所以一定要进行检验;
7.业绩报告需要在英文状态下下载，若出现  KeyError: 'Sessions'  则表明有些报告是在中文状态下下载
'''

import pandas as pd
import os

def get_file(path):
    try:
        filenames = []
        for root,dirs,files in os.walk(path):
                for file in files:
                    filenames.append(os.path.join(root,file))
        return filenames
    except Exception as e:
        print('获取文件失败',e)
        
def merge_file(file_path,year_month):    
    filenames = filename_list
       
    for filename in filenames:
        df = pd.read_csv(filename,encoding = 'ISO-8859-1')  #注意读入的是csv文件 
    
        for i in ["Sessions",'Page Views',"Units Ordered","Total Order Items"]:
            if df[i].dtype == "object":
                df[i] = df[i].apply(lambda x: "".join(x.split(','))).astype('int64')
        
        for i in ['Can$','€','$','£',',','US$','US']:
            if df["Ordered Product Sales"].dtype == 'object':
                df["Ordered Product Sales"] = df["Ordered Product Sales"].apply(lambda x: "".join(x.split(i)))
        
        
        for i in ['Session Percentage', 'Page Views Percentage', 'Buy Box Percentage', 'Unit Session Percentage']:
            if df[i].dtype == "object":
                df[i] = df[i].apply(lambda x: "".join(x.split(',')))
                df[i] = df[i].apply(lambda x: "".join(x.split('%'))).astype('float64') /100
        
        df["Ordered Product Sales"] = df["Ordered Product Sales"].astype('float64')
        
        df['Date'] = year_month
        
        for i in df.columns:   #删除US站点本来存在的B2B相关的数据，因为US站点的横杆又是正常状态
            if 'B2B' in i:
                df.drop(i,axis = 1,inplace = True)
        
        df['Units Ordered - B2B'] = 0   #注意此处的横杆不是一般的英文状态下的横杆
        df['Unit Session Percentage - B2B'] = 0
        df['Ordered Product Sales - B2B'] = 0
        df['Total Order Items - B2B'] = 0 
        
        output_path = filename.split('\\')[-1].split('.')[0] + '_done' + '.csv'
        df.to_csv(output_path,index = False)
            
 

print('请输入要添加月份的业绩报告的文件夹名称')         
origin_path = input('文件夹：')
year_month = input('请输入要写入的日期（格式如：2019-10）：')
if '"' in origin_path:
    origin_path = origin_path.replace('"','')

os.chdir(origin_path)
filename_list = get_file(origin_path)    
merge = merge_file(filename_list,year_month)    
    
print('文件检查以及月份添加完成，请在路径中查看：%s'%origin_path)
os.chdir(r'E:\01工作资料')

