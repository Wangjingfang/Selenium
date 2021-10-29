# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 17:05:15 2021

@author: liuhaolin
"""

import os,time
import requests
import re
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions  #支持浏览器插件
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
    options.add_argument("--user-data-dir="+r"D:/Program Files/GoogleCache/Chrome/UserData/") 
    # options.add_argument("--user-data-dir="+r"C:/Users/liuhaolin/AppData/Local/Google/Chrome/User Data/") 

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
    
    # 模拟移动设备
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"')
    
    #需要指定Google驱动的文件位置,chromedriver_Home     下载地址：http://npm.taobao.org/mirrors/chromedriver/
    driver = webdriver.Chrome(chrome_options=options,executable_path="D:/Reports/Tools/chromedriver")
    # 返回驱动等待的变量
    # wait = WebDriverWait(driver, 15)
    driver.maximize_window()

if __name__ == '__main__':    

    # SITE = 'https://www.sif.com/search'
    # SITE = 'https://app.isellerpal.com/data/asinreverse'
    SITE = 'https://members.helium10.com/cerebro?'
    
    #ASIN列表Excel地址以及一次多少条
    path = r"C:\Users\liuhaolin\Desktop\666.xlsx"
    LoadBunch = 10

    driver_options()

    Now_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    i = 0

    df = pd.read_excel(path, sheet_name = 0)
    #ASIN列转列表
    AsinList = df['ASIN'].values.tolist()[:200]
    StepByLoadBunch = [AsinList[i:i+LoadBunch] for i in range(0,len(AsinList),LoadBunch)]

    for y,x in enumerate(tqdm(StepByLoadBunch)):
        
        
        time.sleep(random.randint(5,10))
        
        Try_Count = 0
        while Try_Count <=3:
            try:
                driver.get(SITE)

                #打乱下ASIN顺序以免某些狗掉的ASIN导致无法搜索
                random.shuffle(x)
                
                ASINs = " ".join(x) + ' '

                # #SIF版本
                # time.sleep(random.randint(5,10))
                # AsinSearch = driver.find_element_by_xpath('//*[@placeholder="输入ASIN，多个请使用逗号分隔"]')
                # AsinSearch.clear()
                # AsinSearch.send_keys(ASINs)

                # driver.find_element_by_xpath("//*[contains(text(),'搜 索')]").click()

                # time.sleep(3)
                # driver.find_element_by_xpath("//*[@class='batch']/*[contains(text(),'批量下载流量词')]").click()
                
                # time.sleep(3)
                # driver.find_element_by_xpath("//*[@class='el-checkbox__input']").click()
                
                # time.sleep(3)
                # driver.find_element_by_xpath("//*[@class='batch']/*[contains(text(),'下载流量词')]").click()


                # #isellerpal版本
                # time.sleep(random.randint(5,10))
                # driver.find_element_by_xpath("//*[@class='el-popover__reference-wrapper']//*[contains(text(),'热门搜索词')]").click()
                # time.sleep(0.5)
                # driver.find_element_by_xpath("//*[@class='el-dropdown-menu__item']//*[contains(text(),'全部关键词')]").click()
                # time.sleep(0.5)
                # AsinSearch = driver.find_element_by_xpath('//*[@placeholder="请输入ASIN"]')
                # AsinSearch.send_keys(ASINs)
                # time.sleep(1)
                # driver.find_element_by_xpath("//*[@type='button']//*[@class='el-icon-search']").click()

                # time.sleep(random.randint(5,10))
                # driver.find_element_by_xpath("//*[@type='button']/*[contains(text(),'下载')]").click()


                # #Helium10版本
                WebDriverWait(driver, 72).until(ec.visibility_of_element_located((By.XPATH,"//*[@class='cerebro-search-form']//*[contains(text(),'Get Keywords')]")))
                
                time.sleep(1)
                
                AsinSearch = driver.find_element_by_xpath("//*[@class='multi-asin-search-container']//input")
                AsinSearch.send_keys(ASINs)
                
                time.sleep(2)
                driver.find_element_by_xpath("//*[@class='cerebro-search-form']//*[contains(text(),'Get Keywords')]").click()
                
                time.sleep(2)
                try:
                    driver.find_element_by_xpath("//*[@class='sa-button-container']//*[contains(text(),'New Search')]").click()
                    
                finally:
                    WebDriverWait(driver, 72).until(ec.visibility_of_element_located((By.XPATH,"//*[@class='dropdown float-right']//button")))
                    
                    time.sleep(1)
                    
                    driver.find_element_by_xpath("//*[@class='dropdown float-right']//button").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//*[@class='dropdown float-right show']//*[@data-format='xlsx']").click()
                    
                    WebDriverWait(driver, 72, 0.5).until(ec.visibility_of_element_located((By.XPATH,"//*[@class='tooltipster-box']//*[contains(text(),'Exported!')]")))
                    time.sleep(random.randint(1,3))
                    i += 1
                    break
                
            except:
                Try_Count += 1
                print("获取失败,第%s次尝试刷新"%Try_Count)
                driver.refresh()
                time.sleep(5)
                continue

driver.quit() 

print('搞完了，最后一个ASIN：%s'%x[:-1])

# End_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# # 发送到钉钉群
# json_data = {
#           "msgtype": "text",
#           "text": {
#               "content": "AMZ(SearchTerm)\n启动时间：{0}\n结束时间：{1}\n数据量：{2}\最后ASIN：{3}".format(Now_Time,End_Time,i*10,ASINs[:-1])  # 发送内容
#           },
#           "at": {
#               "atMobiles": [
#               ],
#               "isAtAll": False  # 是否要@某位用户
#           }
#       }

# ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=' \
#                     '66571ff131625d3a0f9f8a053333939a571ff902ee1f9a8a5af8a8dc5de04b9f'
#                     # 公司钉钉群 '314ba5ccba18c377ec9d688543a6b5afcb2baf6319023e29878278453f3ab96c'
#                     # GOGO哒     '4d7674403085618ece3003a8166f5f7bce07f160851e496f78e2abc4c5026e4a'
#                     # 执行记录    '66571ff131625d3a0f9f8a053333939a571ff902ee1f9a8a5af8a8dc5de04b9f'

# requests.post(url=ding_url, json=json_data)
# print('信息发送成功。')