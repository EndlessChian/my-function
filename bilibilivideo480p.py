# coding = utf-8
import requests
import json
from lxml import etree
import os

requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Cookie': 'CURRENT_QUALITY=80;',
}
file = r'D:\download'

def GetBiliVideo(homeurl,num,file,session=requests.session()):
    res = session.get(url=homeurl, headers=headers, verify=False)
    assert res.status_code != '200', 'status code is not 200'
    html = etree.HTML(res.content)
    videoinforms = str(html.xpath('/html/body/script[3]/text()')[0])[25:]
    listjson = json.loads(videoinforms)
    # 获取详情信息列表
    listinform = str(html.xpath('/html/body/script[4]/text()')[0])
    print(listinform)
    videojson=json.loads(listinform[20:])
    # 获取视频链接和音频链接
    try:
        # 2018年以后的b站视频，音频和视频分离
        VideoURL = videojson['data']['dash']['video'][0]['baseUrl']
        AudioURl = videojson['data']['dash']['audio'][0]['baseUrl']
        flag=0
    except Exception:
        # 2018年以前的b站视频，格式为flv
        VideoURL = videojson['data']['durl'][0]['url']
        flag=1
    # 获取文件夹的名称
    #dirname = str(html.xpath("/html/head/title/text()")[0]).split('-')[0].strip()
    dirname = str(html.xpath('/html/head/script[4]/text()')[0]).strip()
    dirname = json.loads(dirname)['itemListElement'][0]['name']
    print(dirname)
    if not dirname.isalnum(): dirname = input('dirname is not avoildable. please give a new one:\t')
    if not os.path.exists(os.path.join(file, dirname)):
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(os.path.join(file, dirname))
        print('目录文件创建成功!')
    # 获取每一集的名称
    try:
        print(listjson)
        name=dirname + '_' + listjson['progress']['last_ep_index']
    except KeyError:
        #'/html/body/div[2]/div[2]/div[3]/div[2]/ul/li[8]/a/span'
        name = dirname + '_' + str(num + 1)#('not found listnum, please add one:\t')
    print(name)
    # 下载视频和音频
    print('正在下载 "'+name+'" 的视频····')
    BiliBiliDownload(homeurl=homeurl,url=VideoURL, name=os.path.join(file, dirname, name) + '_Video.mp4', session=session)
    if flag==0:
        print('正在下载 "'+name+'" 的音频····')
        BiliBiliDownload(homeurl=homeurl,url=AudioURl, name=os.path.join(file, dirname, name) + '_Audio.mp3', session=session)
    print(' "'+name+'" 下载完成！')

def BiliBiliDownload(homeurl,url, name, session=requests.session()):
    headers.update({'Referer': homeurl})
    session.options(url=url, headers=headers,verify=False)
    # 每次下载1M的数据
    begin = 0
    end = 1024*512-1
    flag=0
    while True:
        headers.update({'Range': 'bytes='+str(begin) + '-' + str(end)})
        res = session.get(url=url, headers=headers,verify=False)
        if res.status_code != 416:
            begin = end + 1
            end = end + 1024*512
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = session.get(url=url, headers=headers,verify=False)
            flag=1
        with open(name, 'ab') as fp:
            fp.write(res.content)
            fp.flush()

        # data=data+res.content
        if flag==1:
            fp.close()
            break


#av306286164
if __name__ == '__main__':
    av = input('请输入视频号：')
    url='https://www.bilibili.com/video/'+av
    # 视频选集
    range_start=int(input('从第几集开始？'))
    range_end = int(input('到第几集结束？'))
    if range_start < range_end:
        for index in range(range_start, range_end + 1):
            GetBiliVideo(url+'?p='+str(index),index-1, file)

    else:
        print('选集不合法！')
