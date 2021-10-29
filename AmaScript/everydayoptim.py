# -*- coding: utf-8 -*-

"""
@Author: wang

@date: 2021/06/23

@File  : everydayoptim.py

@Desc  : 优化158导出的（库存>=10，周销量>=5）的产品

path：下载的xls 数据表
final_path：生成文件路径

"""

import pandas as pd
import numpy as np
import time
import datetime
import os
from tqdm import tqdm
import pymysql
import sqlalchemy
from sqlalchemy import create_engine

# import MySQLdb  #  python -m pip install mysqlclient  安装这个包才能正常执行
# db = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'P@ssw0rd123',database = 'amadata' ,charset = 'utf8mb4')
# cursor = db.cursor()            #cursor为游标，返回一个多行多列的结果，在多行多列引用中，必须使用游标；

# def file_name(path):
#
#     print(path)
#     for root, dirs, files in os.walk(path):
#         for i in range(len(files)):
#     try:
#         L=[]
#         for root, dirs, files in os.walk(path):
#             for file in files:
#                 if os.path.splitext(file)[1] == '.xls':
#                     print(os.path.splitext(file))
#                     L.append(os.path.join(root, file))
#         return L
#
#     except Exception as e:
#         print("获取各文件路径失败", e)
        
def concat_excel(path, final_path):
    try:


        total_file = pd.DataFrame()

        df = pd.read_excel(path)
        print(df.shape)
        total_file = pd.concat([total_file, df], axis = 0)
        
        print(total_file.shape)

        finish_tb = data_cleaning(total_file, final_path)


        
    except Exception as e:
        print("合并失败", e)
        
    else:
        return finish_tb
        print("文件已创建")

def data_cleaning(total_file, final_path):
    try:
        #截取想要字段
        total_file['Country'] = total_file['渠道来源'].map(lambda x: x[-2:])
        total_file['Station'] = total_file['渠道来源'].map(lambda x: x[-6:])
        print("1")

        # 产品类型FBA，FBM
        total_file['产品类型'] = total_file['备货仓库'].map(lambda x: "FBA" if ( "FBA" in x) else "FBM")

        #拼接渠道来源、SellSKU、ASIN成唯一码
        # total_file['渠道ASIN'] = list(map(lambda x, y: str(x) + str(y),total_file['渠道来源'],total_file['ASIN']))
        total_file['唯一'] = list(map(lambda x, y: str(x) + str(y), total_file['Station'], total_file['SellSKU']))
        total_file['ASIN'] = total_file['ASIN'].map(lambda x: str(x).replace(" ", ""))
        # total_file['StationASIN'] = list(map(lambda x, y: str(x) + str(y), total_file['Station'], total_file['ASIN']))
        # total_file['StationASIN'] = total_file['StationASIN'].map(lambda x: x if len(x) == 16 else x[:6])

        #上架时间向上补全
        total_file['上架时间'] = total_file['上架时间'].fillna(method='ffill')
        total_file['上架时间'] = total_file['上架时间'].map(lambda x: str(x).split()[0])
        print("2")

        #剔除非法字符
        for i in ["x", "X", "×", "#", '	', "’", "—", "°", "²", '“', '”', "㡳", " ","【", "】","Φ"]:
            total_file['产品中文名称'] = total_file['产品中文名称'].map(lambda x: str(x).replace(i, "A"))
        total_file['节日标识'] = total_file['节日标识'].map(lambda x: str(x).replace(",", "|"))
        total_file.replace({"nan": np.nan}, inplace=True)
        print("3")

        #库存计算
        total_file['总库存'] = list(map(lambda x, y, z: x+y+z, total_file['采购中'], total_file['运输途中'], total_file['可用库存']))
        total_file['待入库存'] = list(map(lambda x, y: x-y, total_file['可用库存'], total_file['当前库存']))
        # 计算是否要提高竞价，用一周销量求取每日销量，系数2是冗余系数。
        total_file['平均每日销量*2'] = list(map(lambda x: round(2* x /7, 2), total_file['一周销量']))
        total_file['调整竞价'] = list(map(lambda x, y: "提高竞价" if (round(x,2) >= y ) else "NO", total_file['当前库存'], total_file['平均每日销量*2']))

        # 添加日期，为以后的库存趋势做准备
        total_file['日期'] = datetime.date.today()
        #
        #补全剩余9列
        for i in range(2):

            total_file[str(i)] = ""

        data_filter = total_file[["渠道来源","备货仓库","Country","Station","产品类型", "唯一","SKU","ASIN","SellSKU","0","1","在线状态","活跃状态","日期","产品中文名称","销售小组（一级）","上架时间",
         "总库存","可用库存","当前库存","待入库存","平均每日销量*2","调整竞价","默认运输方式","采购单价","采购中","运输途中","估算销量","今天销量","昨天销量","前天销量","上前销量","一周销量","两周销量","30天销量","90天销量",
                                  "可卖天数","可售数量","产品状态","产品物流属性","节日标识"]]
        #最终列顺序
        # # data_filter = total_file[['销售小组（一级）','Country','渠道来源','唯一','StationASIN','ASIN','SKU','SellSKU','在线状态','上架时间','产品中文名称',
        #                           '节日标识','0','1','2','3','4','5','6','7','8','估算销量','可卖天数','总库存','采购中','运输途中','待入库存','可用库存','当前库存','原价','review评分','review个数']]



        data_filter.to_excel(excel_writer=final_path, index=None)

    except Exception as e:
        print("数据处理失败", e)

    else:
        return data_filter
        print("数据处理成功")

def main():


    path = input("请输入要处理的文件路径：").replace('"','')
    final_path = r"C:\Users\wangjingfang\Desktop\每日库存-{0}.xlsx".format(datetime.date.today())

    # path = r"D:\data\ERP每周批量\FBM"
    # final_path = r"D:\data\ERP每周批量\FBM\FBM.xlsx"

    # path = r"E:\ERP下载\爆旺款FBM"
    # final_path = r"E:\ERP下载\爆旺款FBM.xlsx"

    # path = r"E:\ERP下载\节日FBM"
    # final_path = r"E:\ERP下载\节日FBM.xlsx"

    # path = r"E:\ERP下载\大建云仓项目"
    # final_path = r"E:\ERP下载\大建云仓项目.xlsx"




    # 数据存入到mysql版本
    # INSERT INTO brand_info(渠道来源, ASIN, 品牌信息) VALUES ('Amazon-Z01123-UK','B085VJJ12W','Visit the POPETPOP Store)

    try:
        upload_sheet = concat_excel(path, final_path)

        connect = create_engine('mysql+pymysql://root:P@ssw0rd123@localhost:3306/amadata?charset=utf8mb4')
        upload_sheet.to_sql('inventory_log', connect, index=False, if_exists='append')


        # sql = "load data infile {0} into table inventory_log".format(final_path)
        #
        # cursor.execute(sql)
        # connect.commit() # 提交到数据库执行，一定要记提交哦
    except Exception as e:
        # db.rollback() # 发生错误时回滚
        print(e,"创建失败")
    # 关闭连接对象，否则会导致连接泄漏，消耗数据库资源
    # connect.close()



if __name__ == '__main__':
    main()

