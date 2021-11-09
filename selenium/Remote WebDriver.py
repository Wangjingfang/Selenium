'''
您可以如本地一样, 使用远程WebDriver. 主要区别在于需要配置远程WebDriver, 以便可以在不同的计算机上运行测试.

远程WebDriver由两部分组成：客户端和服务端. 客户端是您的WebDriver测试，而服务端仅仅是可以被托管于任何现代Java EE应用服务器的Java Servlet.

要运行远程WebDriver客户端, 我们首先需要连接到RemoteWebDriver. 为此, 我们将URL指向运行测试的服务器的地址. 为了自定义我们的配置, 我们设置了既定的功能.

下面是一个实例化样例, 其指向我们的远程Web服务器 www.example.com 的远程WebDriver对象, 并在Firefox上运行测试.
'''

### 这部分远端布置没有测试出来，
from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "67")
chrome_options.set_capability("platformName", "Windows XP")
driver = webdriver.Remote(
    command_executor='http://www.example.com',
    options=chrome_options
)
driver.get("http://www.google.com")
driver.quit()


### 本地文件检测器
'''
本地文件检测器允许将文件从客户端计算机传输到远程服务器. 例如, 如果测试需要将文件上传到Web应用程序, 则远程WebDriver可以在运行时 
将文件从本地计算机自动传输到远程Web服务器. 这允许从运行测试的远程计算机上载文件. 默认情况下未启用它, 可以通过以下方式启用:
'''
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.common.by import By

driver.file_detector = LocalFileDetector()

driver.get("http://sso.dev.saucelabs.com/test/guinea-file-upload")

driver.find_element(By.ID, "myfile").send_keys("/Users/sso/the/local/path/to/darkbulb.jpg")

#### 追踪客户端请求 (仅适用于Jave客户端绑定)
# 操作文档：https://www.selenium.dev/zh-cn/documentation/webdriver/remote_webdriver/


