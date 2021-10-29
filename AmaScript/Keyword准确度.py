# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 10:58:55 2021

@author: liuhaolin
"""


import time
import requests
import re
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import selenium.common.exceptions  #支持浏览器插件
import urllib.parse as urlparse
import pandas as pd
from datetime import date,datetime, timedelta
import random
from tqdm import tqdm


#浏览器相关
def driver_options():
    global driver
    global wait
    # 设置get直接返回，不再等待界面加载完成
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()

    # 附带本地插件
    # extension_path = r'D:\Reports\Tools\SellerSprite2.7.0_0.crx'
    # options.add_extension(extension_path)   
    
    # 启用本地带插件的浏览器 chrome://version/  个人资料路径
    # options.add_argument("--user-data-dir="+r"D:/Program Files/GoogleCache/Chrome/UserData/") 

    # 无窗口模式
    # options.add_argument('--headless')
    
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
    #忽略证书错误
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    # 模拟移动设备
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"')
    
    #需要指定Google驱动的文件位置,chromedriver_Home     下载地址：http://npm.taobao.org/mirrors/chromedriver/
    driver = webdriver.Chrome(chrome_options=options,executable_path="D:/Reports/Tools/chromedriver")
    # 返回驱动等待的变量
    wait = WebDriverWait(driver, 30, 5)
    # driver.maximize_window()


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


# css选择器，返回结果存在跳出，异常报错刷新
def css_finder():
    Try_Count = 0
    while Try_Count <=6:
        try:
            time.sleep(3)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
            break
        except:
            Try_Count += 1
            print("url: " + search_page_url + "获取失败,第%s次尝试刷新"%Try_Count)
            driver.refresh()
            time.sleep(10)
            continue


if __name__ == '__main__':    

    SITE = 'https://www.amazon.com'
    postal = "20237"

    ExcelPath = r"C:\Users\liuhaolin\Desktop\洁面仪Plus词 (100).xlsx"
    KeywordSaveBunch = 300
    KeywordSheet = pd.read_excel(ExcelPath, sheet_name = 0)
    ASINSheet = pd.read_excel(ExcelPath, sheet_name = 1)

    #关键词列转列表
    KEYWORDS_List = KeywordSheet['Phrase'].values.tolist()

    #ASIN列转列表
    Asins_List = ASINSheet['ASIN'].values.tolist()
    Asins_Set = set(Asins_List)

    EndTime = (datetime.now() + timedelta(minutes=len(KEYWORDS_List)/10)).strftime('%H:%M')
    print('共 %s 个关键词，预计 %s 次抓取完成，预计完成时间：%s'%(len(KEYWORDS_List), len(KEYWORDS_List)/KeywordSaveBunch, EndTime))

    #分批查询保存避免错误耽误时间
    for Times in range(0, len(KEYWORDS_List), KeywordSaveBunch):
        KEYWORDS_List_Bunch = KEYWORDS_List[Times: Times + KeywordSaveBunch]

        driver_options()
        driver.get(SITE)
        time.sleep(random.randint(3,5))
        change_address(postal)

        #列表存储自然位及结果数据
        NatureList = []
        # sponsorList = []
        ResultList = []

        for y,keyword in enumerate(tqdm(KEYWORDS_List_Bunch)):
            #生成搜素结果页面的url
            data = {"k": keyword}
            search_page_url = SITE +'/s?' + urlparse.urlencode(data)

            driver.get(search_page_url)

            css_finder()

            time.sleep(random.randint(5,8))
            #PyQuery
            doc = pq(driver.page_source,parser="html")

            MainList = doc('.s-main-slot').children()

            # #正则直接取出ASIN
            # AsinList = re.findall('<div data-asin="(.*?)" data-index', str(MainList.children()))
            # AsinListWithoutNull = [o for o in AsinList if o != '']

            AsinListForCheck = []
            NatureRankNum = 0
            #这一页的每一个子体元素都遍历一遍
            for child in MainList.items():

                #确定是否产品展示位
                IsASIN = child.attr('data-component-type')
                if IsASIN is None:
                    continue
                elif IsASIN.find('s-search-result') == -1:
                    continue

                #确认是否自然位
                ClassName = child.attr('class')
                if ClassName.find('AdHolder') > -1:
                    continue

                #获取ASIN
                ASIN_TEXT = child.attr('data-asin').strip()

                #获取标题
                Title_TEXT = child('.a-size-base-plus.a-color-base.a-text-normal').text()
                if Title_TEXT == "":
                    Title_TEXT = child('.a-size-medium.a-color-base.a-text-normal').text()

                #获取首图
                ImgLink = child('.s-image').attr('src')

                NatureRankNum = NatureRankNum + 1
                NatureList.append({'Keyword': keyword, 'NatureASIN': ASIN_TEXT, 'Title': Title_TEXT, 'ImgLink': ImgLink, 'Index': NatureRankNum})

                AsinListForCheck.append(ASIN_TEXT)

            AsinListForCheck_Set = set(AsinListForCheck)

            ASIN_Percentage = len(AsinListForCheck_Set&Asins_Set)/len(AsinListForCheck)
            ResultList.append({'Keyword': keyword, '同类ASIN占比': ASIN_Percentage})

        driver.quit() 

        NatureASIN_Sheet = pd.DataFrame(NatureList)
        ResultList_Sheet = pd.DataFrame(ResultList)

        # DataFrame表格转存Excel
        Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        NatureASIN_To_Path = r"D:\Reports\Keyword匹配度\KeywordNatureASIN\{0}_KeywordNatureASIN.xlsx".format(Time)
        ResultList_To_Path = r"D:\Reports\Keyword匹配度\KeywordResultList\{0}_KeywordResultList.xlsx".format(Time)

        NatureASIN_Sheet.to_excel(NatureASIN_To_Path, index = False)
        ResultList_Sheet.to_excel(ResultList_To_Path, index = False)

        print('---------- 抓取完成，等待60s后开始下一批，进度: %s / %s ----------'%(Times + KeywordSaveBunch, len(KEYWORDS_List))) 
        time.sleep(60)

print('Ready')

# # 发送到钉钉群
# json_data = {
#           "msgtype": "text",
#           "text": {
#               "content": "AMZ(Rank)\n爬虫启动：{0}\n结束时间：{1}\n数据量：{2}".format(Now_Time, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), len(Things))  # 发送内容
#           },
#           "at": {
#               "atMobiles": [
#               ],
#               "isAtAll": False  # 是否要@某位用户
#           }
#       }

# ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=' \
#                     '66571ff131625d3a0f9f8a053333939a571ff902ee1f9a8a5af8a8dc5de04b9f'
# requests.post(url=ding_url, json=json_data)
# print('信息发送成功。')  
