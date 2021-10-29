# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:45:26 2020

@author: Administrator
"""
'''
想法：主要对批量广告中的广告组进行批量调价，由于数量居多，每页只能500条，所以采用程序进行修改;
此脚本有时执行的好，有时又会出现异常，暂时不再调节，待用时再整理
'''
import os
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image

import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')
brower = webdriver.Chrome()
brower.implicitly_wait(5)

#从muggle_ocr识别验证码
def get_code():
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
def code_judge():
    try:
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/div')
        return 1
    except:
        print('验证码输入正确')
        return 0
    
def login_cpc():
    url = 'http://cpc.irobotbox.com/'
    brower.get(url)
    brower.maximize_window()  #窗口最大化
    
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
    print('网站登录成功')
    
#进入广告活动-进行广告组
def get_in_group():
    campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
    WebDriverWait(brower, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]')))
    for i in range(100):
        if brower.find_element_by_xpath('//*[@class = "ant-tabs-nav ant-tabs-nav-animated"]/div/div[1]').get_attribute('aria-disabled') == 'false':
            print('广告组页面加载成功')
            break
        else:
            time.sleep(2)
            print('等待中')
    
    time.sleep(2)
    #进入广告组页面
    ad_group = brower.find_element_by_xpath('/html/body/div/div/section/section/main/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[3]').click()
    time.sleep(2)
    WebDriverWait(brower, 100).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))

    print('广告组成功进入')
    
#对广告组进行设置，去除操作时间，竞价设置，广告活动输入，修改每页为500等等；
def group_setting(pending_campaign,origin_bid):
#去除更新时间
    above = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[2]/div/div[2]/div/span/span/span/span/i[2]')
    ActionChains(brower).move_to_element(above).perform()
    time.sleep(1)
    operation_time_x = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[2]/div/div[2]/div/span/span/span/span/i[1]').click()
    time.sleep(2)
    
    campaign_halloween = pending_campaign
    
    filter_max_bid = str(origin_bid)  #第一次修改为0.04
    
    #选择国家页面，这里选择US+CA+EU五国，其余不选；
    origin_station = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[1]/div/div[1]/div/div[2]/div/span/span/span/span').click()
    time.sleep(2)
    us_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[1]/span[2]/span').click()
    ca_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[2]/span[2]/span').click()
    uk_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[4]/span[2]/span').click()
    de_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[6]/span[2]/span').click()
    fr_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[5]/span[2]/span').click()
    it_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[7]/span[2]/span').click()
    es_choose = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li[8]/span[2]/span').click()
       
    #进入批量搜索，设置批量搜索的广告活动
    time.sleep(1)
    batch_search = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[5]/span/a[3]/button').click()
    time.sleep(1)
    batch_search_condition_box = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[6]/div/div[2]/div/span/div/div/span/i').click()
    time.sleep(1)
    batch_search_condition_campaign_name = brower.find_element_by_xpath('//*[@style = "width: 120px; left: 111px; top: 294px;"]/div/ul/li[2]').click()
    time.sleep(1)
    input_batch_search_condition_campaign_name = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[6]/div/div[2]/div/span/textarea').send_keys(campaign_halloween)
    # batch_search_verifty = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[6]/div/div[2]/div/span/button[1]').click()
    
    #进入高级搜索，并设置搜索的竞价
    time.sleep(1)
    advance_search = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[2]/div/div[5]/span/a[1]/button').click()
    time.sleep(1)
    default_bid_max = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[3]/div[2]/div/div[5]/div/div[2]/div/span/span/div/div[3]/div/div[2]/input').send_keys(filter_max_bid)
    time.sleep(1)
    advance_search_verifty = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[3]/div[4]/button[1]').click()
    time.sleep(2)
    #等待高级搜索结果
    WebDriverWait(brower, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))


    #设置翻页等功能,先将搜索的结果翻到最底层
    js="var q=document.documentElement.scrollTop=100000"  
    brower.execute_script(js)
    time.sleep(2) 
    #获取总的广告组条数 
    total_group_num = brower.find_element_by_xpath('//*[@id="group"]/div[1]/div/div/div/div[2]/div/div/ul/li[1]').text.split(' ')[1]
    print('总共要修改竞价的广告组数量：%s'%total_group_num)
    #计算需要翻页的次数
    #turn_page_time = int(total_group_num)//500 + 1
    #设置为500页每条
    turn_page_box = brower.find_element_by_xpath('//*[@class = "ant-pagination-options-size-changer ant-select ant-select-enabled"]/div/span/i').click()
    time.sleep(2)
    turn_page_500 = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-topLeft"]/div/ul/li[6]').click()
    time.sleep(2)
    #等待翻页为500条后数据加载完成
    WebDriverWait(brower, 300).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))

    print('广告组设置完成')
    
#全选广告组，进行批量调价
def batch_group_bid(add_price):
    #将进度条拉倒最顶部
    js="var q=document.documentElement.scrollTop=0"  
    brower.execute_script(js)
    time.sleep(2) 
    print('正在修改竞价中：')
    choose_all_box = brower.find_element_by_xpath('//*[@id="group"]/div[1]/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span').click()
    time.sleep(5)
    #批量操作
    WebDriverWait(brower, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="group"]/form/div[2]/button[2]')))
    # bulk_operation_box = brower.find_element_by_xpath('//*[@id="group"]/form/div[2]/button[2]').click()
    # time.sleep(1)
    bulk_operation_box_above = brower.find_element_by_xpath('//*[@id="group"]/form/div[2]/button[2]')
    ActionChains(brower).move_to_element(bulk_operation_box_above).perform()
    time.sleep(2)
    
    bulk_change_default_bid = brower.find_element_by_xpath('//*[@class = "ant-dropdown ant-dropdown-placement-bottomLeft"]/ul/li[6]').click()
    time.sleep(3)
    change_bid_value = brower.find_element_by_xpath('//*[@class = "ant-row-flex ant-row-flex-start"]/div[3]/span/div/div[2]/input')
    change_bid_value.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    change_bid_value.send_keys(Keys.DELETE)
    change_bid_value.send_keys(str(add_price))
    time.sleep(1)
    change_bid_value_confirm = brower.find_element_by_xpath('//*[@class = "ant-modal-footer"]/div/button[2]').click()
    time.sleep(5)
    WebDriverWait(brower, 500).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-modal-confirm-btns"]/button')))
    time.sleep(5)
    change_suceess_verifty = brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button').click()
    
    #等待最终显示的条数可以点击为止
    #WebDriverWait(brower, 300).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="group"]/form/div[1]/div[3]/div[4]/button[1]')))
    #WebDriverWait(brower, 300).until(ec.presence_of_element_located((By.XPATH, '//*[@id="group"]/div[1]/div/div/div/div[2]/div/div/ul/li[1]')))
    time.sleep(10)
    WebDriverWait(brower, 300).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))

    print('竞价修改完成，进行下次修改中')

#
def loop_change_bid(add_price):
    #读取是否还存在的修改竞价的全选框，若存在返回1，不存在返回0，并给while做循环判断；
    if brower.find_element_by_xpath('//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span/input').is_enabled():
        error = 1
    else:
        error = 0
        
    
    #循环修改广告组竞价，当广告组全部修改完成后    
    while error:
        try:
            batch_group_bid(add_price)
            print(' 竞价批量修改成功')
        except:
            print(' 竞价批量修改失败')
            try:
                #如果存在竞价批量修改页面，那么则点击取消按钮，回归正常页面
                cancel_adjust_bid = brower.find_element_by_xpath('//*[@class = "ant-modal-footer"]/div/button[1]').click()
            except:
                pass
            finally:
                #最后重新广告组调价页面，点击重新搜索页面，待页面加载完成，继续执行batch_group_bid函数进行竞价的修改
                WebDriverWait(brower, 300).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))
                advance_search_verifty = brower.find_element_by_xpath('//*[@id="group"]/form/div[1]/div[3]/div[4]/button[1]').click()
                time.sleep(2)
                WebDriverWait(brower, 300).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="group"]/div/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span')))
                print(' 已重新高级搜索，')

    print('竞价已全部修改完成！')        
  
def main(campaign_halloween,origin_bid,add_price):
    login_cpc()
    get_in_group()
    group_setting(campaign_halloween,origin_bid)
    loop_change_bid(add_price)

if __name__ == "__main__":
    campaign_halloween = '''
075-MX-2020_万圣节
075-UK-2020_万圣节
075-US-2020_万圣节
088-DE-2020_万圣节
088-ES-2020_万圣节
088-FR-2020_万圣节
088-IT-2020_万圣节
088-JP-2020_万圣节
088-UK-2020_万圣节
096-CA-2020_万圣节
096-DE-2020_万圣节
096-ES-2020_万圣节
096-FR-2020_万圣节
096-IT-2020_万圣节
096-MX-2020_万圣节
096-UK-2020_万圣节
096-US-2020_万圣节
'''
    main(campaign_halloween,0.05,0.01)

