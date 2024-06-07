#!python
#coding=utf-8
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
    'Connection': 'close',
    "Cache-Control": "max-age=12",
    'User-Agent': 'Mozilla/5.0(Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}
file = r'D:\music'

def getMP3(url, name):
    o = time()
    print('*', end='')
    try: respone = requests.get('https://' + url)	# cert=
    except Exception as e:
        print(e)
        respone = requests.get('http://' + url, verify=False)
    assert respone.status_code == 200, respone.close()
    with open(name, 'wb') as f:
        for ck in respone.iter_content(102400):
            f.write(ck)
            f.flush()
            print('-', end='')
        print('|', end='')
    respone.close()
    print('{} down ok with in {:.0f}min {:.2f}s.'.format(name, *divmod(time() - o, 60)))

filt = lambda name: name.replace('&nbsp;', ' ').replace('&apos;', "'").replace('&quot;', '~')\
        .translate(str.maketrans('<>"?:/\\|*', "[]'!,;_#^"))#\/:*?"<>|

class from_163:
    'https://music.163.com/#/search/m/?s={}&type=1'
    '//*[@id="auto-id-ggDuBPnFzeOiaFSq"]/div/div/div[1]/div[2]/div/div/a[1]'
    "https://music.163.com/api/sns/authorize?snsType=2&clientType=web2&callbackType=Login&forcelogin=true"
    {
    'cache-control': 'max-age=0',
    'cookie': '_ntes_nnid=4294b11f9764948ae9616aed995187d1,1683625727456; _ntes_nuid=4294b11f9764948ae9616aed995187d1; '
              'NMTID=00OZ087idLSHfSz8Ueilzmo-6fHvmgAAAGH_-m6kA; WEVNSM=1.0.0; WNMCID=qfagbv.1683625727770.01.0; '
              'WM_NI=%2FFwsfyY9iYg9N4rGLHPR4fmvGCjGrspNNgcePjkg44kFiHN4cfQtLGIqd0GAanXPbIkLafnqkutwplz73f34KM4zlYVcnHHRP'
              'RiYxNIeIZJUA%2BhQWjQlh5WU5T8Jvy91YkE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee94f73ff7ecb782b72187b08fb3d14e96'
              '8a8b82c445f5eaba96d96a8dabc0b5c52af0fea7c3b92aed9ab994e5739be7a7bae6338eecbea8cf44948efc87f07e859da6a8f17'
              '9b4928288e26f94b6a588b740a99aa7a9cd40a1ba9f95cf4d8bafacd1c64ba3b298b1e143a994af87ed7ba9abbc98f368bae9fd87'
              'b2408993fc9bef5396bda2a9cb5a948ea7bafb468bbb87bbc95f83f5a8b2d66293b4a8d6d65ff78cf8abf573fbef978cc837e2a3; '
              'WM_TID=Oqd5ShjeM0FEQUQVQRaEe6%2Bv7Yaf74HA; JSESSIONID-WYYY=Q%2F8TvoA6TZefTFCi85B3lx2bmSqxFVuT%5CznivHe8I6'
              '3xbJ2Hbp%2Fh18JDR9BI4k1djeVmDMx6fi69dhqQ5NwAMzCNTGWPvl443PDIi1ZQGlCM4tJhNiJRtQhCew6b%5C5di9cH9nIuxAI3DKSk'
              'vtWbVm7d1PldKfoX%2FDEfw3QDXg0r3EsaU%3A1683627529646; _iuqxldmzr_=33',
    'dnt': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
     }
def get(mode, key, page):
    url = 'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}'.format(key, page)
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200, 'status code is not 200'
    li = resp.json()['data']['list']
    resp.close()
    for data in li:
        data['name'] = filt(data['name'].strip())
        data['artist'] = filt(data['artist'].replace('&nbsp;', '&'))
        print('NAME={name} ARTIST={artist} TIME={songTimeMinutes}'.format_map(data))
        if mode.upper() == 'S':
            page = input('download???\t').lower()
            if page.startswith('n'): continue
            elif page.startswith('b'): break
        name = data['name'].split('-')[0]
        key = os.path.join(file, data['artist'])
        if not os.path.exists(key): os.mkdir(key)
        filename = os.path.join(key, filt(name)) + '.mp3'
        if os.path.isfile(filename): continue
        url = 'link.hhtjim.com/kw/{}.mp3'.format(data['rid'])
        getMP3(url, filename)

if __name__ == '__main__':
    if not os.path.exists(file): os.mkdir(file)
    get(input('mode=:(A)(S)\t'), input('SONGER:\t'), input('PAGE:\t'))
