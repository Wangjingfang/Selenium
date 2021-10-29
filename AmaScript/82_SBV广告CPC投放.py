# -*- coding: utf-8 -*-
"""
Created on Fri May 14 14:58:12 2021

@author: Administrator
"""
'''
# 此脚本的目的主要是为了 自动化操作SBV系统，进行广告的自动上传  - 20210514
需要读入的原表的列：渠道来源，广告活动名称，品牌，ASIN，SellSKU ,视频本地地址
'''

import re
import requests,json,base64,urllib
import os,time,datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.webdriver.chrome.options import Options

import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')


def get_in_google():
    global brower
    #要进入的网站
    url = 'http://888cpc.irobotbox.com/'
    brower = webdriver.Chrome(ChromeDriverManager().install())

    # brower = webdriver.Chrome()
    
    # chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
    # chrome_options.add_argument('window-size=2560x1440')  #指定浏览器分辨率
    # chrome_options.add_argument('--disable-gpu')  #谷歌文档提到需要加上这个属性来规避bug
    # chrome_options.add_argument('--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    # brower=webdriver.Chrome(chrome_options=chrome_options)
    
    brower.get(url)
    print('CPC网页进入成功')
    brower.implicitly_wait(5)
    brower.maximize_window()  #窗口最大化
'''
def get_code():

    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    img.screenshot(r'D:\01工作资料\000数据脚本\log\vcode_pic\code81.png')#验证码文件夹位置

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
    temp_file = open(r'D:\01工作资料\000数据脚本\log\vcode_pic\code81.png', 'rb')   #验证码文件夹位置
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
'''

# 从muggle_ocr识别验证码
def get_code(brower, sdk):
    brower.save_screenshot(r'D:\PycharmProjects\vode_pic\pictures.png')
    page_snap_obj = Image.open(r'D:\PycharmProjects\vode_pic\pictures.png')

    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    time.sleep(2)
    # location = img.location
    size = img.size
    left = 2090  # 2112  2092 #location['x']  后面的数值2112为显示浏览界面时验证码的定位位置，前面的数值2092为隐藏浏览器界面时验证码的定位位置
    top = 730  # 723  805   #location['y']
    right = left + size['width']
    bottom = top + size['height']
    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    # image_obj.show()  # 打开切割后的完整验证码

    image_obj.save(r'D:\PycharmProjects\vode_pic\code.png')

    with open(r'D:\PycharmProjects\vode_pic\code.png', "rb") as f:
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
    customerName.send_keys('Admin62277')  #写入自己的账号，字符加引号
    customerPassword.send_keys('P@ssw0rd123')    #写入自己的密码
    
    #验证码登录确认
    time.sleep(1)
    verify_code.clear()
    verify_code.send_keys(get_code(brower,sdk))
    time.sleep(2)
    
    #此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
    while code_judge():
       verify_code.clear()
       brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
       verify_code.send_keys(get_code(brower,sdk))
       time.sleep(2)
         
    
    login = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  #此处用click()不行，只能用submit提交
    time.sleep(10)
    print('网站已成功进入。。。')
    #SBV广告活动页面的进入
    campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[6]/a').click()
    time.sleep(5)  #此网站较慢，暂停5s


def create_sbv_campaign(cam_info):
    for row in range(0,len(cam_info)):
        # 创建广告页面
        creative_campaign = brower.find_element_by_xpath('//*[@id="sbactivity"]/div[1]/span[1]/button').click()
        time.sleep(2)
        
        # 点击渠道下拉框
        brower.find_element_by_xpath('//*[@id="module-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').click()
        brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/span/span/input').send_keys(cam_info.loc[row,'渠道来源'])
        time.sleep(1)
        brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li/ul/li/span[2]/span').click()
        
        # 传入活动名称与预算
        brower.find_element_by_xpath('//*[@id="register_Name"]').send_keys(cam_info.loc[row,'广告活动名称'])
        brower.find_element_by_xpath('//*[@id="register_Budget"]').send_keys('10')
        
        # 获取品牌，此处较复杂
        brower.find_element_by_xpath('//*[@id="register_BrandEntityId"]/a').click()  #刷新品牌，即点击从品牌获取数据
        time.sleep(4)
        brower.find_element_by_xpath('//*[@id="register_BrandEntityId"]/div/div/div').click()
        
        brand_name_path = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown-menu  ant-select-dropdown-menu-root ant-select-dropdown-menu-vertical"]')
        brand_list_url = brand_name_path.get_attribute("outerHTML")   #获取此段html断码，以字符串形式存储
        
        brand_lis = brand_list_url.split('</li>')
        brand_list = list()
        for i in range(0,len(brand_lis)-1):
            brand_list.append(brand_lis[i].split('none;">')[1])
        
        brand = cam_info.loc[row,'品牌']
        
        for i in range(0,len(brand_list)):
            if brand.upper() == brand_list[i].upper():
                print('品牌已在广告系统中授权')
                break
        else:   # 如果品牌不在该品牌的范围内，直接结束当前循环，关闭当前网页创建页面，继续下一个循环
            cam_info.loc[row,'投放结果'] = '品牌未授权到广告系统'
            close_create_page = brower.find_element_by_xpath('//*[@class = "ant-modal-close-x"]/i').click()
            time.sleep(2)
            continue
        
        time.sleep(1)
        choose_brand = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown-menu  ant-select-dropdown-menu-root ant-select-dropdown-menu-vertical"]/li[{}]'.format(i + 1)).click()  
        time.sleep(1)
        
        # 选择视频投放
        choose_video = brower.find_element_by_xpath('//*[@id="register_CreativeType"]/label[2]/span[1]/input').click()
        time.sleep(1)
        
        # 添加listing，这个改为选择  在线的SellSKU
        add_listing = brower.find_element_by_xpath('//*[@id="module-two"]/div/div[2]/div/div[2]/div/span/div/div/div[1]/button').click()
                
        time.sleep(1)
        
        #input_asin = brower.find_element_by_xpath('//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(cam_info.loc[row,'ASIN'])
        
        clcik_ASIN_box = brower.find_element_by_xpath('//*[@title= "Asin"]').click()
        time.sleep(1)
        #此处选择SKU非常难定位，先在console栏冻结网页网页，查看下拉结构中的SKU的位置，再通过xpath路径进行定位
        choose_sku = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div[1]/ul[1]/li[2]').click()

        input_SellSKU = brower.find_element_by_xpath('//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(cam_info.loc[row,'SellSKU'])
        
        time.sleep(1)
        asin_search = brower.find_element_by_xpath('//*[@style = "margin-top: 3px; margin-left: 10px;"]').click()
        time.sleep(2)
        choose_all = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
        time.sleep(1)
        choose_confirm = brower.find_element_by_xpath('//*[@style = "margin-top: 20px;"]/button[1]').click()
        time.sleep(2)
        choose_confirm_ensure = brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]').click()
        time.sleep(2)
        
        # 上传视频页面  地址格式："C:/Users/Administrator/Desktop/缝纫机-广告版-2.mp4"
        brower.find_element_by_xpath('//*[@id="register_VideoMediaIds"]').send_keys(cam_info.loc[row,'视频本地地址'])        
        time.sleep(10) # 视频上传比较慢，先等待10s
        
        # 选择推荐关键词，先判断是否有推荐关键词，若有，则选择推荐关键词，没有的话，随便输入一个关键词，做好记录
        '''  注释掉的部分为先选择推荐关键词，推荐关键词没有的话，手动随便添加一个关键词
        brower.find_element_by_xpath('//*[@id = "module-fife"]/div/div[2]/span/div/div[2]/div/span/button').click()
        time.sleep(5)
        
        try:
            brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table/thead/tr/th/span/div/span/div/label/span/input')
            keyword_exist = 1
        except:
            keyword_exist = 0
            

        if keyword_exist:  #存在推荐关键词，选择10个
            choose_all = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table/thead/tr/th/span/div/span/div/label/span/input').click()
            time.sleep(3)
            choose_confirm = brower.find_element_by_xpath('//*[starts-with@aria-labelledby, "rcDialogTitle"]/div/div[2]/div[3]/div/button[2]').click()
            time.sleep(3)
        
                    # 修改每个关键词的竞价到 US-0.25  CA-EU-0.15
            for i in range(0,10):
                keyword_path = brower.find_element_by_xpath('//*[@data-row-key = "{}"]/td[3]/div/div/div[2]/input'.format(i))
                keyword_path.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
                keyword_path.send_keys(Keys.DELETE)
                if cam_info.loc[row,'渠道来源'][-2:] == 'US':
                    bid = 0.25
                else:
                    bid = 0.15
                keyword_path.send_keys(str(bid))
                time.sleep(2)
                
            cam_info.loc[row,'关键词信息'] = 10
                
        else:   #手动随便补充一个关键词如，test，竞价给0.25，后续补充新值后会关闭
            suppose_word_close = brower.find_element_by_xpath('').click()
            time.sleep(2)
            self_word = brower.find_element_by_xpath('//*[@id = "module-fife"]/div/div[2]/span/div[2]/div[2]/div/span/button').click()
            time.sleep(2)
            self_word = brower.find_element_by_xpath('//*[@class = "ant-col ant-col-19 ant-form-item-control-wrapper"]/div/span/textarea').send_keys('test')
            time.sleep(2)
            ensure = brower.find_element_by_xpath('//*[@style = "margin-top: 20px; text-align: right;"]/button').click()
            time.sleep(2)
            
            cam_info.loc[row,'关键词信息'] = '关键词为test'        
        '''
        
        # 这里用作测试，直接进行 手动随便添加一个关键词
        self_word = brower.find_element_by_xpath('//*[@id = "module-fife"]/div/div[2]/span/div[2]/div[2]/div/span/button').click()
        time.sleep(2)
        self_word = brower.find_element_by_xpath('//*[@class = "ant-col ant-col-19 ant-form-item-control-wrapper"]/div/span/textarea').send_keys('test')
        time.sleep(2)
        ensure = brower.find_element_by_xpath('//*[@style = "margin-top: 20px; text-align: right;"]/button').click()
        time.sleep(2)
        
        keyword_path = brower.find_element_by_xpath('//*[@data-row-key = "0"]/td[3]/div/div/div[2]/input')
        keyword_path.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
        keyword_path.send_keys(Keys.DELETE)
        if cam_info.loc[row,'渠道来源'][-2:] == 'US':
            bid = 0.25
        else:
            bid = 0.15
        keyword_path.send_keys(str(bid))
        time.sleep(2)
        
        cam_info.loc[row,'关键词信息'] = '关键词为test'   
        
        
        time.sleep(30)
        save_submit = brower.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()  # 提交“保存并提交”,
        time.sleep(5)
        for i in range(0,20):
                        
            #判断是否由于广告名称重复的原因出错
            try:
                brower.find_element_by_xpath("/html/body/div[9]/div/div[2]/div/div[2]/div/div/div[1]/span")
                error_exist = True
            except:
                error_exist = False
                
            if error_exist:
                print('广告活动名称重复，已忽略')
                cam_info.loc[row,'投放结果'] = '广告活动名称重复'
                brower.refresh()
                continue
            else:
                print('正常')

            #判断保存按钮是否存在，存在为1，说明视频未上传成功
            try:   
                brower.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]')
                submit_exist = True
            except:
                submit_exist = False
                
            if submit_exist:
                time.sleep(2)
                save_submit = brower.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
                time.sleep(5)
            else:
                cam_info.loc[row,'投放结果'] = '提交成功'
                break
                   
        time.sleep(5)
        print('广告投放成功，待下一个投放中')
    
    return cam_info
                

def main(cam_info):
    
    get_in_google()
    
    get_code(brower,sdk)

    code_judge()
    
    login_cpc()
    
    cam_info_result = create_sbv_campaign(cam_info) #进行广告在CPC系统的自动化操作
    
    return cam_info_result
    
if __name__ == '__main__':
    
    cam_info = pd.read_excel(input('请输入要投放SBV广告的excel：').replace('"',''))   
    print('正在进行读取数据中，请稍后')
    cam_info['视频本地地址'] = cam_info['视频本地地址'].apply(lambda x:x.replace('\\','/'))
    
    cam_info_result = main(cam_info)
    brower.quit()
    print('广告投放完毕，结果请在桌面上查看')
    cam_info_result.to_excel(r'C:\Users\Administrator\Desktop\SBV投放结果.xlsx',index = False)
    
    
    