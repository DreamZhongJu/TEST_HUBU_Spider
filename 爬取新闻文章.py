import urllib.request
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from configparser import ConfigParser
import glob



if glob.glob('option.ini') == []:
    config = ConfigParser()  # 读取配置文件
    config.read('.\option.ini', encoding='UTF-8')
    config["URL"] = {
        'Link' : 'https://zsxx.hubu.edu.cn/zsxx/',
        "Name": "zsjz"
    }
    config["Range"] = {
        'start' : '9',
        'end' : '1',
        'step' : '-1'
    }
    config["User-Agent"] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    config["File"] = {
        'name' : 'Dafult'
    }
    # SAVE CONFIG FILE
    with open("option.ini", "w") as file_object:
        config.write(file_object)
    print("找不到配置文件，已生成默认文件")

# print file content
read_file = open("option.ini", "r")
content = read_file.read()
print("配置文件内容如下:")
print(content)


config = ConfigParser() #读取配置文件
config.read('.\option.ini', encoding='UTF-8')
pages = set() #页面集合
myHeader=config['User-Agent']


file = open('.\\'+config['File']['name']+'.txt','w', encoding='utf-8') #在当前目录生成一个爬取文件

def getLinks(pageurl): #获取相关链接
    global pages
    #html = requests.get('https://news.hubu.edu.cn/info/1052/'+pageurl+".htm",headers=myHeader).content
    html = requests.get(config["URL"]['Link']+pageurl+".htm",headers=myHeader).content
    bs = BeautifulSoup(html, 'html.parser')
    try:
        for link in bs.find_all('a'):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    newPage = link.attrs['href']
                    try:
                        newPage = re.findall('info/\d{4}/\d{4}',newPage)[0]
                        pages.add(newPage)
                        getText(newPage)
                    except:
                        None

    except:
        print("爬取失败")


def getText(pageurl):
    html = requests.get('https://zsxx.hubu.edu.cn/'+pageurl+".htm",headers=myHeader).content
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.find_all('h2',{'align':"center"})[0].get_text())
        article = bs.find_all('div',{'class':"v_news_content"})[0].get_text()
        file.write(article)
        file.write('\n')
    except:
        print("文章获取失败")



getLinks(config['URL']['name'])
start = int(config['Range']['start'])
end = int(config['Range']['end'])
step = int(config['Range']['step'])
for i in range(start,end,step):
    getLinks(config['URL']['name']+"/"+str(i))

file.close()

