import requests
import os
from time import time

headers = {
    'Cookie': '_ga=GA1.2.157485442.1641026894;'
              '_gid=GA1.2.6074611508.1641026894;'
              'kw_token=WRFKXNRRLBB',
    'csrf': 'WRFKXNRRLBB',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list',
    'User-Agent': 'Mozilla/5.0(Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}
file = r'D:\music'

def down(url, name):
    o = time()
    respone = requests.get(url)
    assert respone.status_code != '200', 'status code is not 200'
    with open(name, 'wb') as f:
        for ck in respone.iter_content(102400):
            f.write(ck)
            f.flush()
        #f.write(respone.content)
    print('{} down ok with in {:.0f}min {:.2f}s.'.format(name, *divmod(time() - o, 60)))

def filt(name):
    return name.replace('&nbsp;', ' ').replace('&apos;', "'")\
        .translate(str.maketrans('<>"?:/\\|*', "[]'？：;_-^"))#\/:*?"<>|

def main(mode='A'):
    key = input('SONGER:\t')
    page = input('PAGE:\t')
    url = 'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}'.format(key, page)
    resp = requests.get(url, headers=headers)
    assert resp.status_code != '200', 'code is not 200'
    for data in resp.json()['data']['list']:
        print(f'''NAME={data['name'].replace('&nbsp;', ' ')} ARTIST={data['artist'].replace('&nbsp;', '&')} TIME={data['songTimeMinutes']}''')
        if mode.upper() == 'S':
            page = input('download???\t').lower()
            if page.startswith('n'): continue
            elif page.startswith('b'): break
        name = data['name'].split('-')[0]
        key = os.path.join(file, filtdir(data['artist'].replace('&nbsp;', '&')))
        if not os.path.exists(key): os.mkdir(key)
        filename = os.path.join(key, filt(name)) + '.mp3'
        if os.path.isfile(filename): continue
        url = 'https://link.hhtjim.com/kw/{}.mp3'.format(data['rid'])
        down(url, filename)

if __name__ == '__main__':
    if not os.path.exists(file): os.mkdir(file)
    main(input('mode=:(A)(S)\t'))
