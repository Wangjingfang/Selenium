from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

### Find Element

driver.get("http://www.baidu.com")

# Get search box element from webElement 'q' using Find Element
search_box = driver.find_element(By.NAME,'wd')

search_box.send_keys("webdriver")

### Find Elements

driver.get("https://www.example.com")

elements = driver.find_elements(By.TAG_NAME,'p')

for e in elements:
    print(e.text)

### Find Element From Element
'''
It is used to find a child element within the context of parent element. To achieve this, the parent WebElement is chained with ‘findElement’ to access child elements
'''
driver.get("http://www.baidu.com")

search_form = driver.find_element(By.TAG_NAME,"form")
search_box = search_form.find_element(By.NAME,"wd")
search_box.send_keys("webdriver")

### Find Elements From Element
driver.get("https://www.example.com")

element = driver.find_element(By.TAG_NAME,"div")

elements = element.find_elements(By.TAG_NAME,"p")
for e in elements:
    print(e.text)

### Get Active Element

driver.get("http://www.baidu.com")
driver.find_element(By.CSS_SELECTOR, '[name="q"]').send_keys("webElement")

# Get attribute of current active element
attr = driver.switch_to.active_element.get_attribute("title")
print(attr)

# Is Element Enabled
driver.get("http://www.baidu.com")

# Returns true if element is enabled else returns false
# 这个'btnK' 没有找到，
value = driver.find_element(By.NAME, 'btnK').is_enabled()


# Is Element Selected
# Navigate to url
driver.get("https://the-internet.herokuapp.com/checkboxes")

# Returns true if element is checked else returns false
value = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']:first-of-type").is_selected()


### Get Element TagName
# It is used to fetch the TagName of the referenced Element which has the focus in the current browsing context.

driver.get("https://www.example.com")

# Returns TagName of the element
attr = driver.find_element(By.CSS_SELECTOR, "h1").tag_name

### Get Element Rect
'''
It is used to fetch the dimensions and coordinates of the referenced element.

The fetched data body contain the following details:

X-axis position from the top-left corner of the element
y-axis position from the top-left corner of the element
Height of the element
Width of the element
'''
# Navigate to url
driver.get("https://www.example.com")

# Returns height, width, x and y coordinates referenced element
res = driver.find_element(By.CSS_SELECTOR, "h1").rect



### 获取元素CSS值
# # Navigate to Url
driver.get('https://www.example.com')
#
# # Retrieves the computed style property 'color' of linktext
#
cssValue = driver.find_element(By.LINK_TEXT, "More information...").value_of_css_property('color')
print(cssValue)
# rgba(56, 72, 143, 1)

### Get Element Text
# Retrieves the rendered text of the specified element.
driver.get('https://www.example.com')

text = driver.find_element(By.CSS_SELECTOR,'h1').text

