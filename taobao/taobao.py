import re
import hashlib
import os
import requests
from requests import RequestException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

from config import *
import pymongo

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)

def get_one_page(url):
    try:
        browser.get(url)
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_product()

        return(total.text)
    except TimeoutException:
        return get_one_page(url)
def next_one_page(page_number):
    try:
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_product()

    except TimeoutException:
        return next_one_page(page_number)

def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=browser.page_source
    #print(html)
    doc=pq(html)
    items=doc("#mainsrp-itemlist .items .item").items()
    for it in items:
         product={
             'image':it.find('.pic .img').attr('bird_data-src'),
             'price':it.find('.price').text(),
             'deal-cnt':it.find('.deal-cnt').text()[:-3],
             'title':it.find('.title').text(),
             'shopname':it.find('.shopname').text(),
             'location':it.find('.location').text()
         }
         #print(product)
         save_to_mongo(product)
         print(product.get('image'))
         img_url=product.get('image')
         content=download_img(img_url)
         save_image(content)
         #save_to_mongo(content)
def download_img(url):
    try:
        response=requests.get('http:'+url)
        if response.status_code==200:
            return response.content
        else:
            print('打开图片失败')
            return None
    except RequestException:
        return None

def save_image(content):
    if content!=None:
        file_path='{0}/{1}.{2}'.format(os.getcwd(), hashlib.md5(content).hexdigest(), 'jpg')
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(content)
                f.close()
        print('存储图片成功')
    else:
        print('打开图片失败')
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)

def main():
    url='https://www.taobao.com/'
    searc=get_one_page(url)
    total=int(re.compile('(\d+)').search(searc).group(1))
    print(total)
    for i in range(2,total+1):
        next_one_page(i)
    browser.close()
if __name__=='__main__':
    main()