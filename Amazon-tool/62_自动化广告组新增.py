# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:58:04 2020

@author: Administrator
"""

"""
脚本说明：采用selenium在CPC网站内自动化进行广告的投放:
# 当相同广告活动出现在不同渠道时，会出现由于选择上的错误，此处暂时未解决；    

"""


import os
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')


print('请输入要在CPC投放的广告的表格（已清理好的广告）：')
path = input('路径：')

begin = time.time()
#进入CPC网站，注意其中验证码需要自己手动填写
url = 'http://cpc.irobotbox.com/'
brower = webdriver.Chrome()
brower.implicitly_wait(5)
brower.get(url)
brower.maximize_window()  #窗口最大化

#从muggle_ocr识别验证码
def get_code(brower,sdk):
    brower.save_screenshot('vode_pic/pictures.png')
    page_snap_obj = Image.open('vode_pic/pictures.png')
    
    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    time.sleep(2)
    #location = img.location
    size = img.size
    left = 2112   #location['x']
    top = 723     #location['y']
    right = left + size['width'] + 20
    bottom = top + size['height'] + 20
    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    #image_obj.show()  # 打开切割后的完整验证码
    
    image_obj.save('vode_pic/code.png')
    
    with open('vode_pic/code.png', "rb") as f:
        b = f.read()
    text = sdk.predict(image_bytes=b)
    return text

#判断验证码是否正确，输入验证码后，如果出现错误，网页会提示，提示元素出现，返回1表示验证码输入错误；否则返回0验证码输入正确
def code_judge(brower):
    try:
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/div')
        return 1
    except:
        print('验证码输入正确')
        return 0

#网站密码输入以及登录
customerID = brower.find_element_by_xpath('//*[@id="CustomerId"]')
customerName = brower.find_element_by_xpath('//*[@id="UserName"]')
customerPassword = brower.find_element_by_xpath('//*[@id="PassWord"]')
verify_code = brower.find_element_by_xpath('//*[@id="ValidateCode"]')

customerID.clear()
customerName.clear()  #清除用户名的字符
customerPassword.clear()  #清除密码的字符
customerID.send_keys('1')
customerName.send_keys('XXX')  #写入自己的账号，字符加引号
customerPassword.send_keys('XXX')    #写入自己的密码

#验证码登录确认
time.sleep(1)
verify_code.clear()
verify_code.send_keys(get_code(brower,sdk))
time.sleep(2)

#此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
while code_judge(brower):
   verify_code.clear()
   brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
   verify_code.send_keys(get_code(brower,sdk))
   time.sleep(2)
     

login = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  #此处用click()不行，只能用submit提交
time.sleep(10)

#广告活动页面的进入
campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
WebDriverWait(brower, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]')))
for i in range(100):
    if brower.find_element_by_xpath('//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]').get_attribute('aria-disabled') == 'false':
        print('广告活动页面加载成功')
        break
    else:
        time.sleep(2)
        print('广告活动页面等待加载中')
time.sleep(2)
ad_group = brower.find_element_by_xpath('/html/body/div/div/section/section/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[3]').click()
time.sleep(2)

def cpc_group_targeting(campaign_name,group_name,SellSKU,bid):

    create_ad_group = brower.find_element_by_xpath('//*[@id="group"]/form/div[2]/button[1]').click()  
    time.sleep(2)
    input_campaign_name = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div/div/div/div/div[1]').click()
    time.sleep(1)
    input_campaign_name = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div/div/div/div/div[2]/div/input').send_keys(campaign_name)
    time.sleep(1)  #此处搜索可能时间可能较长
    #当出现相同名称的广告活动对应多个渠道时，这里选择就会出错，暂时无解决办法，若出错则渠道sku选择错误，若不出错，则证明选择错误
    WebDriverWait(brower, 8).until(ec.visibility_of_element_located((By.XPATH, '//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft "]/div[1]/ul/li')))
    choose_campaign_name = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft "]/div[1]/ul/li').click()
    
    ad_group_name = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[1]/div[2]/div/span/input').send_keys(group_name)
    
    #添加渠道SKU,跟广告活动的路径基本一致；
    WebDriverWait(brower, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button')))
    cam_add_sku = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()  #添加listing
    time.sleep(2)
    WebDriverWait(brower, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button')))
    cam_add_sku = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()
    time.sleep(1)

    clcik_ASIN_box = brower.find_element_by_xpath('//*[@title= "Asin"]').click()
    time.sleep(1)    
    choose_sku = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div[1]/ul[1]/li[2]').click()
    time.sleep(1)
    input_sku = brower.find_element_by_xpath('//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(SellSKU)
    time.sleep(1)
    search_confirm = brower.find_element_by_xpath('//*[@style = "margin-top: 3px; margin-left: 10px;"]').click()
    time.sleep(3)
    check_sku = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
    time.sleep(2)
    
    
    ensure_sku = brower.find_element_by_xpath('//*[@style = "margin-top: 20px;"]/button[1]').click()
    time.sleep(3)

    try:
        #brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]')
        ensure_again_sku = brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]').click()
    except:
        print('   存在唯一的SKU，不需要确认')
    
    time.sleep(1)
    bid = brower.find_element_by_xpath('//*[@id="module-two-item-two"]/div/div[2]/div/div[2]/div/span/div/span[1]/input').send_keys(str(bid))
    time.sleep(1)
    save_and_quit = brower.find_element_by_xpath('//*[@class = "ant-form ant-form-horizontal ant-form-hide-required-mark stepForm"]/div/div[2]/button').click()
    WebDriverWait(brower, 30).until(ec.visibility_of_element_located((By.XPATH, '//*[@class = "ant-message-custom-content ant-message-success"]/span')))
    error = brower.find_element_by_xpath('//*[@class = "ant-message-custom-content ant-message-success"]/span').text
    time.sleep(2)
    
    return error
#读取要投放的广告活动名；请输入广告活动，广告组名称，SellSKU，bid等表格信息

if '"' in path:
    path = path.replace('"','')

os.chdir(os.path.dirname(path))  

cam_sheet = pd.read_excel(path)
print('网站已成功进入。。。')

cam_sheet_result = pd.DataFrame()
cam_sheet_result = cam_sheet.copy(deep = True)

for i in range(0,len(cam_sheet)):
    campaign_name = cam_sheet.loc[i,'广告活动']
    group_name = cam_sheet.loc[i,'广告组名称']
    SellSKU = cam_sheet.loc[i,'SellSKU']
    bid = cam_sheet.loc[i,'bid']
    print('正在批量投放广告组中，请稍后:')
    try:
        error = cpc_group_targeting(campaign_name,group_name,SellSKU,bid)
        targeting_result = error 
        print(' 投放成功')
    except Exception as e:
        print(' 投放失败')
        brower.refresh()
        WebDriverWait(brower, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]')))
        for i in range(100):
            if brower.find_element_by_xpath('//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]').get_attribute('aria-disabled') == 'false':
                print(' 广告活动页面加载成功')
                break
            else:
                time.sleep(2)
                print(' 广告活动页面等待加载中')
        time.sleep(2)        
        ad_group = brower.find_element_by_xpath('/html/body/div/div/section/section/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[3]').click() #再次进入广告组页面
        targeting_result = '投放失败:' + str(e)
           
    cam_sheet_result.loc[i,'投放结果'] = targeting_result
    
    time.sleep(5)

brower.quit()
writer = pd.ExcelWriter(path)
cam_sheet.to_excel(writer,'原始数据',index = False)
cam_sheet_result.to_excel(writer,'投放结果_广告组',index = False)
writer.save()
print('请在看投放结果，系统投放出现问题的，请手动投放!')

