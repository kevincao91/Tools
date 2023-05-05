#coding=utf-8
import requests
from lxml import etree
import re
import time
import os

img_count = 0
file = ''
word = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# 保存图片
def save_img(url):
    img_name = url[-10:]
    #name = re.sub('/', '', img_name)  # img_name中出现/，将其置换成空
    global img_count
    global file
    global word
    name = 'bing_'+ word +'_'+str(img_count)+'.jpg'
    img_count = img_count + 1
    try:
        res = requests.get(url, headers=headers, timeout=7)
    except BaseException:
        print('出现错误，错误的url是:', url)
    else:
        with open(file + '/' + name, 'wb')as f:
            try:
                f.write(res.content)
            except OSError:
                print('无法保存，url是：', url)


# 获取全部图片url
def parse_img(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    data = response.content.decode('utf-8', 'ignore')
    html = etree.HTML(data)
    conda_list = html.xpath('//a[@class="iusc"]/@m')
    all_url = []    # 用来保存全部的url
    for i in conda_list:
        img_url = re.search('"murl":"(.*?)"', i).group(1)
        all_url.append(img_url)
    return all_url


# 主函数
def main():
    global word
    for i in range(0, 2000, 35):
        url = 'https://cn.bing.com/images/async?q='+ word +'&first='+str(i)+'&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1'
        img_data = parse_img(url)
        for img_url in img_data:
            print(img_url)
            save_img(img_url)

        time.sleep(1)


if __name__ == '__main__':
    file = input("请输入图片存放文件夹地址: ")
    if not os.path.exists(file):
        os.mkdir(file)
    word = input("请输入搜索关键词: ")
    main()
