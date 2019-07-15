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
i=0

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)
def get_one_page(url):
    try:
        browser.get(url)
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#search > div > div.form > button')))
        input.send_keys('礼物')
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        get_product()

        return(total.text)
    except TimeoutException:
        return get_one_page(url)
def get_next_page(page):
    try:
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.curr'),str(page)))
        get_product()

    except TimeoutException:
        return get_next_page(page)

def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList > ul > li')))
    html=browser.page_source
    #print('html=',html)
    doc=pq(html)
    items=doc('.gl-item').items()
    #print(items)

    for item in items:
        #print('item=',item)
        pat = item.find('.p-img')
        #print(pat)
        products={
            'img_url':re.findall(r'src="(.*?)"',str(pat)),
            'price':item.find('.p-price').text(),
            'describe':item.find('.p-name').text(),
            'commit_count':item.find('.p-commit').text(),
            'shopname':item.find('.p-shop .curr-shop').attr('title')
        }
        if products['img_url']==[]:
            products['img_url']=re.findall(r'bird_data-lazy-img="(.*?)"',str(pat))
        print('products=',products)
        save_to_mongo(products)
        content=download_img(products['img_url'][0])
        save_image(content)
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
        file_path='{0}/{1}.{2}'.format('H:/Python/jingdong/bird_data', hashlib.md5(content).hexdigest(), 'jpg')
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
    url='https://www.jd.com/'
    total=get_one_page(url)
    print(total)
    print('第1页')
    for page in range(2,int(total)+1):
        print('第%s页'%page)
        get_next_page(page)
    browser.close()

if __name__=='__main__':
    main()
