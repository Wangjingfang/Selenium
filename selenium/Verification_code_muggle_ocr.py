'''
使用指北
注意: 因模块过新，阿里/清华等第三方源可能尚未更新镜像，因此手动指定使用境外源，为了提高依赖的安装速度，可预先自行安装依赖：tensorflow/numpy/opencv-python/pillow/pyyaml

pip install muggle-ocr

作者：后山小鲨鱼
链接：https://www.jianshu.com/p/1e6430b1c4d7
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''
'''
SDK类参数
参数名	必选	类型	说明
model_type	No	ModelType	指定预置模型类型
conf_path	No	str	指定自定义模型yaml配置文件（绝对路径）
'''
# 1\. 导入包

import muggle_ocr
import time

"""
使用预置模型，预置模型包含了[ModelType.OCR, ModelType.Captcha] 两种
其中 ModelType.OCR 用于识别普通印刷文本, ModelType.Captcha 用于识别4-6位简单英数验证码

"""


# 打开印刷文本图片
with open(r"muggle-test1.jpg","rb") as f:
    ocr_bytes = f.read()

# 打开验证码图片
with open(r"muggle-test2.jpg","rb") as f:
    captcha_bytes = f.read()

# 2\.初始化；model_type 可选：[ModelTyoe.OCR,ModelType.Captcha]
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)

# ModelType.ocr 可识别光学印刷文本
for i in range(5):
    st = time.time()
    # 3\. 调用预测函数
    text = sdk.predict(image_bytes=ocr_bytes)
    print(text,time.time() - st)

# ModelType.Captcha 可识别4-6位验证码
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
for i in range(5):
    st = time.time()
    # 3\. 调用预测函数
    text = sdk.predict(image_bytes=captcha_bytes)
    print(text, time.time() - st )

"""
使用自定义模型
支持基于 https://github.com/kerlomz/captcha_trainer 框架训练的模型
训练完成后，进入导出编译模型的[out]路径下, 把[graph]路径下的pb模型和[model]下的yaml配置文件放到同一路径下。
将 conf_path 参数指定为 yaml配置文件 的绝对或项目相对路径即可，其他步骤一致，如下示例：
"""
with open(r"test3.jpg", "rb") as f:
    b = f.read()
sdk = muggle_ocr.SDK(conf_path="./ocr.yaml")
text = sdk.predict(image_bytes=b)
