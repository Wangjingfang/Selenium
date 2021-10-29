#  UTF-8
"""
STEP 1 : 从158系统下载要创建自动广告的Excel表格，并做成在CPC系统自动开广告的文件内容格式
STEP 2 : 将整理好的自动开广告的文件自动在CPC平台创建

"""
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:58:04 2020

@author: Administrator
"""

"""
脚本说明：采用selenium在CPC网站内自动化进行广告的投放:

1.由于投放重复广告活动会出错（广告活动名称重复），这里采用try_finally，finally后刷新页面，除去以前未投放成功的历史记录；并记录好投放失败的SKU，未投放成功的SKU请手动补充；
2.验证码问题已解决，通过muggle_ocr包，但是目前识别率不是很高，后续可以手动让机器学习；
3.目前存在的问题：投放的SKU在CPC系统中搜不出，无法返回原因；  广告活动名称重复，无法返回原因； 合理的确认一个sleep等待时间；获取不到广告投放成功后的那个提示，message——info
4.CPC系统偶然出现突然很卡的时候，建建议不在整点以及某些时候投放；
5.由于自动化投放过程会出现各种偶然错误(主要由于网页加载问题，偶然出现加载不了)，针对出现的错误的广告活动进行再次投放，这里循环投放错误广告3次，失败的请手动确认（大概为渠道没有，或着sku搜索不出）；
6.注意158系统里面导出的FBA产品，在CPC系统里面可能搜索不到对应的渠道以及SellSKU，需要前期手动确认是否有该渠道，sellSKU暂无办法确认
"""

import AutoSPExcel as spfile
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
# import pytesseract
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from PIL import Image

import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')
#
# import muggle_ocr
# sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings

warnings.filterwarnings('ignore')

path = input('请输入要在CPC投放的广告的表格（已清理好的广告）：')

# 让程序无浏览器界面执行
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# #这里是重点，增加一个参数即可实现在不打开浏览器的情况下完成系列操作
# brower = webdriver.Chrome(chrome_options=option)
# brower.get(url)
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


# 判断验证码是否正确，输入验证码后，如果出现错误，网页会提示，提示元素出现，返回1表示验证码输入错误；否则返回0验证码输入正确
def code_judge(brower):
    try:
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/div')
        return 1
    except:
        print('验证码输入正确')
        return 0


# 网站密码输入以及登录
def login_cpc():
    customerID = brower.find_element_by_xpath('//*[@id="CustomerId"]')
    customerName = brower.find_element_by_xpath('//*[@id="UserName"]')
    customerPassword = brower.find_element_by_xpath('//*[@id="PassWord"]')
    verify_code = brower.find_element_by_xpath('//*[@id="ValidateCode"]')

    customerID.clear()
    customerName.clear()  # 清除用户名的字符
    customerPassword.clear()  # 清除密码的字符
    customerID.send_keys('1')
    customerName.send_keys('Admin62277')  # 写入自己的账号，字符加引号
    customerPassword.send_keys('P@ssw0rd123')  # 写入自己的密码

    # 验证码登录确认
    time.sleep(1)
    verify_code.clear()
    verify_code.send_keys(get_code(brower, sdk))
    time.sleep(2)

    # 此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
    while code_judge(brower):
        verify_code.clear()
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
        verify_code.send_keys(get_code(brower, sdk))
        time.sleep(2)

    login = brower.find_element_by_xpath(
        '//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  # 此处用click()不行，只能用submit提交
    time.sleep(10)
    print('网站已成功进入。。。')
    # 广告活动页面的进入
    campaign_page = brower.find_element_by_xpath(
        '//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
    time.sleep(5)  # 此网站较慢，暂停5s

begin = time.time()
# 进入CPC网站，注意其中验证码需要自己手动填写
#要进入的网站
url = 'http://888cpc.irobotbox.com/'
brower = webdriver.Chrome(ChromeDriverManager().install())
# brower = webdriver.Chrome()
# brower.get(url)
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

print('正在登陆CPC网站，请稍后：')
login_cpc()
"""
# 从muggle_ocr识别验证码
# def get_code(brower,sdk):
#    brower.save_screenshot('vode_pic/pictures.png')
#    page_snap_obj = Image.open('vode_pic/pictures.png')
#
#    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
#    time.sleep(2)
#    #location = img.location
#    size = img.size
#    left = 2112   #location['x']
#    top = 723     #location['y']
#    right = left + size['width'] + 20
#    bottom = top + size['height'] + 20
#    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
#    #image_obj.show()  # 打开切割后的完整验证码
#
#    image_obj.save('vode_pic/code.png')
#
#    with open('vode_pic/code.png', "rb") as f:
#        b = f.read()
#    text = sdk.predict(image_bytes=b)
#    return text
#
##判断验证码是否正确，输入验证码后，如果出现错误，网页会提示，提示元素出现，返回1表示验证码输入错误；否则返回0验证码输入正确
# def code_judge(brower):
#     try:
#         brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/div')
#         return 1
#     except:
#         print('验证码输入正确')
#         return 0
# 
# 
# # 网站密码输入以及登录
# customerID = brower.find_element_by_xpath('//*[@id="CustomerId"]')
# customerName = brower.find_element_by_xpath('//*[@id="UserName"]')
# customerPassword = brower.find_element_by_xpath('//*[@id="PassWord"]')
# verify_code = brower.find_element_by_xpath('//*[@id="ValidateCode"]')
# 
# customerID.clear()
# customerName.clear()  # 清除用户名的字符
# customerPassword.clear()  # 清除密码的字符
# customerID.send_keys('1')
# customerName.send_keys('Admin62277')  # 写入自己的账号，字符加引号
# customerPassword.send_keys('P@ssw0rd123')  # 写入自己的密码
# # 第一次刷新验证码
# i = 1
# while i <= 3:
#     brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
#     i = i + 1
# 
# print('请输入在网页中看见的验证码：')
# code = input('请输入在网页中看见的验证码：')
# verify_code.send_keys(code)
# login = brower.find_element_by_xpath(
#     '//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  # 此处用click()不行，只能用submit提交
# time.sleep(10)
# if  code_judge(brower) == 1:
#     verify_code.clear()
#     code = input('请再次输入在网页中看见的验证码：')
#     verify_code.send_keys(code)
#     login = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  # 此处用click()不行，只能用submit提交
#     time.sleep(10)
# else:
#     login = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  #此处用click()不行，只能用submit提交
#     time.sleep(10)


# code_judge(brower):
#    verify_code.clear()
#    code = input('请输入在网页中看见的验证码：')
#    verify_code.send_keys(code)


# 验证码登录确认
# time.sleep(1)
# verify_code.clear()
# verify_code.send_keys(get_code(brower,sdk))
# time.sleep(2)
#
##此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
# while code_judge(brower):
#   verify_code.clear()
#   brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
#   verify_code.send_keys(get_code(brower,sdk))
#   time.sleep(2)
#
"""

# 广告活动页面的进入
campaign_page = brower.find_element_by_xpath(
    '//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
time.sleep(5)  # 此网站较慢，暂停5s


def cpc_targeting(campaign_name, long_station, group_name, SellSKU, budget, bid):
    # 定位网页中创建广告元素的位置
    cam_create = brower.find_element_by_xpath('//*[@id="activity"]/form/div[2]/button[1]').click()

    time.sleep(3)
    cam_origin_path = brower.find_element_by_xpath(
        '//*[@id="module-one-item-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').click()
    # cam_origin_path = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').click()
    time.sleep(1)

    # 定位来源渠道的位置，由于动态网页，位置经常出现变化，这里采用xpath模糊匹配定位
    brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/span/span/input').send_keys(long_station)
    time.sleep(1)
    # 输入站点渠道后，对出现值进行点击,此处较难定位
    brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li/ul/li/span[2]/span').click()
    # cam_origin_path_choose = brower.find_element_by_xpath('//*[@id="rc-tree-select-list_7"]/ul/li/ul/li/span[2]/span').click()
    # select = Select(brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/span/span/input'))
    # select.select_by_value('Amazon-Z01075-US')
    # cam_origin_path = brower.find_element_by_link_text('来源渠道').click()
    # brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').send_keys('Amazon-Z01075-US')

    cam_name = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[2]/div[2]/div/span/input')
    cam_name.send_keys(Keys.CONTROL, 'a')  # 此处使用clear()失效，采用键盘功能进行全选后删除
    cam_name.send_keys(Keys.DELETE)
    cam_name.send_keys(campaign_name)
    cam_budget = brower.find_element_by_xpath(
        '//*[@id="module-one-item-one"]/div/div[2]/div[4]/div[2]/div/span/div/div[2]/input')
    cam_budget.send_keys(Keys.CONTROL, 'a')  # 此处使用clear()失效，采用键盘功能进行全选后删除
    cam_budget.send_keys(Keys.DELETE)
    cam_budget.send_keys(str(budget))  # 直接传入数字会出错，需要传入字符串
    cam_adgroup_name = brower.find_element_by_xpath(
        '//*[@id="module-two-item-one"]/div/div[2]/div[1]/div[2]/div/span/input')
    cam_adgroup_name.send_keys(Keys.CONTROL, 'a')  # 此处使用clear()失效，采用键盘功能进行全选后删除
    cam_adgroup_name.send_keys(Keys.DELETE)
    cam_adgroup_name.send_keys(group_name)
    time.sleep(1)

    # 进入listing选择页面 ---  添加listing
    WebDriverWait(brower, 15).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button')))
    cam_add_sku = brower.find_element_by_xpath(
        '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()  # 添加listing
    time.sleep(1)
    cam_add_sku = brower.find_element_by_xpath(
        '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()
    time.sleep(1)
    # 将输入ASIN切换成输入SKU
    clcik_ASIN_box = brower.find_element_by_xpath('//*[@title= "Asin"]').click()
    time.sleep(1)
    # 此处选择SKU非常难定位，先在console栏冻结网页网页，查看下拉结构中的SKU的位置，再通过xpath路径进行定位
    choose_sku = brower.find_element_by_xpath(
        '//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div[1]/ul[1]/li[2]').click()
    time.sleep(1)
    input_sku = brower.find_element_by_xpath(
        '//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(SellSKU)
    time.sleep(1)
    search_confirm = brower.find_element_by_xpath('//*[@style = "margin-top: 3px; margin-left: 10px;"]').click()
    time.sleep(2)
    # check_sku = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
    # time.sleep(2)

    check_sku = brower.find_element_by_xpath(
        '//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
    time.sleep(1)

    ensure_sku = brower.find_element_by_xpath('//*[@style = "margin-top: 20px;"]/button[1]').click()
    time.sleep(4)

    # 对于新品，SKU之前未投放广告的，没有再次确认框，需要先判断是否有该弹出框；
    try:

        ensure_again_sku = brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]').click()
    except:
        print('    存在唯一的SKU，不需要确认')

    # 定位竞价位置，并输入竞价
    cam_bid = brower.find_element_by_xpath(
        '//*[@id="module-two-item-two"]/div/div[2]/div[2]/div[2]/div/span/div/span[2]/input').send_keys(str(bid))
    ## ('// *[ @ id = "module-two-item-two"] / div / div[2] / div[2] / div[2] / div / span / div / span[2] / input')
    cam_save_done = brower.find_element_by_xpath(
        '//*[@class = "antd-pro-pages-advertisementmanagement-css-activityadd-bottom_group"]/button').click()
    # WebDriverWait(brower, 30).until(ec.visibility_of_element_located((By.XPATH, '//*[@class = "ant-message-custom-content ant-message-success"]/span')))
    WebDriverWait(brower, 15).until(ec.visibility_of_element_located((By.XPATH, '//*[@class = "ant-message-custom-content ant-message-success"]/span')))
    # 获取成功的路径2    /html/body/div[6]/div/span/div/div/div/span
    # "//*[@id="time1617781447764"]/div/div[2]/div/div[2]/button"
    # "//*[@id="time1617781447764"]/div/div[2]"
    # "//*[@id="time1617782262980"]/div/div[2]/div/div[2]/button/span/i"
    # "/html/body/div[11]/div/div[2]/div/div[2]/button/span/i"
    # time.sleep(1)
    # WebDriverWait(brower, 500).until(ec.presence_of_element_located((By.XPATH, '//*[@class = "ant-modal-confirm-btns"]/button')))
    time.sleep(3)
    anywhereclick = brower.find_element_by_xpath('//*[@id="activity"]/form/div[2]/button[1]').click()
    # anywhereclick = brower.find_element_by_xpath("//*[@id="activity"]/form/div[1]/div[2]/div/div[6]/div/div[2]/div/span/button[1]").click()
    # create_suceess_verifty = brower.find_element_by_xpath('/html/body/div[11]/div/div[2]/div/div[2]/button/span/i').click()
    print(' 打印屏幕显示内容：创建成功')

    result = brower.find_element_by_xpath('/html/body/div[11]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div').text

    return result


# 将要投放的广告信息设置为函数，可多次引用和调入
# 需要一个原始读入表格，一个原始表格汇总记录表格，一个筛选出错误的表格再次投放
def targeting_record(cam_pending, cam_result_current):
    for i in range(0, len(cam_pending)):
        campaign_name = cam_pending.loc[i, '广告活动']
        long_station = cam_pending.loc[i, '渠道来源']
        group_name = cam_pending.loc[i, '广告组名称']
        SellSKU = cam_pending.loc[i, 'SellSKU']
        budget = cam_pending.loc[i, 'budget']
        bid = cam_pending.loc[i, 'bid']
        print('正在批量投放广告中，请稍后:')

        try:
            return_result = cpc_targeting(campaign_name, long_station, group_name, SellSKU, budget, bid)
            targeting_result = '投放成功'
            error_reason = 'no_error'
        except:
            print('投放失败')
            targeting_result = '投放失败'
            error_reason = '网页定位错误,待重复投放'
            brower.refresh()

        time.sleep(2)
        cam_result_current.loc[i, '投放结果'] = targeting_result
        cam_result_current.loc[i, '错误原因'] = error_reason
    return cam_result_current


# 读取要投放的广告活动名；请按照站点，广告活动，广告组名称，SKU，预算，竞价等表格信息
if '"' in path:
    path = path.replace('"', '')

os.chdir(os.path.dirname(path))

cam_origin_data = pd.read_excel(path)
cam_origin = pd.read_excel(path)
print('网站已成功进入。。。')

cam_result_total = pd.DataFrame()

# 提取投放失败的sku,进行循环再次投放至三次，若三次后还失败，请手动检查；最后一次循环中保留了投放失败的sku,且total报告中含有所有的sku的投放结果
for i in range(0, 3):
    cam_result_current = pd.DataFrame()
    cam_result_current = cam_origin.copy(deep=True)
    cam_result = targeting_record(cam_origin, cam_result_current)
    cam_result = cam_result.reset_index(drop=True)
    cam_origin = cam_result[cam_result['投放结果'] == '投放失败']
    cam_origin = cam_origin.reset_index(drop=True)
    cam_result_total = pd.concat([cam_result_total, cam_result])
    cam_result_total = cam_result_total.reset_index(drop=True)
    # 此处是删除掉汇总表格中的投放失败的结果，在循环中下次记录投放的结果，且最后一次的结果不删除，留待手动处理
    if i < 2:
        cam_result_total = cam_result_total[~cam_result_total['投放结果'].isin(['投放失败'])]
    else:
        pass

brower.quit()
# 退出浏览器

# 将投放的结果写入Excel的第二个sheet中，免得再次生成多个表格
writer = pd.ExcelWriter(path)
cam_origin_data.to_excel(writer, '原始数据', index=False)
cam_result_total.to_excel(writer, '投放结果_广告活动', index=False)
writer.save()

print('请在文件下查看投放结果，系统未投放的，请手动投放!')
end = time.time()
spend_time = int(end - begin) / 3600
print('总共花费时间%d小时' % round(spend_time, 2))
















