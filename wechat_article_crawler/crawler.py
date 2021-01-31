import requests
import json
import urllib
import os
from bs4 import BeautifulSoup
import logging
import pdfkit
import pandas as pd
import numpy as np

MAX = 1000000001

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


# TODO 实时获取 cookie 和 key
key_ = 'af4c4474d22b7e512f633a2c7eba9d9e559e2cf9113f370d3c08f06974a97fd9a57fe105fdce30e1e33e7e02d6fc58a0d318ae0db3a0975bc1ca10474d970490518dc84b8dac9623aa6a17263864f945ab949ba9120d802806fbd22b56d820f4fa107641f3492d61ac1c42deccb0ef86b633a219cdd78d4356b0e5f6f4ca28fa'

header = {
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAwMzU1ODAwOQ==&uin=MTc2OTQ2Mjc3MQ%3D%3D&key=' + key_ + '&devicetype=Windows+10+x64&version=63010043&lang=zh_CN&a8scene=7&pass_ticket=WobaG0TjAGPOyhsl5v705iUCfZzCp70KKvXknf%2FxQFH87Exp7cQub0iwU69zuzRZ&fontgear=2',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1769462771; devicetype=android-29; version=2700163b; lang=en; pass_ticket=WobaG0TjAGPOyhsl5v705iUCfZzCp70KKvXknf/xQFH87Exp7cQub0iwU69zuzRZ; wap_sid2=CPO338sGEooBeV9ITl9DdEhCSXNxdUpMbExJWDNORzVLTHdfbDZja1pUWUlkM1RHVHI2QVByQTEtaFBVU09QdC1ROEV2QUk5OXZzZHJYYl8yMmtQYzJRbXBjNS1RZjlGbEZFc21BRVBCVHdUMXVkM2hteUx5cGtZTmhsbExhRjc4UGZDY0Y2T29zOVRTY1NBQUF+MNmpxoAGOA1AlU4='
}

header1 = {
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
}

def parse_url_to_html(url, name):
    """
    解析URL，返回HTML内容
    :param url:解析的url
    :param name: 保存的html文件名
    :return: html
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 正文
        body = soup.find_all(class_="rich_media_content ")[0]
        # 标题
        title = soup.find('h2').get_text()
 
        # 标题加入到正文的最前面，居中显示
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        # body中的img标签的src相对路径的改成绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"
 
        # def func(m):
        #     if not m.group(3).startswith("http"):
        #         rtn = m.group(1) + "http://www.liaoxuefeng.com" + m.group(2) + m.group(3)
        #         return rtn
        #     else:
        #         return m.group(1)+m.group(2)+m.group(3)
        # html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name
 
    except Exception:
        logging.error("解析错误", exc_info=True)

def save_pdf(htmls, file_name):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, file_name, options=options)

def get_url_list():
    """
    request -- get json url
    """
    for i in range(1, MAX, 10):
        ajson_url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzAwMzU1ODAwOQ==&f=json&offset=" + str(i) + "&count=10&is_ok=1&scene=&uin=MTc2OTQ2Mjc3MQ%3D%3D&key=" + key_ + "&pass_ticket=WobaG0TjAGPOyhsl5v705iUCfZzCp70KKvXknf%2FxQFH87Exp7cQub0iwU69zuzRZ&wxtoken=&appmsg_token=1098_wHht2BznlzH5YkHDVqpxrjifmEnHbRvUMX6IBA~~&x5=0&f=json"
        
        ajson = requests.get(ajson_url, headers=header).text
        contents = json.loads(ajson)
        if contents['ret'] == -3:
            print('key is invalid')
            break
        if contents['can_msg_continue'] == 0:
            break
        a_urls = json.loads(contents['general_msg_list'])['list']
        # item_urls = []
        for item in a_urls:
            try:
                item_url = item['app_msg_ext_info']['content_url']
                item_content = requests.get(item_url, headers=header).text
                # soup = BeautifulSoup(item_content)
                # item_title = soup.title.text.replace('\n', '')
                # item_img_arr = soup.find('')
            except:
                continue            


def extract_url_list(file, type):
    """
    从 json 文件中直接提取 article url df
    """
    if type == 'html':
        # content = BeautifulSoup(file, "lxml")
        content = json.loads(file)
        title_url_df = pd.DataFrame({}, columns=['title', 'url'])
        for item in content['list']:
            title = item['app_msg_ext_info']['title']
            url = item['app_msg_ext_info']['content_url']
            title_url_df = title_url_df.append(pd.DataFrame({'title':[title], 'url':[url]}))

    elif type == 'json':
        msg = json.loads(file)
        content = json.loads(msg['general_msg_list'])
        title_url_df = pd.DataFrame({}, columns=['title', 'url'])
        for item in content['list']:
            try:
                title = item['app_msg_ext_info']['title']
                url = item['app_msg_ext_info']['content_url']
                title_url_df = title_url_df.append(pd.DataFrame({'title':[title], 'url':[url]}))
            except:
                print('some content is invalid')
                continue


    return title_url_df

def get_article(url, encoding='utf-8', headers=None, filename=None, path=None):
    resp = requests.get(url, headers = header1)
    html = urllib.request.urlopen(resp)
    with open(path + '/article' + filename + '.html', 'wb') as f :
        f.write(html.read())
    bsObj = BeautifulSoup(html.read(), 'html.parser', from_encoding=encoding)
    return bsObj

def article_from_json():
    # get_url_list()
    path = './data'
    files = os.listdir(path + '/json')
    article_urls = pd.DataFrame({}, columns=['title', 'url'])
    f = open(path +'/json/' + files[0],  encoding='utf-8').read() 
    urls_df = extract_url_list(f, 'html')
    article_urls = article_urls.append(urls_df)
    for item in files[1:]:
        f = open(path +'/json/' + item,  encoding='utf-8').read()  # 注意这里要调用 read 函数否则只是一个 TextIOWrapper 没有内容
        urls_df = extract_url_list(f, 'json')
        article_urls = article_urls.append(urls_df)
        print(item)
    
    # 所有文章对应的链接文件
    # article_urls.to_csv('article_urls.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    article_from_json()      