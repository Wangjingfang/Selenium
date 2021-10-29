# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:58:04 2020

@author: Administrator
"""

"""
脚本说明：SBV的关键词位置的竞价修改; 增加一个实际调整的数量actual_changed = 0，用于记录实际调整的数量；
在投放位置，设置好条件：spend>2；对Acos和花费进行判断，再进行调整，20210426时间，总条数为147条，数据量可以接受
定义全局变量global：brower,将浏览器头写入函数中，已测试成功；

目前问题：
1.CPC系统的SB位置没有操作记录时间以及排序，导致无法使用，已反馈给赛盒 -3.20
update20210320 排序和修改竞价函数未修改完成，其他均已修改完成，待赛盒修改后，在更新此脚本

update-20210426
由于没有操作时间，调整的逻辑改为 对CPC和竞价的判断，当前大量数据表明SBV采用的是fixed竞价，那么若Acos高或者，花费多，将采用CPC与bid的值进行比较，下降幅度以0.05为基础单位；
将排序函数，暂时注释掉；
注意US的最低竞价为0.25，EU 国家的最低竞价为0.15，需要增加国家字段的判断，若当前已经为最低竞价(仍满足当前的调整条件的话)，那么需要停用当前的搜索词；其余根据逻辑值进行判断；

update-20210427
今天脚本能运行成功，日志能成功生成，但是仍存在一些问题，待后续更正；
第265行，选择“停用”关键词，定位一直出现错误，当前通过try,except方法来避免，后续待解决；
目前的竞价逻辑中，仍然存在一些问题，待仔细优化；主要是：最近调过的，如何避免再次调整；（初步想法是在竞价第二位小数位以日期来进行标记，后续待解决）
当前的调整逻辑中，也有一些遗落，由于时间太紧，暂时只用于五一期间SBV的关键词调整，待后续再完善；

update-20210508
赛盒CPC系统已更新搜索词位置上的操作日志，可以根据日志排序后，计算需要调整的条数来进行调整； --测试成功
"""
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
    # url = "http://94.74.123.132"
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

# 从muggle_ocr识别验证码
def get_code():
    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    img.screenshot(r'D:\PycharmProjects\vode_pic\pictures.png')  # 验证码文件夹位置
    time.sleep(2)
    with open(r'D:\PycharmProjects\vode_pic\pictures.png', "rb") as f:
        b = f.read()
    text = sdk.predict(image_bytes=b)

    return text
'''
def get_code(brower, sdk):
    brower.save_screenshot(r'D:\PycharmProjects\vode_pic\pictures.png')
    page_snap_obj = Image.open(r'D:\PycharmProjects\vode_pic\pictures.png')

    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    time.sleep(2)
    # location = img.location
    size = img.size
    left = 2090  # 2090  2092 #location['x']  后面的数值2112为显示浏览界面时验证码的定位位置，前面的数值2092为隐藏浏览器界面时验证码的定位位置
    top = 730  # 730  805   #location['y']
    right = left + size['width']
    bottom = top + size['height']
    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    # image_obj.show()  # 打开切割后的完整验证码

    image_obj.save(r'D:\PycharmProjects\vode_pic\code.png')

    with open(r'D:\PycharmProjects\vode_pic\code.png', "rb") as f:
        b = f.read()
    text = sdk.predict(image_bytes=b)
    return text
'''


# def get_code():
#
#     img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
#     img.screenshot(r'D:\01工作资料\000数据脚本\log\vcode_pic\code81.png')#验证码文件夹位置
#
#     API_Key = 'hhLeDihbTyG64wke7Tp1W8XL'               #你的key
#     Secret_Key = 'yIuO5HEXzyZwcST2isT0idK7AYeH8VXd'    #你的秘钥
#     # 获取token
#     res = requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_Key + '&client_secret=' + Secret_Key)
#     res = json.loads(str(res.text))
#     access_token = res['access_token']
#     #传输百度API
#     #通用文字(高精度)  一天500次免费：https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic
#     #网络图片(复杂背景)一天500次免费：https://aip.baidubce.com/rest/2.0/ocr/v1/webimage
#     temp_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic' + '?access_token=' + access_token
#     temp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     temp_file = open(r'D:\01工作资料\000数据脚本\log\vcode_pic\code81.png', 'rb')   #验证码文件夹位置
#     temp_image = temp_file.read()
#     temp_file.close()
#     temp_data = {'image': base64.b64encode(temp_image)}
#     temp_data = urllib.parse.urlencode(temp_data)
#     temp_res = requests.post(url=temp_url, data=temp_data, headers=temp_headers)
#
#     res = json.loads(str(temp_res.text))
#
#     try:
#         code = res['words_result'][0]['words'].strip().replace(' ','')
#     except:
#         code = 'retry'
#         print('验证码重试ing')
#     return code

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
    campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[6]/a').click()
    time.sleep(5)  #此网站较慢，暂停5s

#进入广广告活动页面设置，以及在投放位置的设置；
def setting_keyword():

    #去除操作时间
    time.sleep(1)
    above = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[1]/div[8]/div[2]/div/span/span/span/i[2]')
    ActionChains(brower).move_to_element(above).perform()
    time.sleep(1)
    operation_time_x = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[1]/div[8]/div[2]/div/span/span/span/i[1]').click()
    time.sleep(1)
    
    #选择过去7天
    date_category =brower.find_element_by_xpath ('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[1]/div[2]/div[2]/div/span/div/span/div/div/span/i').click()
    time.sleep(1)
    #日期下拉框的选择；定位日期中的自定义标签（li[9]）,过去7天li[7]）,过去30天li[8]），可自己修改
    date_customize = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown-menu  ant-select-dropdown-menu-root ant-select-dropdown-menu-vertical"]/li[9]').click()
    time.sleep(1)

    # 进入搜索词位置
    keyword = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]').click()
    time.sleep(10)
  
#进行高级设置
def setting_advance_search():
    # 进入高级搜索
    advance_search_box = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[1]/div[10]/div/div/span/button[3]').click()
    time.sleep(1)
    
    #输入spend大于2的
    spend_min = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[2]/div[13]/div[2]/div/span/span/div/div[1]/div/div[2]/input').send_keys(2)
    #order_max = brower.find_element_by_xpath('//*[@id="targeting"]/form/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div/span/span/div/div[3]/div/div[2]/input').send_keys(5)
    time.sleep(2)

    #进行高级搜索
    advance_search_click = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/form[2]/div[16]/div/div/span/button[1]').click()
    #WebDriverWait(brower, 60).until(ec.invisibility_of_element_located((By.XPATH,'//*[@id="targeting"]/div[1]/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/div/label/span/input')))
    time.sleep(10)

#进行日期排序        
def sort_desc_date():
    time.sleep(3)
    js="var q=document.documentElement.scrollTop=0"  
    brower.execute_script(js)
    #进行两次排序，对操作时间先降序，再升序,
    #重大疑问：为什么是ec.invisibility  等待元素不可见才能测试成功，排序成功后还需要再等待几秒，再能进行再次排序
    time.sleep(20)
    sort_1 = brower.find_element_by_xpath('//*[@class="ant-table-thead"]/tr/th[21]/span/div/span[1]/div').click()
    
    WebDriverWait(brower, 90).until(ec.invisibility_of_element_located((By.XPATH,'//*[@id="sbkeyword"]/div[2]/div/div/div/div/div/div/div/div/table/thead/tr[1]/th[1]/span/div/span[1]/div/label/span/input')))
    time.sleep(60)
    sort_2 = brower.find_element_by_xpath('//*[@class="ant-table-thead"]/tr/th[21]/span/div/span[2]/div').click()
    WebDriverWait(brower, 90).until(ec.invisibility_of_element_located((By.XPATH,'//*[@id="sbkeyword"]/div[2]/div/div/div/div/div/div/div/div/table/thead/tr[1]/th[1]/span/div/span[1]/div/label/span/input')))
    time.sleep(10)

#进行500条翻页
def turn_500_page():
    #翻页500页，此处莫名其妙的容易出现报错，设置一个try except,当出现报错的时候进行重复最多5次
    time.sleep(5)
    js="var q=document.documentElement.scrollTop=100000"  
    brower.execute_script(js)
    time.sleep(10)

    turn_page_box = brower.find_element_by_xpath('//*[@class="ant-select-sm ant-pagination-options-size-changer ant-select ant-select-enabled"]/div').click()
    time.sleep(1)  #此处间隔时间越短越好，终于调试出来了
    turn_page_500 = brower.find_element_by_xpath('//*[@style="position: absolute; top: 0px; left: 0px; width: 100%;"]/div/div/div/ul/li[6]').click()

    time.sleep(15)
    
#这里最多修改500条，不足500条的时候会进行判断找到最符合的日期值（比当前日期小4天的最大日期值，并获得该定位）
def get_pending_num(page_n):
    
    if page_n > 500:
        n = 499
    else:
        n = page_n - 1
                
    x = 1
    # id = "sbkeyword"
    while x:
        pending_judge_time = brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('//*[@data-row-key = "{}"]/td[21]/div/div'.format(n)).text.split(' ')[0]
        if len(pending_judge_time) == 0:
            x = 0 
        else:
            pending_judge_time = datetime.datetime.strptime(pending_judge_time,'%Y-%m-%d')
            if pending_judge_time + datetime.timedelta(days = 7) > datetime.datetime.today() and n > 1:
                n = n - 1
                x = 1
            else:
                x = 0
    
    return n  #返回的值比实际条数少一条，由于起始值为0开头的

#一条条修改竞价
def change_bid_func():
    time.sleep(2)
    total_num = int(brower.find_element_by_xpath('//*[@class="ant-pagination ant-table-pagination mini"]/li[1]').text.split(' ')[1])
    print('正在计算需要调整的条数，请稍后：')
    total_change_num = get_pending_num(total_num)
    record_log.loc[length,'待修改'] = total_change_num
    print('需要修改的竞价位置的条数有：%s条'%total_change_num)
    print('正在修改竞价中：请稍后')
    actully_changed = 0
    if total_change_num > 0:
        for i in range(0,total_change_num):
            #注意此处直接在find_xpath中找不到对应的格式化字符串，只有先将xpath路径格式化后（传入参数i），再送入查询才能找到该值
            get_country = get_country = brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[3]/div/div[2]'.format(i)).text[-2:]
            
            get_bid = float(brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[7]/div/div/div/div/div/a'.format(i)).text.split(' ')[1])
            
            get_CPC = float(brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[12]/div'.format(i)).text)
            
            get_spend = float(brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[10]/div'.format(i)).text.split(' ')[1])
            
            get_acos = brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[16]/div'.format(i)).text
            
            if get_acos == '-':
                get_acos = 1000
            else:
                get_acos = float(get_acos.split('%')[0])/100
            
            try:
                # 对Acos小于26%的搜索词不调整
                if get_acos < 0.26:
                    continue
                
                elif get_acos == 1000:
                    if get_country in ['US','CA']:
                        if get_bid <= 0.25:  #将关键词暂停
                            pause_keyword_pen = brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[6]/div/div/div/div/div'.format(i)).click()
                            time.sleep(1.5)
                            pause_keyword = brower.find_element_by_xpath('/html/body/div[3]').find_element_by_xpath('.//*[@role = "listbox"]/li[2]').click()
                            time.sleep(1)
                            continue
                        else:
                            adjust_bid = 0.25
                            
                        if round(adjust_bid,2) < 0.25:
                            adjust_bid = 0.25
                    
                    else:
                        if get_bid >= get_CPC:
                            adjust_bid = get_CPC - 0.1
                        else:
                            continue
                        
                        if round(adjust_bid,2) < 0.15:
                            adjust_bid = 0.15
               
                
                else:  # 正常的Acos高的广告的调整
                    if get_country in ['US','CA']:
                        if get_bid >= get_CPC:
                            adjust_bid = get_CPC - 0.1
                        else:
                            adjust_bid = get_bid * 0.8
                    
                        if round(adjust_bid,2) < 0.25:
                            adjust_bid = 0.25
                    
                    else:  # EU国家的竞价
                        if get_bid >= get_CPC:
                            adjust_bid = get_CPC - 0.1
                        else:
                            adjust_bid = get_bid * 0.8
                            
                        if round(adjust_bid,2) < 0.15:
                            adjust_bid = 0.15
               
                adjust_bid = round(adjust_bid,2)            
                # '//*[@id = "sbkeyword"]'
                change_bid_ico = brower.find_element_by_xpath('//*[@id = "root"]').find_element_by_xpath('.//*[@data-row-key="{}"]/td[7]/div/div/div/div/div/i'.format(i)).click()
                time.sleep(2)
             
                bid_value = brower.find_element_by_xpath('//*[@class = "ant-popover ant-popover-placement-rightBottom"]/div/div[2]/div/div/div/div/span/div/div[2]/input')
                bid_value.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
                bid_value.send_keys(Keys.DELETE)
                time.sleep(1)
                bid_value.send_keys(str(adjust_bid))
                click_sure = brower.find_element_by_xpath('//*[@class = "ant-popover ant-popover-placement-rightBottom"]/div/div[2]/div/div/div[2]/button[2]').click()
                time.sleep(2)
                
            except:
                continue
              
            actully_changed = i  #记录当前修改的条数
                
        time.sleep(2)
        print('竞价修改完成，请在Excel中查看')
        brower.quit()
    else:
        print('当前无需需要修改的SBV的关键词竞价') 
    return actully_changed

def main():
    
    print('打开google浏览器中')
    get_in_google()
    
    print('正在登陆CPC网站，请稍后：')
    login_cpc()
    
    print('正在进行投放位置的页面设置，请稍后：')
    setting_keyword()
    
    print('正在进行高级设置，请稍后：')
    setting_advance_search()
    
    print('正在排序中，请稍后：')    
    sort_desc_date()
    
    print('正在切换页面到500条，请稍后：')
    turn_500_page()

    print('正在修改竞价中，请稍后：')
    actully_changed = change_bid_func()
    
    return actully_changed
       
if __name__ == '__main__':
    record_log = pd.read_excel(r"D:\坚果云\我的坚果云\log\SBV关键词位置竞价调整记录-Acos30.xlsx")
    length = len(record_log)
    record_log.loc[length,'调整日期'] = time.strftime("%m-%d", time.localtime())
    record_log.loc[length,'开始时间'] = time.strftime("%H:%M:%S", time.localtime())
    
    actully_changed = main()
    brower.quit()
    
    record_log.loc[length,'已修改'] = actully_changed
    record_log.loc[length,'结束时间'] = time.strftime("%H:%M:%S", time.localtime())
    record_log.to_excel(r"D:\坚果云\我的坚果云\log\SBV关键词位置竞价调整记录-Acos30.xlsx",index = False)


