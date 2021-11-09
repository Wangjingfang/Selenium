'''
代理服务器充当客户端和服务器之间的请求中介. 简述而言, 流量将通过代理服务器流向您请求的地址, 然后返回.

使用代理服务器用于Selenium的自动化脚本, 可能对以下方面有益:

捕获网络流量
模拟网站后端响应
在复杂的网络拓扑结构或严格的公司限制/政策下访问目标站点.
如果您在公司环境中, 并且浏览器无法连接到URL, 则最有可能是因为环境, 需要借助代理进行访问.
'''

from selenium import webdriver

PROXY = "<HOST:PORT>"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",

}

with webdriver.Firefox() as driver:
    # Open URL
    driver.get("https://selenium.dev")

