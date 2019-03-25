from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import sys
import os
import time
from bs4 import BeautifulSoup

elementDict = {'.last-sale-block': 'Sales', '.bid-button-b': 'Asks', '.ask-button-b': 'Bids'}
idDict = {'.last-sale-block': "480", '.bid-button-b': "400", '.ask-button-b': "300"}
jquery_url = '//code.jquery.com/jquery-latest.min.js'

def refresh():
    global url
    print('Refresher', url)
    
    browser.switch_to.default_content()

    with open('addjQuery.js', 'r') as jquery_js: 
        # 3) Read the jquery from a file
        jquery = jquery_js.read() 
        # 4) Load jquery lib
        browser.execute_script(jquery)

    time.sleep(1)

browser = Chrome("/usr/local/bin/chromedriver")
browser.get('http://www.stockx.com/login')

email = browser.find_element_by_name("email")
password = browser.find_element_by_name("password")

email.send_keys('akakamath@gmail.com')
password.send_keys('#Sairam21')

submit = browser.find_elements_by_class_name("button-green")[0].click();

browser.get('https://stockx.com/adidas-yeezy-boost-700-inertia')
chart = browser.find_elements_by_class_name('chart')[0].get_attribute('innerHTML')

stroke = '#41ad33'

# SECOND PATH EVERY OTHER VARIABLE IS Y COORD
soup = BeautifulSoup(chart, 'html.parser')
path = soup.find("path", {"stroke": stroke})['d'].split('L')

path = [float(a.strip().split(' ')[-1].strip()) for a in path]

print(path)

browser.quit()



































