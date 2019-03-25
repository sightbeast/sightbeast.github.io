from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import sys
import os
import time

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

def get_sales(element):
    refresh()
    with open('get_data.js', 'r') as jquery_js: 
        jquery = jquery_js.read()
        browser.execute_script(jquery + "\nclearElement('"+element+"');loadswag('#"+idDict[element]+"', function() {console.log('swag')});")

    #limit = int(browser.find_elements_by_class_name('gauge-value')[0].text)
    print([a.text for a in browser.find_elements_by_class_name('gauge-value')])
    limit = 10000
    max_tries = 3
    rows = browser.find_elements_by_tag_name("tbody")[-1].find_elements_by_tag_name('tr')
    prev_rows = rows
    num_times_repeated = 0

    while len(rows) < limit and num_times_repeated < max_tries:
        rows = browser.find_elements_by_tag_name("tbody")[-1].find_elements_by_tag_name('tr')
        if len(rows) == len(prev_rows):
            num_times_repeated += 1
            print('repeated', num_times_repeated)
        else:
            num_times_repeated = 0
        prev_rows = rows
        #print(len(browser.find_elements_by_tag_name("tbody")[-1].find_elements_by_tag_name('tr')))
        time.sleep(1)

    #print(element)
    #print(browser.find_elements_by_tag_name("tbody")[-1].get_attribute('innerHTML'))
    rows = browser.find_elements_by_tag_name("tbody")[-1].find_elements_by_tag_name('tr')
    rows = [a.find_elements_by_tag_name('td') for a in rows]
    rows = [[b.text for b in a] for a in rows]
    headings = ['Date', 'Time', 'Size', 'Price']
    #print(rows)
    df = pd.DataFrame(rows, columns=headings)
    df.to_csv('yeezys/'+prefix+'-'+elementDict[element]+'.csv')
    browser.execute_script(jquery + "\nclearElement('"+element+"');")

def bid_ask(element):
    with open('get_data.js', 'r') as jquery_js: 
        refresh()
        jquery = jquery_js.read() 
        browser.execute_script(jquery + "\nclearElement('"+element+"');")
        browser.execute_script(jquery + "\nwriteCSV('#"+idDict[element]+"', '"+prefix+'-'+elementDict[element]+"', '"+element+"');")
        try:
            element = WebDriverWait(browser, 10000).until(
                EC.presence_of_element_located((By.ID, "fuckingloaded"))
            )
        except:
            print("FUCKED")
            browser.quit()

def get_data(link, sales=True, bids_asks=True):
    global url, prefix
    url = link #sys.argv[-1] #'https://stockx.com/nike-air-vapormax-moc-multi-color-w'
    prefix = url.split('/')[-1]

    if sales:
        print("Getting Sales Data...")
        get_sales('.last-sale-block')
        print("Fetched Sales Data")

    if bids_asks:
        print("Getting bid data...")
        bid_ask('.ask-button-b')
        os.system(f'mv ~/Downloads/{prefix}-Bids.csv yeezys/bids')
        print("Fetched Bid Data")

        print("Getting Ask Data...")
        bid_ask('.bid-button-b')
        os.system(f'mv ~/Downloads/{prefix}-Asks.csv yeezys/asks')
        print("Fetched Ask Data.")

browser = Chrome("/usr/local/bin/chromedriver")
browser.get('http://www.stockx.com/login')

email = browser.find_element_by_name("email")
password = browser.find_element_by_name("password")

email.send_keys('akakamath@gmail.com')
password.send_keys('#Sairam21')

submit = browser.find_elements_by_class_name("button-green")[0].click();

browser.get('https://stockx.com/adidas/yeezy')
#browser.get('https://stockx.com/new-releases/sneakers')

products = browser.find_element_by_id('products-container').find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('tile')
l = len(products)
prev_l = 0

while True:
    try:
        browser.find_elements_by_class_name('browse-load-more')[0].find_elements_by_tag_name('button')[0].click()
        time.sleep(1)
    except:
        break
    finally:
        products = browser.find_element_by_id('products-container').find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('browse-grid')[0].find_elements_by_class_name('tile')
        l = len(products)
        if l == prev_l:
            break
        prev_l = l

products = [a.find_elements_by_tag_name('a')[0].get_attribute("href") for a in products]

global url, prefix
url, prefix = ['', '']

print(products)

for link in products[1:]:
    print(link)
    get_data(link, True, False)
    try:
        get_data(link, True, False)
    except:
        try:
            print('first didn\'t work')
            time.sleep(3)
            get_data(link, True, False)
        except:
            try:
                print('second didn\'t work')
                time.sleep(3)
                get_data(link, False, False)
            except:
                print('Probably not enough sales')

#delay = 10 # seconds
#print("Loading")
#myElem = WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'all')))
#print("Page is ready!")
#links = browser.find_element_by_xpath("//a[@class='all' and text()='View All Asks']")
#links.click()
#print(links)