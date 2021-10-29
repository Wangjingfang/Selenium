# import pandas as pd
#
# data = pd.read_excel(r"D:\亚马逊FBA库龄库存报告汇总表2021-09-01至2021-09-30-456453 - 亚马逊运营中心.xls")
# rows = data.shape[0]
# department_list = []
# for i in range(rows):
#     temp = data["9月账号首选业务人员部门"][i]
#     if temp not in department_list:
#         department_list.append(temp)  # 将部门的分类存在一个列表中
# for department in department_list:
#     new_df = pd.DataFrame()
#     for i in range(0, rows):
#         if data["9月账号首选业务人员部门"][i] == department:
#             new_df = pd.concat ([new_df, data.iloc [[i], :]], axis=0, ignore_index=True)
#     new_df.to_csv(department+'.xls',encoding='utf_8_sig',index=False)
#     # new_df.to_excel(department+'.xlsx',encoding='utf-8',index=False)

# 好简洁的拆表代码！！！
import pandas as pd

# Excel文件所在的路径
df1 = pd.read_excel(r"D:\data\拆分表\亚马逊FBA库龄库存报告汇总表2021-09-01至2021-09-30-456453 - 亚马逊运营中心.xls",sheet_name=r"亚马逊FBA库龄库存报告汇总表")
# 添加要分组的列名
nodeDataList = list(df1.groupby(['9月账号首选业务人员部门']))
for nodeData in nodeDataList:
    # nodeData 是元组包含两列；nodeData[0] 是元组的第0列，0列是部门名；nodeData[1]是元组的第1列，是拆分表前的所有部门对应的内容
    # print(nodeData[2]) IndexError: tuple index out of range
    #
   nodeData[1].to_excel('D:\data\拆分表' + str(nodeData[0])+ '.xlsx', sheet_name=nodeData[0], index=False)