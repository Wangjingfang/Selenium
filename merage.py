import numpy as np
import pandas as pd
import os
path = r"D:\data\festival\圣诞20190930"
# transform_path = r"D:\data\keywords\transform.xlsx"
# group_path = r"D:\data\keywords\group.xlsx"
# final_path = r"D:\data\keywords\final.xlsx"
# class_path = r"D:\data\keywords\class.xlsx"
# upload_path = r"D:\data\keywords\upload\upload-{}.xlsx".format(path[-8:])
def file_name():

    try:
        L=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                    newfile = file + "(1)"
                    print(newfile)
                    #L.append(os.path.join(root, newfile))
                    os.rename(root+"\\"+file, root+"\\"+newfile)
                    #os.rename(root + "\\" + file, dir + "\\" + new_name)
                    #print(newfile)

        return L

    except Exception as e:
        print("获取各文件路径失败", e)


file_name()
# def change_name():
#     for i in L:
#         i = i + "1"
# D:\data\keywords\data_6.9-8.8\027-CA.xlsx
# df = pd.read_excel(L[0])
# df["Group"] = L[0][-14:-12]
# print(df["Group"])
# df["Country"] = L[0][-7:-5]
# print(df["Country"])
# df["Station"] = L[0][-11:-5]
# # (rows=1702,cloumns=26)
# print(df["Station"])

# print(L[0][-11:-5], df.shape)
#
# group_path = r"D:\data\keywords\group.xlsx"
#
# class_path = r"D:\data\keywords\class.xlsx"
#
# gc_path = r"D:\data\keywords\gc.xlsx"
# df_group = pd.read_excel(group_path, sheet_name='Sheet1')
# df_class = pd.read_excel(class_path,sheet_name='Sheet1')
#
# # group_file = pd.read_excel(group_path, sheet_name='Sheet1')
# group_file = pd.merge(df_group, df_class, on='Station', how='left')
# # for i,j,k in zip(df_week,df_exchange,df_group):
# #     print("{},{},{}".format(i,j,k))
#
# print(group_file)
# group_file.to_excel(excel_writer=gc_path, index=None)

# def read_data():
#     try:
#         L = file_name()
#         df_week = pd.read_excel(transform_path, sheet_name='Sheet1')
#         df_exchange = pd.read_excel(transform_path, sheet_name='Sheet2')
#         df_group = pd.read_excel(group_path,sheet_name='Sheet1')
#         upload_file = pd.read_excel(final_path, sheet_name='Sheet1')
#
#         #         df = pd.read_excel(L[0])
#         #         df["Group"] = L[0][-13:-12]
#         #         df["Country"] = L[0][-7:-5]
#         #         df["Station"] = L[0][-11:-5]
#         #         df.columns = list(upload_file.columns)
#         #         upload_file = pd.concat([upload_file, df], axis = 0)
#         m = 0
#         n = 0
#         for l in L:
#             df = pd.read_excel(l)
#             df["Group"] = l[-14:-12]
#             df["Country"] = l[-7:-5]
#             df["Station"] = l[-11:-5]
#             df.columns = list(upload_file.columns)
#             print(l[-11:-5], df.shape)
#             upload_file = pd.concat([upload_file, df], axis=0)
#             n += 1
#             m += df.shape[0]
#         print(n, m)
#         print(upload_file.shape)
#
#         upload_file = pd.merge(upload_file, df_week)
#         upload_file = pd.merge(upload_file, df_exchange, on='Country', how='left')
#         print(upload_file.shape)
#
#         upload_file['Spend$'] = upload_file['Spend'] * upload_file['Price']
#         upload_file['Sales$'] = upload_file['Sales'] * upload_file['Price']
#         upload_file['Sales'] = upload_file['Sales'].replace(0, np.nan)
#         upload_file['Orders'] = upload_file['Orders'].replace(0, np.nan)
#         final_df = upload_file.drop(columns='Price')
#         print(final_df.shape)
#         final_df.to_excel(excel_writer=upload_path, index=None)
#
#     except Exception as e:
#         print("读取数据失败", e)
#
#     else:
#         print("文件已创建，可上传")

