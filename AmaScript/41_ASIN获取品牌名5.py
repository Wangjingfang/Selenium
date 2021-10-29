# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:04:11 2021

@author: Administrator
"""
# 此脚本的目的在于获取ASIN的listing页面的品牌名称，用于核对是否跟视频广告的品牌是否一致；
# 需要的列名    来源渠道（6位或者16位的长站点都行）  ASIN
# url/dp/ASIN 直接进入到该ASIN的产品页


from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=2560x1440')  #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')

brower = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)




path = r"D:\SBV\获取ASIN\5.xlsx"
asin_list = pd.read_excel(path)

country_url_dict = {'US':'https://www.amazon.com/dp/',
                    'CA':'https://www.amazon.ca/dp/',
                    'UK':'https://www.amazon.co.uk/dp/',
                    'DE':'https://www.amazon.de/dp/',
                    'FR':'https://www.amazon.fr/dp/',
                    'IT':'https://www.amazon.it/dp/',
                    'ES':'https://www.amazon.es/dp/'}

# 定义国家和url
asin_list['国家'] = asin_list['渠道来源'].apply(lambda x:x[-2:].upper())
asin_list['url'] = asin_list['国家'].map(country_url_dict) + asin_list['ASIN'] #通过字典对df中的列的映射
print(asin_list['url'])


for i in range(0,len(asin_list)):
    try:

        brower.get(asin_list.loc[i,'url'])
        time.sleep(3)
        print('正在获取中品牌中，请稍后；')
        WebDriverWait(brower, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="bylineInfo"]')))
        brand_name = brower.find_element_by_xpath('//*[@id="bylineInfo"]').text
        asin_list.loc[i,'brand_listing'] = brand_name
    except:
        asin_list.loc[i,'异常'] = "出现异常"

        continue

brower.quit()

asin_list = asin_list.dropna(subset = ['brand_listing'])  #删除brand_listing列中为空的行
asin_list.reset_index(inplace=True)

brand_list = ['HEMOTON','BESTonZON','OUNONA','BESTOMZ','NICEXMAS','Yardwe','TOPBATHY','UPKOCH','Cabilock','DOITOOL','YARNOW','Angoily']


for i in range(0,len(asin_list)):
    for brand in brand_list:
        if brand.upper() in asin_list.loc[i,'brand_listing'].upper():
            asin_list.loc[i,'brand_listing_done'] = brand
            break
        else:
            asin_list.loc[i,'brand_listing_done'] = ''

to_file = path.replace('"','').split('\\')[-1]
asin_list.to_excel(r"D:\SBV\获取ASIN\5-5.xlsx".format(to_file),index = False)

print('品牌获取完成，请在文件下查看；')

# asin_list = asin_list.dropna(subset = ['brand_listing'])  #删除brand_listing列中为空的行
# asin_list['brand_listing'] = asin_list['brand_listing'].apply(lambda x:x.split(' ')[-1])
# asin_list.to_excel(r"D:\SBV\获取ASIN\7-7.xlsx",index = False)





