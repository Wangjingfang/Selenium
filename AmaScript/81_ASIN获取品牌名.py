# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:04:11 2021

@author: Administrator
"""
# 此脚本的目的在于获取ASIN的listing页面的品牌名称，用于核对是否跟视频广告的品牌是否一致；
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time,random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from tqdm import tqdm
import MySQLdb  #  python -m pip install mysqlclient  安装这个包才能正常执行

db = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'P@ssw0rd123',database = 'db_band',charset = 'utf8mb4')
cursor = db.cursor()            #cursor为游标，返回一个多行多列的结果，在多行多列引用中，必须使用游标；


c_sql = """CREATE TABLE IF NOT EXISTS `brand_info`(
   `渠道来源` VARCHAR(255) NOT NULL,
   `ASIN` VARCHAR(255) NOT NULL,
   `品牌信息` VARCHAR(255) NOT NULL,
   `品牌名` VARCHAR(255) NOT NULL)"""

cursor.execute(c_sql)


path = r"D:\SBV\获取ASIN\11.xlsx"
asin_list = pd.read_excel(path)

# path = input('请输入路径：')
# asin_list = pd.read_excel(path.replace('"',''))
#asin_list = asin_list.loc[asin_list['渠道来源'].str.contains('US|CA|UK|DE|FR|IT|ES')]

chrome_options = Options()
chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=2560x1440')  #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

brower = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

# brower=webdriver.Chrome()

country_url_dict = {'US':'https://www.amazon.com/dp/',
                    'CA':'https://www.amazon.ca/dp/',
                    'UK':'https://www.amazon.co.uk/dp/',
                    'DE':'https://www.amazon.de/dp/',
                    'FR':'https://www.amazon.fr/dp/',
                    'IT':'https://www.amazon.it/dp/',
                    'ES':'https://www.amazon.es/dp/'}

asin_list['国家'] = asin_list['渠道来源'].apply(lambda x:x[-2:].upper())
asin_list['url'] = asin_list['国家'].map(country_url_dict) + asin_list['ASIN'] #通过字典对df中的列的映射

print(asin_list['url'])

# for i in range(0,len(asin_list)):
#     try:
#
#         brower.get(asin_list.loc[i,'url'])
#         time.sleep(3)
#         print('正在获取中品牌中，请稍后；')
#         WebDriverWait(brower, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="bylineInfo"]')))
#         brand_name = brower.find_element_by_xpath('//*[@id="bylineInfo"]').text
#         asin_list.loc[i,'brand_listing'] = brand_name
#     except:
#         asin_list.loc[i,'异常'] = "出现异常"
#
#         continue
#
# brower.quit()
#
# asin_list = asin_list.dropna(subset = ['brand_listing'])  #删除brand_listing列中为空的行
# asin_list.reset_index(inplace=True)

brand_list = ['HEMOTON','BESTonZON','OUNONA','BESTOMZ','NICEXMAS','Yardwe','TOPBATHY','UPKOCH','Cabilock','DOITOOL','YARNOW','Angoily']


# for i in range(0,len(asin_list)):
#     for brand in brand_list:
#         if brand.upper() in asin_list.loc[i,'brand_listing'].upper():
#             asin_list.loc[i,'brand_listing_done'] = brand
#             break
#         else:
#             asin_list.loc[i,'brand_listing_done'] = ''
#
# to_file = path.replace('"','').split('\\')[-1]
# asin_list.to_excel(r"D:\SBV\获取ASIN\1-1.xlsx".format(to_file),index = False)


for i in tqdm(range(0,len(asin_list))):     # tqdm是打印当前进度包
    try:
        brower.get(asin_list.loc[i,'url'])
        time.sleep(random.uniform(2,4))
        WebDriverWait(brower, 5).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="bylineInfo"]')))
        brand_name = brower.find_element_by_xpath('//*[@id="bylineInfo"]').text

        asin_list.loc[i,'brand_listing'] = brand_name
        for brand in brand_list:
            if brand.upper() in asin_list.loc[i,'brand_listing'].upper():
                asin_list.loc[i,'brand_listing_done'] = brand
                break
            else:
                asin_list.loc[i, 'brand_listing_done'] = ''
    except:
        continue
    
    # 数据存入到mysql版本
    # INSERT INTO brand_info(渠道来源, ASIN, 品牌信息) VALUES ('Amazon-Z01123-UK','B085VJJ12W','Visit the POPETPOP Store,' POPETPOP')
    sql = 'INSERT INTO brand_info(渠道来源, ASIN, 品牌信息, 品牌名) VALUES ("%s","%s","%s","%s")'%(asin_list.loc[i,'渠道来源'],asin_list.loc[i,'ASIN'],asin_list.loc[i,'brand_listing'],asin_list.loc[i,'brand_listing_done'])
    cursor.execute(sql)
    db.commit()

# cursor.close()  # 关闭游标
# db.close()  # 关闭数据库连接




