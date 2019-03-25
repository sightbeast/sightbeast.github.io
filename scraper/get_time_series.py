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
    browser.get(url)
    browser.switch_to.default_content()

    with open('addjQuery.js', 'r') as jquery_js: 
        # 3) Read the jquery from a file
        jquery = jquery_js.read() 
        # 4) Load jquery lib
        browser.execute_script(jquery)
        time.sleep(1)
        try:
            browser.execute_script('$("g[transform=\'translate(196,0)\']").click()')
        except:
            print('jQuery not injected')

def get_data(link, sales=True, bids_asks=True):
    global url, prefix
    url = link #sys.argv[-1] #'https://stockx.com/nike-air-vapormax-moc-multi-color-w'
    prefix = url.split('/')[-1]

    refresh()
    chart = browser.find_elements_by_class_name('chart')[0].get_attribute('innerHTML')

    stroke = '#41ad33'

    try: 
        # SECOND PATH EVERY OTHER VARIABLE IS Y COORD
        soup = BeautifulSoup(chart, 'html.parser')
        path = soup.find("path", {"stroke": stroke})['d'].split('L')
        path = [float(a.strip().split(' ')[-1].strip()) for a in path]
    except:
        path = []

    name = browser.find_elements_by_class_name('name')[0].text
    print(name)
    return name, path

browser = Chrome("/usr/local/bin/chromedriver")
browser.get('http://www.stockx.com/login')

email = browser.find_element_by_name("email")
password = browser.find_element_by_name("password")

email.send_keys('akakamath@gmail.com')
password.send_keys('#Sairam21')

submit = browser.find_elements_by_class_name("button-green")[0].click();

#browser.get('https://stockx.com/adidas/yeezy')
#browser.get('https://stockx.com/new-releases/sneakers')
#browser.get('https://stockx.com/retro-jordans')

def get_by_url(link):
    browser.get(link)

    products = browser.find_element_by_id('products-container').find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('tile')
    l = len(products)
    prev_l = 0

    while True:
        try:
            browser.find_elements_by_class_name('browse-load-more')[0].find_elements_by_tag_name('button')[0].click()
        except:
            break
        finally:
            products = browser.find_element_by_id('products-container').find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('tile')
            l = len(products)
            if l == prev_l:
                break
            prev_l = l
        time.sleep(1.5)

    products = [a.find_elements_by_tag_name('a')[0].get_attribute("href") for a in products]
    products = ['https://stockx.com/yeezy-nylon-slipper-graphite-w']

    global url, prefix
    url, prefix = ['', '']

    print(products)
    df = []

    for i, link in enumerate(products[1:]):
        try:
            name, path = get_data(link, True, False)
            df.append({'name': name, 'series': path})
        except:
            print(sys.exc_info()[0])
            #browser.quit()
        time.sleep(1)
        print(i, len(products) - 1)

    df = pd.DataFrame(df)
    suffix = link.split('/')[-1]
    df.to_excel(f'{suffix}_series.xlsx')
    #browser.quit()

get_by_url('https://stockx.com/yeezy')
#get_by_url('https://stockx.com/retro-jordans')
#get_by_url('https://stockx.com/nike')

#delay = 10 # seconds
#print("Loading")
#myElem = WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'all')))
#print("Page is ready!")
#links = browser.find_element_by_xpath("//a[@class='all' and text()='View All Asks']")
#links.click()
#print(links)