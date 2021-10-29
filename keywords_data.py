import numpy as np
import pandas as pd
import changename as cn
import time
import datetime
import os

def file_name(path):

    try:
        L=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                    L.append(os.path.join(root, file))
                    print((os.path.join(root, file)))
        return L

    except Exception as e:
        print("获取各文件路径失败", e)

def read_data():

    try:
        L = file_name(path)
        df_week = pd.read_excel(transform_path, sheet_name='Sheet1')
        df_transform = pd.read_excel(transform_path, sheet_name='Sheet2')
        df_group = pd.read_excel(group_path,sheet_name='Sheet1')
        upload_file = pd.read_excel(final_path, sheet_name='Sheet1')
        
#         df = pd.read_excel(L[0])
#         df["Group"] = L[0][-13:-12]
#         df["Country"] = L[0][-7:-5]
#         df["Station"] = L[0][-11:-5]
#         df.columns = list(upload_file.columns)
#         upload_file = pd.concat([upload_file, df], axis = 0)
        m = 0
        n = 0
        for l in L:
            df = pd.read_excel(l)
            #df["Group"] = lambda g : if g = df_group['Station']
            #df["Group"] = l[-14:-12]
            df["Country"] = l[-7:-5]
            df["Station"] = l[-11:-5]
            df.columns = list(upload_file.columns)
            print(l[-11:-5], df.shape)
            upload_file = pd.concat([upload_file, df], axis = 0)
            n += 1
            m += df.shape[0]
        print(n, m)
        print(upload_file.shape)
            

        # upload_file = pd.merge(upload_file,df_week)
        # 加入group
        upload_file = pd.merge(upload_file,df_group, on='Station',how = 'left')
        upload_file = pd.merge(upload_file,df_transform, on = 'Country', how = 'left')

        print(upload_file.shape)
        
        
        upload_file['Spend$'] = upload_file['Spend'] * upload_file['Price']
        upload_file['Sales$'] = upload_file['Sales'] * upload_file['Price']
        upload_file['Sales'] = upload_file['Sales'].replace(0,np.nan)
        upload_file['Orders'] = upload_file['Orders'].replace(0,np.nan)
        final_df = upload_file.drop(columns = 'Price')
        print(final_df.shape)
        final_df.to_excel(excel_writer = upload_path, index = None)

    except Exception as e:
        print("读取数据失败", e)
        
    else:
        print("文件已创建，可上传")

def main():

    global transform_path, final_path, upload_path, group_path, gc_path, path


    # path = r"D:\data\keywords\others\data_09.24-10.23\AFT172"
    path = r"D:\data\keywords\JP\09.24-10.23"
    #path-others = D:\data\keywords\others\7.4-8.31"   D:\data\keywords\important\7.4-8.31  D:\data\keywords\data_7.4-8.31
    # 换算表
    group_path = r"D:\data\keywords\group.xlsx"
    # ### gc_path = r"D:\data\keywords\gc.xlsx"
    transform_path = r"D:\data\keywords\transform.xlsx"
    final_path = r"D:\data\keywords\final.xlsx"
    # upload_path = r"D:\data\keywords\upload\imptntUp\upload-{0}-{1}.xlsx".format(datetime.date.today(), path[-6:])
    upload_path = r"D:\data\keywords\upload\JP\upLoad-{}.xlsx".format(path[-11:])
    # upload_path = r"D:\data\keywords\upload\othersUp\upLoad-{}.xlsx".format(path[-11:])  # imptntUp
    # upload_others_path  = r"D:\data\keywords\upload\othersUp\  D:\data\keywords\upload\imptntUp  D:\data\keywords\upload   D:\data\keywords\upload\othersUp

    cn.changename(path)
    # cn.moveimpstation(totalpath,imppathbef,imppathaft)

    read_data()
    

if __name__ == '__main__':

    main()