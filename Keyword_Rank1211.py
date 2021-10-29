# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:05:11 2020


@author: l1569
"""


from datetime import date
import time
import requests
import re
from PIL import Image
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import openpyxl
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import urllib.parse as urlparse
from texttable import Texttable
import pandas as pd
from pandas.plotting import  table
import matplotlib.pyplot as plt
import xlwt, time, xlrd


#更换地址邮编
def change_address(postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            # driver.find_element_by_id('nav-global-location-slot').click()
            time.sleep(3)
        except Exception as e:
            driver.refresh()
            time.sleep(10)
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(3)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            time.sleep(2)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(2)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(2)
                break
            except Exception as NoSuchElementException:
                driver.refresh()
                time.sleep(10)
                continue
        print("重新选择地址")
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(2)
    driver.refresh()
    time.sleep(3)


if __name__ == '__main__':    
    # 设置get直接返回，不再等待界面加载完成
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()
    
    # 无窗口模式
    # chrome_options.add_argument('--headless')
    
    # 禁止硬件加速，避免严重占用cpu
    options.add_argument('--disable-gpu')
    # 关闭安全策略
    options.add_argument("disable-web-security")
    # 禁止图片加载
    # options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    # 隐藏Chrome正在受到自动软件的控制
    options.add_argument('disable-infobars')
    # 设置开发者模式启动，该模式下webdriver属性为正常值
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #指定浏览器分辨率
    options.add_argument('window-size=1920x1080')
    
    # 模拟移动设备
    # chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"')
    
    #需要指定Google驱动的文件位置,executable_path="D:/Reports/Python/chromedriver"   下载地址：http://npm.taobao.org/mirrors/chromedriver/
    driver = webdriver.Chrome(chrome_options=options,executable_path="D:/Reports/Python/chromedriver")
    # 返回驱动等待的变量
    wait = WebDriverWait(driver, 20, 5)
    # driver.maximize_window()


    SITE = 'https://www.amazon.com'
    #设置要查询的关键词
    KEYWORDS = ['nail drills for acrylic nails','nail drill kit','nail drill','machine for acrylic nails','electric nail drill','efile nail drill','acrylic nail drill']
    #需要查询的产品Asin值
    Asin =["B088NKFC43"]
    #设置US邮编
    postal = "20237"
    
    driver.get(SITE)
    time.sleep(3)
    change_address(postal)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
    
    Now_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    record_sheet = pd.DataFrame()
    i = 0
    for keyword in KEYWORDS:
        #就抓每个关键词前1-?页
        for page in range(1, 4):
            #生成搜素结果页面的url
            data = {
                "k": keyword,
                "page": page,
                "ref": "sr_pg_" + str(page)
            }
            search_page_url = SITE +'/s?' + urlparse.urlencode(data)
            print("当前Url：", search_page_url)
            
            driver.get(search_page_url)
            
            # css选择器，返回结果存在跳出，异常报错
            try:
                time.sleep(3)
                wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
            except:
                time.sleep(3)
                print("url: " + search_page_url.format(i) + "获取失败,尝试刷新")
                driver.refresh()
                pass

            time.sleep(3)
            #PyQuery
            doc = pq(driver.page_source)


            MainList = doc('.s-main-slot.s-result-list.s-search-results.sg-row')      
            AsinList = MainList.children().items()
            for asin in Asin:
                y_y = i
                
                for child in AsinList:
                    ASIN_TEXT = child.attr('data-asin').strip()
                    if ASIN_TEXT == asin:                           
                        rank =  child.attr('data-index').strip()
                        sponsor = child('.s-label-popover-default .a-size-mini.a-color-secondary').text()             
                        record_sheet.loc[i,'sponsor'] = sponsor
                        record_sheet.loc[i,'page'] = "第" + str(page) +"页"
                        record_sheet.loc[i,'rank'] = "第" + rank +"位"
                        
                        record_sheet.loc[i,'current_url'] = search_page_url
                        record_sheet.loc[i,'ASIN'] = asin
                        record_sheet.loc[i,'keywords'] = keyword
                        TotalItemSource = doc('span[dir="auto"]')[0].text
                        TotalItem = re.findall('of(.*?)for', TotalItemSource)[0].strip()
                        record_sheet.loc[i,'Total_Item'] = TotalItem
                        record_sheet.loc[i,'Now_Time'] = Now_Time
                        
                        i += 1
                        
                if i == y_y:
                  record_sheet.loc[i,'page'] = "第" + str(page) +"页未找到"
                  record_sheet.loc[i,'rank'] = ""
                  record_sheet.loc[i,'sponsor'] = ""
                  
                  record_sheet.loc[i,'current_url'] = search_page_url
                  record_sheet.loc[i,'ASIN'] = asin
                  record_sheet.loc[i,'keywords'] = keyword
                  TotalItemSource = doc('span[dir="auto"]')[0].text
                  TotalItem = re.findall('of(.*?)for', TotalItemSource)[0].strip()
                  record_sheet.loc[i,'Total_Item'] = TotalItem
                  record_sheet.loc[i,'Now_Time'] = Now_Time
                  
                  i += 1


Things=pd.DataFrame(record_sheet,columns=['Now_Time','ASIN','keywords','Total_Item','page','rank','sponsor'])

print(Things)



# DataFrame表格转存Excel
Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
To_path = r"E:\Reports\Keyword_Rank跟进\Keyword_{0}.xlsx".format(Time)

Things.to_excel(excel_writer = To_path, index = None)


# DataFrame表格转图片
# plt.rcParams['font.sans-serif'] = ['SimHei']#显示中文字体
# fig = plt.figure(figsize=(2, 3), dpi=1400)#dpi表示清晰度
# ax = fig.add_subplot(111, frame_on=False)
# ax.xaxis.set_visible(False)  # hide the x axis
# ax.yaxis.set_visible(False)  # hide the y axis
# table(ax, Things, loc='center')  # 将df换成需要保存的dataframe即可
# plt.savefig('C:/Users/l1569/Desktop/Things_'+ Now_Time +'.png')


## DataFrame表格加线框
# tb=Texttable() # 初始化Texttable
# tb.set_cols_align(['c','c','l','l','c','c','c']) # 设置对齐方式
# tb.set_cols_dtype(['t','t','t','t','t','t','t']) # 设置每列的数据类型为text
# tb.set_cols_width([12,25,8,20,8,10]) # 设置列宽
# tb.header(Things.columns) # 设置表头
# tb.add_rows(Things.values,header=False) # 为表格添加数据
#print(tb.draw())


## 发送到钉钉群
# json_data = {
#           "msgtype": "text",
#           "text": {
#               "content": "AMZ：" + tb.draw(),  # 发送内容
#           },
#           "at": {
#               "atMobiles": [
#               ],
#               "isAtAll": False  # 是否要@某位用户
#           }
#       }

# ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=' \
#                     '4d7674403085618ece3003a8166f5f7bce07f160851e496f78e2abc4c5026e4a'
#                     # 公司钉钉群 '314ba5ccba18c377ec9d688543a6b5afcb2baf6319023e29878278453f3ab96c'
#                     # GOGO哒     '4d7674403085618ece3003a8166f5f7bce07f160851e496f78e2abc4c5026e4a'

# requests.post(url=ding_url, json=json_data)
# print('信息发送成功。')  
