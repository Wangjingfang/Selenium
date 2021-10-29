# -*- coding:UTF-8 -*-

# coding=utf8
import pandas as pd
import os, time
import changename as cn
# 业绩报告表
def file_name():

    try:
        L=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    L.append(os.path.join(root, file))
                    print(file)
        return L

    except Exception as e:
        print("获取各文件路径失败", e)

def read_data():

    try:
        df_exchange = pd.read_excel(transform_path, sheet_name='Sheet2')
        upload_file = pd.read_excel(final_path, sheet_name='Sheet1')

        L = file_name()

        for l in L:

            # l.decode("utf8mb4")
            df = pd.read_csv(l)
#             #当月
#             df["Group"] = l[-12]
#             df["Country"] = l[-6:-4]
#             df["Station"] = l[-10:-4]
#             df["Month"] = "19.06"
            # 027-JP 18.09.csv
            #新增
            # df["Group"] = l[-18]
            # 027-US 19.09.csv
            # print(df.shape)
            # print(df.columns.values)

            # df.rename(columns={'A': 'a', 'B': 'b', 'C': 'c'}, inplace=True)
            # print(df.columns.values)
            # l.columns = ['a','b','c']

            df.columns = ['(Parent) ASIN', '(Child) ASIN', 'Title', 'SKU', 'Sessions',
             'Session Percentage', 'Page Views', 'Page Views Percentage',
             'Buy Box Percentage', 'Units Ordered','Units Ordered - B2B', 'Unit Session Percentage',
             'Unit Session Percentage - B2B', 'Ordered Product Sales','Ordered Product Sales - B2B', 'Total Order Items', 'Total Order Items - B2B']

            # print(11)
            # print(df.shape)
            # print(df.columns.values)


            # print(df.columns.values)

            df["Country"] = l[-12:-10]
            df["Station"] = l[-16:-10]
            df["Month"] = l[-9:-4]

            if df.shape[1] > 17:
                cols=[x for i,x in enumerate(df.columns) if i in [10,12,14,16]]
                df = df.drop(cols, axis = 1)

            # print(1)
                
            print(df["Station"][0], df["Month"][0], df.shape)

            # CA EU 是小写表头，US,JP是大写
            for i in ["Sessions","Page Views","Units Ordered","Total Order Items"]:
                if df[i].dtype == "object":
                    df[i] = df[i].apply(lambda x: "".join(x.split(','))).astype('int64')

            # print(1)
            
            upload_file = pd.concat([upload_file, df], axis = 0, ignore_index=True)

        # print(1)
        # upload_file.rename(columns={'':''})
        upload_file = pd.merge(upload_file,df_exchange, on = 'Country', how = 'left')
        upload_file = upload_file.drop(columns = 'Title')

        print(upload_file["Ordered Product Sales"].dtypes)
        
        for i in ['Can$','€','$','£',',','￥','¥','JP¥']:
            upload_file["Ordered Product Sales"] = upload_file["Ordered Product Sales"].apply(lambda x: "".join(x.split(i)))


        #for i in ["Ordered Product Sales", "Month"]:
        # test_df = upload_file
        # test_df.to_excel(excel_writer=upload_path, index=None)

        for i in ["Ordered Product Sales"]:
            upload_file[i] = upload_file[i].astype('float64')
            #upload_file[i] = upload_file[i].astype('decimal')
        # for i in ["Month"]:
        #     upload_file[i] = upload_file[i]
        # "%.6f" % float(x)
        # "Buy Box Percentage"
        print(3)
        # 美欧 将float 转为 str ,日本没有
        for i in ['Session Percentage', 'Page Views Percentage', 'Buy Box Percentage', 'Unit Session Percentage']:
            upload_file[i] = upload_file[i].apply(lambda x: "".join(x.split(',')))
            upload_file[i] = upload_file[i].apply(lambda x: "".join(x.split('%'))).astype('float64') / 100

        upload_file['Sales$'] = upload_file['Ordered Product Sales'] * upload_file['Price']
        final_df = upload_file.drop(columns = 'Price')
        print(final_df.shape)
        final_df.to_excel(excel_writer = upload_path, index = None)

    except Exception as e:
        print("读取数据失败", e)
        
    else:
        print("文件已创建，可上传")

def main():

    global path, upload_path, transform_path, final_path
    
    #当月
#     path = r"C:\Users\Administrator\Desktop\Summary\Orders\201906"
#     upload_path = r"C:\Users\Administrator\Desktop\Summary\Orders\upload\upload-{}.xlsx".format(path[-6:])
    
    #新增
    # D:\data\业绩报表
    path = r"D:\data\bussinesReport\JP202109"

    # path = r"C:\Users\Administrator\Desktop\Summary\Orders\201907"
    today_date = time.strftime("%Y%m%d", time.localtime(time.time()))
    upload_path = r"D:\data\bussinesReport\bussines_upload\JPupload {}.xlsx".format(today_date)
    
    
    transform_path = r"D:\data\bussinesReport\transform.xlsx"
    final_path = r"D:\data\bussinesReport\final.xlsx"

    # cn.changename(path)
    
    read_data()
    

if __name__ == '__main__':
    main()