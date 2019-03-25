from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = Chrome("/usr/local/bin/chromedriver")
browser.get('http://www.stockx.com/login')

email = browser.find_element_by_name("email")
password = browser.find_element_by_name("password")

email.send_keys('akakamath@gmail.com')
password.send_keys('#Sairam21')

submit = browser.find_elements_by_class_name("button-green")[0].click();

url = 'https://stockx.com/air-jordan-4-retro-white-black-bright-crimson'
browser.get(url)

delay = 10 # seconds
print("Loading")
#myElem = WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'all')))
#print("Page is ready!")
links = browser.find_element_by_xpath("//a[@class='all' and text()='View All Asks']")
links.click()
print(links)