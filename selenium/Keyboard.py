'''
Keyboard represents a KeyBoard event. KeyBoard actions are performed by using low-level interface which allows us to provide virtualized device input to the web browser.

sendKeys
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()



### sendKeys

# Navigate to url
driver.get("http://www.baidu.com")

# Enter "webdriver" text and perform "ENTER" keyboard action
driver.find_element(By.NAME, "wd").send_keys("webdriver" + Keys.ENTER)

### keyDown
# The keyDown is used to simulate action of pressing a modifier key(CONTROL, SHIFT, ALT)
# Navigate to url
driver.get("http://www.baidu.com")

# Enter "webdriver" text and perform "ENTER" keyboard action
driver.find_element(By.NAME, "wd").send_keys("webdriver" + Keys.ENTER)

webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").perform()

### keyUp

# The keyUp is used to simulate key-up (or) key-release action of a modifier key(CONTROL, SHIFT, ALT)

# Store google search box WebElement
search = driver.find_element(By.NAME, "wd")

action = webdriver.ActionChains(driver)

# Enters text "qwerty" with keyDown SHIFT key and after keyUp SHIFT key (QWERTYqwerty)
# 这个有问题，没测试出来
action.key_down(Keys.SHIFT).send_keys_to_element(search, "qwerty").key_up(Keys.SHIFT).send_keys("qwerty").perform()
# 分开写就可以
action.key_down(Keys.SHIFT).perform()
search.send_keys("qwerty")
# 这个可以输出为QWE
search.send_keys(Keys.SHIFT +"qwe")

### clear
# Store 'SearchInput' element
SearchInput = driver.find_element(By.NAME, "wd")
SearchInput.send_keys("selenium")
# Clears the entered text
SearchInput.clear()
