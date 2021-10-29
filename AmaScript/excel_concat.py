# -*- coding: utf-8 -*-

"""
@Author: MarlonYang

@Date  : 2021/3/4 17:21

@File  : excel_concat.py

@Desc  : ERP导出的FBA listing数据报告合并脚本

path：存放多份ERP导出的excel
final_path：生成文件路径

"""

import pandas as pd
import numpy as np
import os

def file_name(path):

    try:
        L=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.xls':
                    print(os.path.splitext(file))
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
            total_file = pd.concat([total_file, df], axis = 0)
        
        print(total_file.shape)

        data_cleaning(total_file, final_path)
        
    except Exception as e:
        print("合并失败", e)
        
    else:
        print("文件已创建")

def data_cleaning(total_file, final_path):
    try:
        #截取想要字段
        total_file['Country'] = total_file['渠道来源'].map(lambda x: x[-2:])
        total_file['Station'] = total_file['渠道来源'].map(lambda x: x[-6:])

        #拼接渠道来源、SellSKU、ASIN成唯一码
        total_file['渠道ASIN'] = list(map(lambda x, y: str(x) + str(y),total_file['渠道来源'],total_file['ASIN']))
        total_file['唯一'] = list(map(lambda x, y: str(x) + str(y), total_file['Station'], total_file['SellSKU']))
        total_file['ASIN'] = total_file['ASIN'].map(lambda x: str(x).replace(" ", ""))
        total_file['StationASIN'] = list(map(lambda x, y: str(x) + str(y), total_file['Station'], total_file['ASIN']))
        total_file['StationASIN'] = total_file['StationASIN'].map(lambda x: x if len(x) == 16 else x[:6])

        #上架时间向上补全
        total_file['记录时间'] = total_file['记录时间'].fillna(method='ffill')
        total_file['记录时间'] = total_file['记录时间'].map(lambda x: str(x).split()[0])

        #剔除非法字符
        for i in ["x", "X", "×", "#", '	', "’", "—", "°", "²", '“', '”', "㡳", " ","【", "】","Φ"]:
            total_file['产品中文名称'] = total_file['产品中文名称'].map(lambda x: str(x).replace(i, "A"))

        total_file['节日标识'] = total_file['节日标识'].map(lambda x: str(x).replace(",", "|"))
        total_file.replace({"nan": np.nan}, inplace=True)

        #库存计算
        # total_file['总库存'] = list(map(lambda x, y, z: x+y+z, total_file['采购中'], total_file['运输途中'], total_file['可用库存']))
        # total_file['待入库存'] = list(map(lambda x, y: x-y, total_file['可用库存'], total_file['当前库存']))
        #
        #补全剩余9列
        for i in range(7):
            total_file[str(i)] = ""

        data_filter = total_file[["渠道来源","Country","Station","渠道ASIN","唯一","StationASIN","SKU","ASIN","SellSKU","0","1","2","3","4","listing状态","产品活跃度","产品中文名称","Group","销售小组","记录时间",
         "5","可用库存","当前库存","6","默认运输方式","采购单价","采购中","运输途中","估算销量","review评分","review个数","库龄","价格","本地仓库存","可卖天数","可售数量","产品状态","产品物流属性","节日标识",]]
        #最终列顺序
        # # data_filter = total_file[['销售小组（一级）','Country','渠道来源','唯一','StationASIN','ASIN','SKU','SellSKU','在线状态','上架时间','产品中文名称',
        #                           '节日标识','0','1','2','3','4','5','6','7','8','估算销量','可卖天数','总库存','采购中','运输途中','待入库存','可用库存','当前库存','原价','review评分','review个数']]



        data_filter.to_excel(excel_writer=final_path, index=None)

    except Exception as e:
        print("数据处理失败", e)

    else:
        print("数据处理成功")

def main():

    path = r"D:\data\ERP每周批量\FBA"
    final_path = r"D:\data\ERP每周批量\FBA\FBA.xlsx"

    # path = r"D:\data\ERP每周批量\FBM"
    # final_path = r"D:\data\ERP每周批量\FBM\FBM.xlsx"

    # path = r"E:\ERP下载\爆旺款FBM"
    # final_path = r"E:\ERP下载\爆旺款FBM.xlsx"

    # path = r"E:\ERP下载\节日FBM"
    # final_path = r"E:\ERP下载\节日FBM.xlsx"

    # path = r"E:\ERP下载\大建云仓项目"
    # final_path = r"E:\ERP下载\大建云仓项目.xlsx"

    concat_excel(path, final_path)

if __name__ == '__main__':
    main()