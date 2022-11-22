#!usr/bin/env python
# coding=gbk
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from os import makedirs, path
#from random import choice
from timeit import timeit
from time import sleep
from os import remove as deleter
# import cryptography
# import pyOpenSSL
# import certifi
from urllib3 import disable_warnings

disable_warnings()
bs_url = r'https://tuchong.com/tags/'
MAX_index = 10
dir_name = './images'
if not path.exists(dir_name) or path.isfile(dir_name):
    makedirs(dir_name)
URLS_JSON = 'THE_urlS.json'

head = {
    'Host': 'photo.tuchong.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': "webp_enabled=1; lang=zh",
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    "Sec-GPC": "1",
    "TE": "trailers",
    'DNT': "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=moih71ifpv6vn8u6gcgn3diki9; webp_enabled=1; lang=zh; log_web_id=6051308894",
    "DNT": "1",
    "Host": "tuchong.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
}
SERVICE_ARGS = ['--load-images=false', '--disk-cache=false']
executable_path = r'C:\Program Files\Mozilla Firefox\geckodriver.exe'
html = {}
contents = set()
ree = {}
i = 0
firefox_options = Options()
#firefox_options.add_argument('--headless')
"""If you could not conform that the webdriver must be closed, you'd like to keep window on."""

service = Service(executable_path=executable_path, log_path="geckodriver.log") if path.isfile("geckodriver.log") else None
"""The service can help you open again while you unlikely to get an unexpected exited error which is because of webdriver hadn't closed."""

driver = webdriver.Firefox(executable_path=executable_path, service_args=SERVICE_ARGS, options=firefox_options, service=service)
waite = WebDriverWait(driver, 5)


def ropen(keyword):
    global html, ree
    driver.get(bs_url + keyword)
    waite.until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))
    assert '图虫' in driver.title, driver.title
    for i in (0,1,2):
        html = BeautifulSoup(driver.page_source, 'lxml', exclude_encodings='utf-8')
        print(html)  # no delete
        ree = html.select('main>div.content>div>ul>li>div>div>div')
        if ree:break
        if i<2:sleep(1.5)
    else:assert not ree and not print(ree), 'CAN"T SELECT!'
    driver.execute_script('window.open("https://home.firefoxchina.cn/")')

def search():
    for i in ree:
        try: contents.add((i.attrs['data-lazy-url'], i.attrs['href']))
        except KeyError: pass
        else: print('Exception')
    print(contents)
    '''more = driver.find_element(By.CLASS_NAME, 'pagelist-load-more')
    more.click()
    sleep(3)'''

def __update__():
    if path.isfile(URLS_JSON):
        with open(URLS_JSON, encoding='utf-8') as f: message = eval(f.read())
        for ii in contents: contents.remove(ii) if i in message else message.add(ii)
    else: message = contents

    with open(URLS_JSON, 'w', encoding='utf-8') as f:
        f.write(str(message))
        f.flush()

'''def deep_download(url):
    get = load_images(url, mode_auto=False)
    if not get:return
    file_names = iter(get)
    for i in file_names:
        boundary.bgpic(i)
        self.boundary.update()
        if 'n' in input('N or Y...').lower():
            deleter(i);print(i, 'DEL successes.')
        else:print(i, 'SAVEd.')
'''
def download(download_size=None, MAX_index=10):
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)
    download_size_index, download_strip = (1, '.jpg') if download_size else (0, '.webp')
    for small_or_big in contents:
        download_url = small_or_big[download_size_index]
        print(download_url, end=' ')
        if not download_url:
            print('Error!')
            continue
        MAX_index -= 1
        if not MAX_index:break
        print('Downloading...', end=" ")
        time = timeit(
        lambda :load_images(download_url, download_strip) if download_size_index else load_webp(download_url, download_strip),
                      number=1)
        print('TIME count %.3f s.' % time)
    driver.switch_to.window(driver.window_handles[0])
    print(driver.title)

def load_webp(download_url, download_strip='.webp'):
    global i
    head.update({'User-Agent': choice(USER_AGENT)})
    data = requests.get(url=download_url, stream=True, verify=False, headers=head)
    if data.status_code != 200: return print('error for', download_url)
    i += 1
    file_name = lambda :driver.title + '_' + str(i) + download_strip
    while path.isfile(file_name()):i += 1
    with open(file_name(), 'wb') as f:
        for page in data.iter_content(chunk_size=1024):
            f.write(page)
            f.flush()

def load_images(download_url, download_strip='.jpg'):
    driver.get(download_url)
    waite.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    for i in (0,1):
        content = BeautifulSoup(driver.page_source, 'lxml', exclude_encodings='utf-8')
        if content:break
        if i<1:sleep(1.2)
    else:assert content, 'CAN"T SELECT!'
    finds = content.select('main>div.content>article>img')
    print(finds)
    if not finds: return print('Error for NO finds!')
    ledx = len(finds)
    new_dir = '%s/%sP%d/' % (dir_name, driver.title, ledx)
    if not path.exists(new_dir) or path.isfile(new_dir):  makedirs(new_dir)
    else: return print('It HAD Download!')
    for i in range(ledx):
        #head.update({'User-Agent': choice(USER_AGENT)})
        for ii in (0, 1):
            data = requests.get(url=finds[i].attrs['src'], stream=True, verify=False, headers=head, timeout=2.)
            if data.status_code == 200:break
        else:
            print('error for', finds[i])
            deleter(new_dir)
            continue
        with open(new_dir + '_' + str(i) + download_strip, 'wb') as f:
            for page in data.iter_content(chunk_size=1024):
                f.write(page)
                f.flush()
        print('', end='-')
    print(new_dir, 'Download Successful!', end=' ')

def __exit__():
    driver.execute_script('window.close()')
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script('window.close()')
    try:
        driver.close()
        driver.quit()
        service.stop()
        """To stop all, service.stop() is must."""
    except Exception as e:print(e)
    finally:
        exit('EXIT!')


ropen(input('KEYWORD:'))
sleep(1)
search()
__update__()
download(True, MAX_index)

__exit__()
