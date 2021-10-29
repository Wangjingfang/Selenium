import os
import pandas as pd
import shutil
# dir = input('请输入文件路径：')
# path = r"D:\data\festival\圣诞20190930"
# 37
sbvpath = r"D:\data\F-SBV-Data\F部广告活动09.24-10.23"
sdpath = r"D:\data\F-SD-Data\F部SD广告09.24-10.23"
sbpath = r"D:\data\F-SB-Data\F部SB广告09.24-10.23"

path = r"D:\data\keywords\others\data_09.24-10.23"
imppathbef = r"D:\data\keywords\important\09.24-10.23\BEF100"
imppathaft = r"D:\data\keywords\important\09.24-10.23\AFT100"
videopath = r"D:\SBV\测试视频文件20210530\ppt视频 批量测试 输出"

def file_name(videopath):

    try:
        filenames=[]
        for root, dirs, files in os.walk(videopath):
            for file in files:
                    filenames.append(os.path.join(root, file))

    except Exception as e:
        print("获取各文件路径失败", e)

    else:
        print("文件已获取")
        return filenames

def changeSBVideoname(videopath):
    df = pd.read_excel(r"D:\SBV\videoname.xlsx",sheet_name= 0)
    for root, dirs, files in os.walk(videopath):
        for i in range(len(files)):

            filename = files[i]
            print(filename)
            newname = list(df.loc[df["视频名称"] == filename]["更改为"])[0]
            newvideoname = str(newname) + ".mp4"
            print(newvideoname)
            os.rename(root + "\\" + filename, root + "\\" + newvideoname)


def changeSBVname(sbvpath):
    for root, dirs, files in os.walk(sbvpath):
        for i in range(len(files)):

            filename = files[i]
            print(filename)
            new_name = filename[:10] +".xlsx"

            print(new_name)
            os.rename(root + "\\" + filename, root + "\\" + new_name)


def changename(path):
    for root, dirs, files in os.walk(path):
        for i in range(len(files)):

            filename = files[i]
            print(filename)
            if "_SBV" in filename :
                new_name = filename[:10] + ".xlsx"

            elif "_SD" in filename:
                new_name = filename[:9] + ".xlsx"

            elif "_SB" in filename:
                new_name = filename[:9] + ".xlsx"
            else:
                new_name = filename[:6] + ".xlsx"
                # new_name = filename[:6] + " 21.05.csv"
            print(new_name)
            os.rename(root + "\\" + filename, root + "\\" + new_name)
            #print(new_name)

def moveimpstation(path,imppathbef,imppathaft,sbvpath,sdpath,sbpath):

    bef100stationlist = ["027-CA","027-US","028-US","071-UK","071-US","079-DE","079-US","089-DE","089-IT","098-DE","098-UK","098-US"]

    aft100stationlist = ["122-DE","122-ES","122-FR","122-IT","122-UK","122-US","128-DE","128-UK","128-ES","128-FR","128-IT","128-US","172-DE","172-UK","172-US",
                         "175-DE","175-UK","178-DE","178-IT","178-UK","231-DE","231-UK","231-US","285-DE","285-UK","285-IT","334-DE","334-UK","354-UK","354-DE",
                         "355-UK","355-DE","384-DE","384-UK","384-US","390-DE","390-IT","390-UK","403-US","404-US","404-IT","416-US","430-US","451-DE"]

    files_list = os.listdir(path)
    #"['027-AU.xlsx', '027-BR.xlsx', '027-JP.xlsx'... '231-ES.xlsx', '231-FR.xlsx']"
    # print(files_list)
    if len(files_list) > 0:
        for file in files_list:
            if "_SBV" in file:
                shutil.move(path + "\\"+ file, sbvpath + "\\" + file)
                print(file)
                continue

            if "_SD" in file:
                shutil.move(path + "\\" + file, sdpath + "\\" + file)
                print(file)
                continue

            if "_SB" in file:
                shutil.move(path + "\\" + file, sbpath + "\\" + file)
                print(file)
                continue

            filename = file[:6]

            if filename in bef100stationlist:
                # 移动文件
                shutil.move(path + "\\"+ file, imppathbef + "\\" + file)
            if filename in aft100stationlist:
                shutil.move(path + "\\"+ file, imppathaft + "\\" + file)


if __name__ == '__main__':

    # changeSBVideoname(videopath)
    # changeSBVname(sbvpath)

    changename(path)
    moveimpstation(path,imppathbef,imppathaft,sbvpath,sdpath,sbpath)