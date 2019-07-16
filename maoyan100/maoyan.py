import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
def get_one_page(url):
    try:
        responce=requests.get(url)
        if responce.status_code==200:
            return responce.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?bird_data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>'
                        +'.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'url':item[1],
            'name':item[2],
            'star':item[3].strip()[3:],
            'releasetime':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(contex):
    with open('contex.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(contex,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
    pool=Pool()
    pool.map(main,[(i*10) for i in range(10)])

