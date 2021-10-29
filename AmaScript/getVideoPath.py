# -*- coding: utf-8 -*-

"""
@Author: MarlonYang

@Date  : 2021/5/25 09:54

@File  : getVideoPath.py

@Desc  :


"""
import pandas as pd
import os


def file_name():

    try:
        filenames=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                    filenames.append(os.path.join(root, file))

    except Exception as e:
        print("获取各文件路径失败", e)

    else:
        print("文件已获取")
        return filenames

#写Excel
def write_excel(filenames):
    try:
        video_file = pd.DataFrame(columns=['SKU', 'Path', 'Type'])
        n = 0
        for file in filenames:

            video_file.loc[n, "SKU"] = file.split("\\")[-1].split(".")[0]
            video_file.loc[n, "Path"] = file

            type_name = "_{}_{}".format(file.split("\\")[-1].split(".")[0], "测试")
            for i in file.split("\\")[4:][:-1]:
                type_name = "{0}_{1}".format(type_name, i)
            video_file.loc[n, "Type"] = type_name

            n +=1
            video_file.to_excel(excel_writer=to_path, index=None)

    except Exception as e:
        print("写入excel失败", e)

    else:
        print("Excel已生成")

def main():
    global path, to_path, final_path

    # 输入路径文件夹路径
    path = r"D:\SBV\测试视频文件20210820"
    # 输出到Excel
    to_path = r"D:\SBV\测试视频文件20210820\视频路径.xlsx"

    filenames = file_name()
    write_excel(filenames)

if __name__ == '__main__':
    main()