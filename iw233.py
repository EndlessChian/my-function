#!python3
#coding=utf-8
import requests
import time
import os

requests.packages.urllib3.disable_warnings()

HOST = "iw233.cn", "api.iw233.cn", "dev.iw233.cn"
FREQUANCY = 200
CONNECTION = 100
NUMBER = 100
DIRT = r"D:\python\.hh\hh"
if not os.path.exists(DIRT):
    os.mkdir(DIRT)
Cookie = "Hm_lvt_2bfe99c3d9f44e09ca1a2ac5a769294c=1680136397,1681551293,1681636066; Hm_lpvt_2bfe99c3d9f44e09ca1a2ac5a769294c=1681636066",
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66",
headers = {# https://dev.iw233.cn/API/index.php
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cache-Control": "max-age=24",# make a timeout-clear schedule
    "Connection": "close",# avoid connection not close error
    "Cookie": Cookie[0],# updata intime
    "DNT": "1",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Mode": "navigate",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent[0],
}
head = {
    "DNT": "1",
    "Connection": "close",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    "sec-ch-ua-mobile": "?0",
    "Cache-Control": "max-age=12",
    "Referer": "https://weibo.com/",# must
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent[0],
}

def getJSON(host, sort, num=1):
    response = session.get(f"https://{host}/api.php?sort={sort}&type=json&{num=}", headers=headers | {
        "Referer": f"https://{host}/API/index.php",
        "Connection": "close",
        "Host": host,
    }, stream=False, timeout=5)
    try:
        assert response.status_code == 200
        return response.json()['pic']
    except AssertionError:
        raise
    except:
        print(response.text)
        raise
    finally:
        response.close()

def getJPG(url, head, file, stream=False):
    response = session.get(url, headers=head, stream=stream, verify=False, timeout=10)
    try:
        assert response.status_code == 200, response.status_code
        for ck in response.iter_content(1024 * 1024):
            file.write(ck)
            file.flush()
        return True
    except AssertionError as w:
        print('Download Exception in getJPG function', w)
    finally:
        response.close()
    return False

class GATE:
    def __init__(self, long, top=None):
        self.GT = self.SEP = 0
        self.T0 = time.time()
        self.OUTLINE = self.T1 = 0
        self.timeout = lambda i: i * long
        self.top = top

    def __iadd__(self, other):
        self.GT += 1
        return self

    def __call__(self):
        T1 = time.time() - self.T0
        self.SEP = self.timeout(self.GT) - T1
        self.OUTLINE = self.timeout(self.GT) - self.T1
        if self.SEP < 0:
            self.OUTLINE -= self.SEP
            self.SEP = 0
        self.T1 = T1
        return self.SEP

    def __repr__(self):
        return f'Progress: {self.GT / self.top * 100 if self.top else self.GT:.2f}%; UsedTime: {self.T1:.2f}s; ' \
               f'OUTofSCUDLE: {self.OUTLINE:.2f}s; Budget: {self.timeout(self.top or self.GT) + self.OUTLINE:.2f}s.'

if __name__ == '__main__':
    sort = input('sort=')
    num = int(input('num='))
    times, last = divmod(num, NUMBER)
    GT = GATE(60 / FREQUANCY, num)
    with requests.Session() as session:
        while last or times:
            for host in HOST:
                if input('continue'):# interrupted choice
                    exit(-1)
                try:
                    GT += 1
                    res = getJSON(host, sort, NUMBER if times > 0 else last)
                    time.sleep(GT())
                    assert res
                except Exception as e:
                    print(e)
                else:
                    if times > 0:
                        times -= 1
                    elif last:
                        last = 0
                    break
            else:
                # no host answay
                print('not host answay')
                continue
            for url in res:
                path = os.path.join(DIRT, os.path.basename(url))
                if os.path.isfile(path):
                    continue
                with open(path, 'wb') as f:
                    GT += 1
                    if getJPG(url, head, f, False):
                        print('*'.center(50, '*'))
                        print('DOWNLOAD OK', path)
                    else:
                        # test
                        print('false', url)#https:\/\/tva2.sinaimg.cn\/large\/ec43126fgy1go5napxkw1j21xe13bkjq.jpg
                        while input('test'):
                            if getJPG(input('url'), head | eval(input('dict')), file):
                                print('download', path)
                            else:
                                print('false')
                    print('-'*50)
                    time.sleep(GT())
                    print(GT)
        pass