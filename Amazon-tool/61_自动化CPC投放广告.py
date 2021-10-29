# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:58:04 2020

@author: Administrator
"""

"""
脚本说明：
1.验证码段：请修改好对应存放图片的路径；以及验证码在图片中的定位点（left & top），需要根据自己的计算机确定；
2.程序的执行保持在主界面上：其他页面可以覆盖它，但是不能最小化它，最小化后失败率大大提升；
3.已实现无浏览器界面的投放

源码逻辑： -- 待修改
def main():  
    读入源文件
    识别验证码
    登录进入CPC（包含验证码出错的解决）
    投放广告的基本流程
    依次投放广告及出错原因的汇总
    循环投放出错广告（返回最终投放的全部结果）

"""

import os
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image

print('请输入要在CPC投放的广告的表格（已清理好的广告）：')
path = input('excel路径：')

import muggle_ocr
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

import warnings
warnings.filterwarnings('ignore')

#从muggle_ocr识别验证码
def get_code(brower,sdk):
    brower.save_screenshot('vode_pic/pictures.png')
    page_snap_obj = Image.open('vode_pic/pictures.png')
    
    img = brower.find_element_by_xpath('//*[@id="root"]/div/div[3]/form/div[4]/div/div/span/span/img')
    time.sleep(2)
    #location = img.location
    size = img.size
    left = 2092 #2112   #location['x']  后面的数值2112为显示浏览界面时验证码的定位位置，前面的数值2092为隐藏浏览器界面时验证码的定位位置
    top = 805 #723     #location['y']
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


#要进入的网站
url = 'http://888cpc.irobotbox.com/'
# brower = webdriver.Chrome()
# brower.get(url)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=2560x1440')  #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
brower=webdriver.Chrome(chrome_options=chrome_options)

brower.get(url)
print('CPC网页进入成功')
brower.implicitly_wait(5)
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
customerPassword.send_keys('XXXX')    #写入自己的密码

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
print('网站已成功进入。。。')
#广告活动页面的进入
campaign_page = brower.find_element_by_xpath('//*[@id="root"]/div/section/section/header/div/div/div[1]/div[2]/ul/li[4]/a').click()
time.sleep(5)  #此网站较慢，暂停5s

def cpc_targeting(campaign_name,long_station,group_name,SellSKU,budget,bid):

    #定位网页中创建广告元素的位置
    cam_create = brower.find_element_by_xpath('//*[@id="activity"]/form/div[2]/button[1]').click()
    
    time.sleep(3)
    cam_origin_path = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').click()
    #cam_origin_path = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[1]/div[2]/div/span/div/span/span/span[1]/span').click()
    time.sleep(1)
    
    #定位来源渠道的位置，由于动态网页，位置经常出现变化，这里采用xpath模糊匹配定位
    brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/span/span/input').send_keys(long_station)
    time.sleep(1)
    #输入站点渠道后，对出现值进行点击,此处较难定位
    brower.find_element_by_xpath('//*[starts-with(@id,"rc-tree-select-list_")]/ul/li/ul/li/span[2]/span').click()
    
    cam_name = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[2]/div[2]/div/span/input')
    cam_name.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    cam_name.send_keys(Keys.DELETE)
    cam_name.send_keys(campaign_name)
    cam_budget = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[4]/div[2]/div/span/div/div[2]/input')
    cam_budget.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    cam_budget.send_keys(Keys.DELETE)
    cam_budget.send_keys(str(budget)) # 直接传入数字会出错，需要传入字符串
    cam_adgroup_name = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[1]/div[2]/div/span/input')
    cam_adgroup_name.send_keys(Keys.CONTROL, 'a') #此处使用clear()失效，采用键盘功能进行全选后删除
    cam_adgroup_name.send_keys(Keys.DELETE)
    cam_adgroup_name.send_keys(group_name)
    time.sleep(1)
    
    #进入listing选择页面 ---  添加listing
    WebDriverWait(brower, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button')))
    cam_add_sku = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()  #添加listing
    time.sleep(1)
    cam_add_sku = brower.find_element_by_xpath('//*[@id="module-two-item-one"]/div/div[2]/div[2]/div/div[1]/button').click()
    time.sleep(1)
    # 将输入ASIN切换成输入SKU
    clcik_ASIN_box = brower.find_element_by_xpath('//*[@title= "Asin"]').click()
    time.sleep(1)
    #此处选择SKU非常难定位，先在console栏冻结网页网页，查看下拉结构中的SKU的位置，再通过xpath路径进行定位
    choose_sku = brower.find_element_by_xpath('//*[@class = "ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft"]/div[1]/ul[1]/li[2]').click()
    time.sleep(1)
    input_sku = brower.find_element_by_xpath('//*[@class ="ant-col ant-col-20"]/div[1]/div[2]/div[1]/span[1]/div[1]/div[1]/textarea').send_keys(SellSKU)
    time.sleep(2)
    search_confirm = brower.find_element_by_xpath('//*[@style = "margin-top: 3px; margin-left: 10px;"]').click()
    time.sleep(2)
    # check_sku = brower.find_element_by_xpath('//*[@class = "ant-table-header ant-table-hide-scrollbar"]/table[1]/thead/tr/th/span/div/span/div/label/span/input').click()
    # time.sleep(2)
    try:
        error = 0
        WebDriverWait(brower, 4).until(ec.visibility_of_element_located((By.XPATH, '//*[@style = "max-height: 600px; overflow-y: scroll;"]/table/tbody/tr/td/span/label/span')))
        check_sku = brower.find_element_by_xpath('//*[@style = "max-height: 600px; overflow-y: scroll;"]/table/tbody/tr/td/span/label/span').click()
              
    except:
        brower.refresh()
        error =  "SKU无法选中，CPC未授权SKU"
    else:
        time.sleep(1)
        #print('  程序在执行首个确认框')
        # 此处确认栏，确定框有个span,但是对span进行点击会出现无效，一定要对span上一层button进行点击，后续的确定都是此性质
        ensure_sku = brower.find_element_by_xpath('//*[@style = "margin-top: 20px;"]/button[1]').click()
        time.sleep(4)
        
        #对于新品，SKU之前未投放广告的，没有再次确认框，需要先判断是否有该弹出框；
        try:
            #brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]')
            #print('  程序在确认SKU是否唯一')
            ensure_again_sku = brower.find_element_by_xpath('//*[@class = "ant-modal-confirm-btns"]/button[2]').click()
            time.sleep(1)
        except:
            print('    存在唯一的SKU，不需要确认')
            
        finally:    
         # 定位竞价位置，并输入竞价
            #print('  程序在输入竞价')
            cam_bid = brower.find_element_by_xpath('//*[@id="module-two-item-two"]/div/div[2]/div[2]/div[2]/div/span/div/span[2]/input').send_keys(str(bid))
            time.sleep(1)
            #判断广告活动框是否为空，若出现广告活动活动重复，则广告活动框会自动删除变成空值
            cam_repeat_judge = brower.find_element_by_xpath('//*[@id="module-one-item-one"]/div/div[2]/div[2]/div[2]/div/span/input').get_attribute('value')
            # print('  获取广告活动值成功')
            time.sleep(1)
            if cam_repeat_judge == '':
                error = '广告活动名称重复'
                # print('  广告活动重复')
            else:
                error = 0
                # print('  广告活动输入正常')
                           
            if error:
                brower.refresh()
                # print('  广告活动重复，刷新页面中')
            else:    
            #广告活动创建的确认
                # print('  广告活动名称正常')
                cam_save_done = brower.find_element_by_xpath('//*[@class = "antd-pro-pages-advertisementmanagement-css-activityadd-bottom_group"]/button').click()
                time.sleep(1)
                WebDriverWait(brower, 30).until(ec.visibility_of_element_located((By.XPATH, '//*[@class = "ant-message-custom-content ant-message-success"]/span')))
                #获取成功的路径2    /html/body/div[6]/div/span/div/div/div/span
                error = brower.find_element_by_xpath('//*[@class = "ant-message-custom-content ant-message-success"]/span').text

    
    print('  这是函数返回结果:%s'%error)
    return error
 
#需要一个原始读入表格，一个原始表格汇总记录表格，一个筛选出错误的表格再次投放
def targeting_record(cam_pending,cam_result_current):
    for i in range(0,len(cam_pending)):
        campaign_name = cam_pending.loc[i,'广告活动']
        long_station = cam_pending.loc[i,'渠道来源']
        group_name = cam_pending.loc[i,'广告组名称']
        SellSKU = cam_pending.loc[i,'SellSKU']
        budget = cam_pending.loc[i,'budget']
        bid = cam_pending.loc[i,'bid']
        print('正在批量投放广告中，请稍后:')
        
        try:
            return_result = cpc_targeting(campaign_name,long_station,group_name,SellSKU,budget,bid)
            print('  投放执行成功')
        except:
            print('  投放失败')
            return_result = '投放失败'
            brower.refresh()            
 
        if return_result == 'SKU无法选中，CPC未授权SKU':
           targeting_result = '投放出现问题'
           print('  SKU无法选中，CPC未授权SKU')
           error_reason = return_result

           
        elif return_result == '广告活动名称重复':
           targeting_result = '投放出现问题'
           print('  广告活动名称重复')
           error_reason = return_result
          
        elif return_result == '创建成功':
            targeting_result = '投放成功'
            print('  投放成功')
            error_reason = 'no_error'
                        
        # except Exception as e:       
        elif return_result == '投放失败':
            targeting_result = '投放失败'
            error_reason = '网页定位错误,待重复投放'
            print('  出现网页定位错误，待重复投放；')
            
        time.sleep(2)    
        cam_result_current.loc[i,'投放结果'] = targeting_result
        cam_result_current.loc[i,'错误原因'] = error_reason
    return cam_result_current

#读取要投放的广告活动名；请按照站点，广告活动，广告组名称，SKU，预算，竞价等表格信息
if '"' in path:
    path = path.replace('"','')

os.chdir(os.path.dirname(path))  

#cam_158_data = pd.read_excel(path,sheet_name ='原始数据158导出数据')
cam_origin_data = pd.read_excel(path,sheet_name = '待上传CPC广告文件')
cam_origin = pd.read_excel(path,sheet_name = '待上传CPC广告文件')
cam_result_total = pd.DataFrame()

#提取投放失败的sku,进行循环再次投放至三次，若三次后还失败，请手动检查；最后一次循环中保留了投放失败的sku,且total报告中含有所有的sku的投放结果
for i in range(0,3):
    cam_result_current = pd.DataFrame()
    cam_result_current = cam_origin.copy(deep = True)
    cam_result = targeting_record(cam_origin, cam_result_current)
    cam_result = cam_result.reset_index(drop=True)
    cam_origin = cam_result[cam_result['投放结果'] == '投放失败' ]
    cam_origin = cam_origin.reset_index(drop=True)
    cam_result_total = pd.concat([cam_result_total,cam_result])
    cam_result_total = cam_result_total.reset_index(drop=True)
    #此处是删除掉汇总表格中的投放失败的结果，在循环中下次记录投放的结果，且最后一次的结果不删除，留待手动处理
    if i < 2:
        cam_result_total=cam_result_total[~cam_result_total['投放结果'].isin(['投放失败'])]
    else:
        pass

#退出浏览器    
brower.quit()

#将投放的结果写入Excel的第二个sheet中，免得再次生成多个表格
writer = pd.ExcelWriter(path)
#cam_158_data.to_excel(writer,'原始数据158导出数据',index = False)
cam_origin_data.to_excel(writer,'原始数据',index = False)
cam_result_total.to_excel(writer,'投放结果_广告活动',index = False)
writer.save()
print('请在原文件下查看投放结果，系统未投放的，请手动投放!')

