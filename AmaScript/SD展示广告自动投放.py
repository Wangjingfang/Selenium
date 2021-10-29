# -*- coding: utf-8 -*-
"""

脚本说明：采用selenium在CPC网站内自动化进行广告的投放:


"""

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
import warnings
warnings.filterwarnings('ignore')
import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings

warnings.filterwarnings('ignore')


def get_in_google():
    global brower
    # 要进入的网站
    url = 'http://888cpc.irobotbox.com/'

    # brower = webdriver.Chrome()

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=2560x1440')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

    # brower = webdriver.Chrome(ChromeDriverManager().install())
    brower = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    brower.get(url)
    print('CPC网页进入成功')
    brower.implicitly_wait(5)
    brower.maximize_window()  # 窗口最大化


def get_code():
    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    img.screenshot(r'D:\PycharmProjects\vode_pic\pictures.png')  # 验证码文件夹位置

    with open(r'D:\PycharmProjects\vode_pic\pictures.png', "rb") as f:
        b = f.read()
    text = sdk.predict(image_bytes=b)

    return text


# 判断验证码是否正确，输入验证码后，如果出现错误，网页会提示，提示元素出现，返回1表示验证码输入错误；否则返回0验证码输入正确
def code_judge():
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
    verify_code.send_keys(get_code())
    time.sleep(2)

    # 此处判断验证码正确否，若不正确，点击验证码图片进行刷新，并进行再次识别，识别后进行while再次判断；
    while code_judge():
        verify_code.clear()
        brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img').click()
        verify_code.send_keys(get_code())
        time.sleep(2)

    login = brower.find_element_by_xpath(
        '//*[@id="root"]/div/div[3]/form/div[5]/div/div/span/button').submit()  # 此处用click()不行，只能用submit提交
    time.sleep(10)
    print('网站已成功进入。。。')
    # SD广告活动页面的进入
    campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[8]/a').click()
    time.sleep(5)  # 此网站较慢，暂停5s


def create_sd_campagin(cam_info):


    for row in range(0, len(cam_info)):
        try:
            print('-' * 40)
            time.sleep(3)
            print('新一个广告创建中：')
            # 定位网页中创建广告元素的位置
            cam_create = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/main/div/div[2]/div/div[3]/div[1]/div[4]/button[1]').click()
            time.sleep(2)

            # 点击渠道下拉框
            cam_origin_path_down = brower.find_element_by_xpath('//*[@id="locale1"]/div[2]/div[1]/div[2]/div/span/span/span/span[1]/span').click()
            time.sleep(1)
            cam_origin_path = brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/span/span/input').send_keys(cam_info.loc[row,'渠道来源'])
            time.sleep(1.5)

            try:
                brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li/ul/li/span[2]/span')
                station_exist = True
            except:
                station_exist = False

            if station_exist:
                brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li/ul/li/span[2]/span').click()
                print('  站点已授权')
            else:
                print('  站点未授权')
                cam_info.loc[row, '投放结果'] = '站点未授权'
                brower.refresh()
                time.sleep(1)
                continue

            # 传入活动名称与预算
            cam_name = brower.find_element_by_xpath('//*[@id="locale1"]/div[2]/div[2]/div[2]/div/span/input').send_keys(cam_info.loc[row, '广告活动名'])
            time.sleep(1)
            cam_budget = brower.find_element_by_xpath('//*[@id="locale1"]/div[2]/div[4]/div[2]/div/span/div/div[2]/input')
            cam_budget.send_keys(Keys.CONTROL, 'a')  # 此处使用clear()失效，采用键盘功能进行全选后删除
            cam_budget.send_keys(Keys.DELETE)
            cam_budget.send_keys('3')


            cam_group_name = brower.find_element_by_xpath('//*[@id="locale2"]/div[2]/div/div[2]/div/span/input').click()
            cam_group_name = brower.find_element_by_xpath('//*[@id="locale2"]/div[2]/div/div[2]/div/span/input').send_keys(cam_info.loc[row,'SellSKU'])
            time.sleep(1)

            # 选择产品addlisting
            brower.find_element_by_xpath('//*[@class="addlisting"]/div/button').click()
            time.sleep(1)
            # 选择渠道SKU下拉框
            # choose_box = brower.find_element_by_xpath('//*[@id="locale4"]/div[2]/div/div/div/button/span').click()
            # input_asin = brower.find_element_by_xpath('//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(cam_info.loc[row,'ASIN'])

            clcik_ASIN_box = brower.find_element_by_xpath('//*[@title= "Asin"]').click()
            time.sleep(1)
            # 此处选择SKU非常难定位，先在console栏冻结网页网页，查看下拉结构中的SKU的位置，再通过xpath路径进行定位
            choose_sku = brower.find_element_by_xpath('//*[@class="ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div/ul/li[2]').click()

            input_SellSKU = brower.find_element_by_xpath('//*[@class="ant-col ant-col-16 ant-form-item-control-wrapper"]/div/span/div/div/textarea').click()
            input_SellSKU = brower.find_element_by_xpath('//*[@class="ant-col ant-col-16 ant-form-item-control-wrapper"]/div/span/div/div/textarea').send_keys(cam_info.loc[row, 'SellSKU'])
            time.sleep(1.5)
            ## '//*[@class = "ant-col ant-col-4"]/button//span'
            asin_search = brower.find_element_by_xpath('//*[@style = "margin-top: 3px; margin-left: 10px;"]').click()


            time.sleep(2)
            choose_all = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
            time.sleep(6)
            '''
            //*[starts-with(@style,"width: 600px; transform-origin: ")]/div/div[3]/div/button[2]
            //*[@style = "margin-top: 20px;"]/button[1]
            '''
            choose_confirm = brower.find_element_by_xpath('//span[contains(text(),"确 定")]/..').click()
            # //*[starts-with(@style,"width: 900px; transform-origin: ")]/div/div[2]/div/div/div/div[2]/button
            time.sleep(3)

            # 此处若有渠道SKU之前投放过广告，则会弹出确认框，没有投放过广告则不会弹出，需要做出判断
            try:
                brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-body-wrapper"]/div[2]/button[2]')
                done_targeting = True
            except:
                done_targeting = False

            if done_targeting:
                print('  渠道SKU选择成功')
                time.sleep(1)
                brower.find_element_by_xpath('//*[@class="ant-modal-confirm-body-wrapper"]/div[2]/button[2]').click()
            else:
                print('  第一次添加渠道SKU')
                cam_info.loc[row,'新渠道SKU'] ='第一次添加渠道SKU'

            time.sleep(2)

            print('  渠道SKU选择成功')

            # 输入竞价
            country = cam_info.loc[row,'渠道来源'][-2:]
            print(country)
            if country == 'US' or country == 'CA':
                cpc_input = 0.15
            elif country == 'UK' or country == 'DE' or country == 'FR':
                cpc_input = 0.12
            elif country == 'IT' or country == 'ES':
                cpc_input = 0.1
            elif country == 'JP':
                cpc_input = 12
            print(cpc_input)


            time.sleep(2)
            fill_cpc = brower.find_element_by_xpath('//*[@id="locale5"]/div[2]/div[3]/div[2]/div/span/span[1]/div/div[2]/input')
            fill_cpc.send_keys(Keys.CONTROL,'a')
            fill_cpc.send_keys(Keys.DELETE)
            fill_cpc.send_keys(str(cpc_input))
            # brower.find_element_by_xpath('//*[@id="locale5"]/div[2]/div[3]/div[2]/div/span/span[1]/div/div[2]/input').send_keys(cpc_input)
            print("  添加竞价")
            time.sleep(2)
            # "C:\Users\wangjingfang\Desktop\SDTG测试.xlsx"
            # 投放类目

            brower.find_element_by_xpath('//*[@id="locale7"]/div[2]/div[2]/div[2]/div/span/button').click()
            # 等待刷新时间比较长
            print(123)
            time.sleep(8)
            # '//*[@id="rcDialogTitle7"]/../../div[2]/div/div/div/div/div/div[2]/div/div/div/div/div/div/table/thead'
            choose_category = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
            time.sleep(3)
            choose_confirm = brower.find_element_by_xpath('//span[contains(text(),"确 定")]/..').click()
            time.sleep(4)


            # 保存并完成
            save_click = brower.find_element_by_xpath('//span[contains(text(),"保存并完成")]/..').click()
            cam_info.loc[row,'投放结果'] = '创建成功'
            cam_info.loc[row,'投放时间'] = datetime.date.today()
            # 此处等待时间也有点长
            time.sleep(10)

            brower.refresh()
            # 活动名称重复静态网页可以定位到，但实际运行时抓取不到，暂时不用
            try:
                # //*[@class="ant-message-custom-content ant-message-error"]
                brower.find_element_by_xpath('//span[contains(text(),"活动名称重复")]').click()
                print(456)
                error_exist = True

            except:
                error_exist = False

            if error_exist:
                cam_info.loc[row, '投放结果'] = '活动名称重复'
                print("已创建")
                time.sleep(2)
                brower.refresh()
            else:
                print("  创建成功")


        except:
            cam_info.loc[row, '投放结果'] = '莫名原因出错，待手动投放'
            print('  莫名原因出错，待手动投放')
            brower.refresh()
            time.sleep(3)

    return cam_info


def main(cam_info):

    get_in_google()

    get_code()

    code_judge()

    login_cpc()

    cam_info_result = create_sd_campagin(cam_info)  # 进行广告在CPC系统的自动化操作

    return cam_info_result

if __name__ == '__main__':

    cam_info = pd.read_excel(input('请输入要投放SD广告的excel：').replace('"', ''))
    print('正在进行读取数据中，请稍后')
    # cam_info['视频本地地址'] = cam_info['视频本地地址'].apply(lambda x: x.replace('\\', '/'))

    cam_info_result = main(cam_info)
    brower.quit()
    print('广告投放完毕，结果请在桌面上查看')
    cam_info_result.to_excel(r"C:\Users\wangjingfang\Desktop\SDTG测试次投放结果.xlsx", index=False)











