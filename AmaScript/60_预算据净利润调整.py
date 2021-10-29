# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:07:09 2020

@author: Administrator
"""
'''
# =============================================================================
# 预算自动化调整：针对我当前设置的预算
#超出预算的无法用此方法进行修改，里面涉及非常多的逻辑，暂时只修改固定值的预算
让windows每天自动执行两次：第一次执行8:30；  第二次执行18:30；《任务计划程序库》中定义好执行的时间；在log（E盘的log）中生成对应的记录文件
在224行中已设置根据自己的调价策略设置的规则，保证针对自己账号的权限的可用性
# =============================================================================
'''
import requests
import json
import base64
import urllib
import os
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.webdriver.chrome.options import Options

# import muggle_ocr
# sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')

start_Time = time.strftime("%H:%M:%S", time.localtime())
record_log = pd.read_excel(r"D:\01工作资料\000数据脚本\log\预算根据净利润调整.xlsx")
length = len(record_log)
record_log.loc[length,'调整日期'] = time.strftime("%m-%d", time.localtime())
record_log.loc[length,'开始时间'] = time.strftime("%H:%M:%S", time.localtime())

url = 'http://888cpc.irobotbox.com/'

chrome_options = Options()
chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=2560x1440')  #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
brower = webdriver.Chrome(chrome_options=chrome_options)

# brower=webdriver.Chrome()

brower.get(url)
print('CPC网页进入成功')
brower.implicitly_wait(5)
brower.maximize_window()  #窗口最大化

# def get_code():
    
#     img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
#     img.screenshot(r'E:\01工作资料\000数据脚本\log\vcode_pic\code.png')
    
#     with open(r'E:\01工作资料\000数据脚本\log\vcode_pic\code.png', "rb") as f:
#         b = f.read()
#     text = sdk.predict(image_bytes=b)
#     return text

def get_code():

    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    img.screenshot(r'D:\01工作资料\000数据脚本\log\vcode_pic\code60.png')#验证码文件夹位置

    API_Key = 'hhLeDihbTyG64wke7Tp1W8XL'               #你的key
    Secret_Key = 'yIuO5HEXzyZwcST2isT0idK7AYeH8VXd'    #你的秘钥
    # 获取token
    res = requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_Key + '&client_secret=' + Secret_Key)
    res = json.loads(str(res.text))
    access_token = res['access_token']
    #传输百度API
    #通用文字(高精度)  一天500次免费：https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic
    #网络图片(复杂背景)一天500次免费：https://aip.baidubce.com/rest/2.0/ocr/v1/webimage
    temp_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic' + '?access_token=' + access_token
    temp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    temp_file = open(r'D:\01工作资料\000数据脚本\log\vcode_pic\code60.png', 'rb')   #验证码文件夹位置
    temp_image = temp_file.read()
    temp_file.close()
    temp_data = {'image': base64.b64encode(temp_image)}
    temp_data = urllib.parse.urlencode(temp_data)
    temp_res = requests.post(url=temp_url, data=temp_data, headers=temp_headers)

    res = json.loads(str(temp_res.text))
    
    try:
        code = res['words_result'][0]['words'].strip().replace(' ','')
    except:
        code = 'retry'
        print('验证码重试ing')
    return code



#判断验证码是否正确，输入验证码后，如果出现错误，网页会提示，提示元素出现，返回1表示验证码输入错误；否则返回0验证码输入正确
def code_judge():
    try:
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/div')
        return 1
    except:
        print('验证码输入正确')
        return 0

#网站密码输入以及登录
def login_cpc():
    
    customerID = brower.find_element_by_xpath('//*[@id="CustomerId"]')
    customerName = brower.find_element_by_xpath('//*[@id="UserName"]')
    customerPassword = brower.find_element_by_xpath('//*[@id="PassWord"]')
    verify_code = brower.find_element_by_xpath('//*[@id="ValidateCode"]')
    
    customerID.clear()
    customerName.clear()  #清除用户名的字符
    customerPassword.clear()  #清除密码的字符
    customerID.send_keys('1')
    customerName.send_keys('XXXX')  #写入自己的账号，字符加引号
    customerPassword.send_keys('XXXX')    #写入自己的密码
    
    #验证码登录确认
    time.sleep(1)
    verify_code.clear()
    verify_code.send_keys(get_code())
    time.sleep(2)

    #此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
    while code_judge():
       verify_code.clear()
       brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
       verify_code.send_keys(get_code())
       time.sleep(2)
         

    login = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  #此处用click()不行，只能用submit提交
    time.sleep(10)
    print('网站已成功进入。。。')
    #广告活动页面的进入

    campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
    time.sleep(5)  #此网站较慢，暂停5s

# 广告初始的设定，进行活动页面，去除操作时间，修改时间
def cam_page_setting():
    
    WebDriverWait(brower, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]')))
    for i in range(100):
        if brower.find_element_by_xpath('//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]').get_attribute('aria-disabled') == 'false':
            print('页面成功')
            break
        else:
            time.sleep(2)
            print('等待中')
    
    print('广告活动页面加载成功')
    #去除操作时间
    time.sleep(1)
    above = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[2]/div/div[2]/div/div[2]/div/span/span/span/span/i[2]')
    ActionChains(brower).move_to_element(above).perform()
    time.sleep(1)
    operation_time_x = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[2]/div/div[2]/div/div[2]/div/span/span/span/span/i[1]').click()
    time.sleep(1)
    
    #选择过去7天
    date_category =brower.find_element_by_xpath ('//*[@id="activity"]/form/div[1]/div[1]/div/div[2]/div/div[2]/div/span/div/span/div/div/span/i').click()
    time.sleep(1)
    #日期下拉框的选择；定位日期中的自定义标签（li[9]）,过去7天li[7]）,过去30天li[8]），可自己修改
    date_customize = brower.find_element_by_xpath('//*[@style = "position: absolute; top: 0px; left: 0px; width: 100%;"]/div/div/div/ul/li[7]').click()
    #点击高级搜索的下拉框
    time.sleep(1)
    advance_search_box = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[2]/div/div[5]/span/a[1]/button').click()
    time.sleep(1)
    
    #选择是否关注
    # brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div/span/div/div/div/div').click()
    # brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div[1]/ul[1]/li[2]').click()   # 选择 否

#批量竞价的修改
def auto_change_budget():
    #高级搜索设定
    daily_budget_min = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[2]/div/div[1]/div/div[2]/div/span/span/div/div[1]/div/div[2]/input')
    daily_budget_min.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    daily_budget_min.send_keys(Keys.DELETE)
    daily_budget_min.send_keys(str(1.3))
    daily_budget_max = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[2]/div/div[1]/div/div[2]/div/span/span/div/div[3]/div/div[2]/input')
    daily_budget_max.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    daily_budget_max.send_keys(Keys.DELETE)
    daily_budget_max.send_keys(str(1.35))
    Acos_min = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[3]/div/div[4]/div/div[2]/div/span/span/div/div[1]/div/div[2]/input')
    Acos_min.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    Acos_min.send_keys(Keys.DELETE)
    Acos_min.send_keys(str(18))
    Acos_max = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[3]/div/div[4]/div/div[2]/div/span/span/div/div[3]/div/div[2]/input')
    Acos_max.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    Acos_max.send_keys(Keys.DELETE)
    Acos_max.send_keys(str(28))
    advance_search_click = brower.find_element_by_xpath('//*[@id="activity"]/form/div[1]/div[3]/div[4]/button[1]').click()
    time.sleep(10)  #此处只有20条，10s内加载完成
    
    #此处判断全选按钮是否是可选的 ，如果不可选为display ,返回结果值为false,可以用if  else判断    
    if brower.find_element_by_xpath('//*[@id="activity"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span/input').is_enabled():
    
    #如果广告活动栏网页加载完成，则该值为false,否则该值为true
    #brower.find_element_by_xpath('//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]').get_attribute('aria-disabled')
    
        #页面500条设置，
        js="var q=document.documentElement.scrollTop=100000"  
        brower.execute_script(js)
        time.sleep(2)       
        turn_page_box = brower.find_element_by_xpath('//*[@class = "ant-select-sm ant-pagination-options-size-changer ant-select ant-select-enabled"]/div/span').click()
        time.sleep(1.5)
        turn_page_500 = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-topLeft"]/div/ul/li[6]').click()
        
        time.sleep(2) #此处一定要有等待，待搜索后，全选框才会消失，下面是等待页面加载完成，全选框会出现；
        WebDriverWait(brower, 50).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="activity"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))
        print('切换页面到500条成功')
        
        #将页面返回到顶部位置
        js="var q=document.documentElement.scrollTop=0"  
        brower.execute_script(js)  
        
        total_num = int(brower.find_element_by_xpath('//*[@id="activity"]/div[1]/div/div/div/div[2]/div/div/ul/li[1]').text.split(' ')[1])
        actually_changed = 0
        
        print('正在修改预算中')
        for i in range(1,total_num+1):   #广告活动中的定位元素是从1开始
            get_spend_xpath = f'//*[@class = "ant-table-tbody"]/tr[{i}]/td[12]/div'
            get_spend = float(brower.find_element_by_xpath(get_spend_xpath).text.split(' ')[1])
            get_net_xpath = f'//*[@class = "ant-table-tbody"]/tr[{i}]/td[16]/div/div/div'
            get_net = brower.find_element_by_xpath(get_net_xpath).text
            if get_net == '-':
                get_net = 0
            else:
                get_net = float(get_net.split(' ')[1])
            
            if get_net >= get_spend * 1.5:
                change_pen_xpath = f'//*[@class = "ant-table-tbody"]/tr[{i}]/td[9]/div/i'
                change_pen_click = brower.find_element_by_xpath(change_pen_xpath).click()
                time.sleep(1)
                budget_xpath = f'//*[@class = "ant-table-tbody"]/tr[{i}]/td[9]/div/span/span/input'
                budget_location = brower.find_element_by_xpath(budget_xpath)
                budget_location.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
                budget_location.send_keys(Keys.DELETE)
                budget_location.send_keys(str(6))
                time.sleep(1)
                actually_changed += 1
                
            else:
                continue
        batch_change_budget_submit = brower.find_element_by_xpath('//*[@id="activity"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr[1]/th[9]/span/div/span[1]/div/button').click()
        time.sleep(10)
    else:
        print(' 无需要修改的预算')
        total_num = 0
        actually_changed = 0
        
    return total_num,actually_changed

login_cpc()
cam_page_setting()
record_log.loc[length,'总共条数'],record_log.loc[length,'实际调整'] = auto_change_budget()
record_log.to_excel(r"D:\01工作资料\000数据脚本\log\预算根据净利润调整.xlsx",index = False)
brower.quit()
print('预算修改完成，请在log日志中查看')


















