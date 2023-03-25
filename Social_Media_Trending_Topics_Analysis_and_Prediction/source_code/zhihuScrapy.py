# import os
# import sys
# sys.path.append(os.path.dirname(os.path.abspath('.')))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'  # 导入django项目下的settings.py
# # 初始化Django
# import django
# django.setup()
#
# from items import DatabotsItem

import requests
import re
from bs4 import BeautifulSoup
import datetime

## 获取知乎热搜，https://zhuanlan.zhihu.com/p/86035241


headers = {"User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
           "Cookies": "_zap=d7b289b2-e55b-4350-8715-496a08827b7e; d_c0=\"AKAfcF9ZYBOPTg0eNt6tu8QgvXnBE--nKZk=|1625663393\"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=%2BW1SoRfORvFBVERUFQc%2ByYBTQ3qkGwB2; gdxidpyhxdE=Od0bAmYwxWyPShefxZe%5CHHO%2BtlIiU%2FInv6tT7eHQqijKGVv1lMsajs477eq4UQNhwRfrzfVcoN%2FVudTGyLZY55%5Cr9AnjA3HYz7%2FGtcPjax0oiZ9oCv5tIWaikoszDzI0uOk4NA7gqAXxvs7QvDu07Z0c0nrv4dJDU1tmb3%2Bkm9HddoCY%3A1646820390779; YD00517437729195%3AWM_NI=nQLzZZVefMzxSpDVcX0IwLV17zZX9ivHBnLao55AJuBz%2BMrN6mbVZxjjgDEsXhOFePqklSFft%2FYc5uXWs9g5vZF%2F6tFKMJPLOYrXQMHe5tLvGbw2qCry1FTGVs7oDQNOUzE%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eebbf66d9b95a4d8f843bae78fa3c15e839e8babae25afb2fcb6ed3f8db9bda7c12af0fea7c3b92aae8f849bd95296bbaaaef97491b08cb7e254f497b9add53bf5a696b9bc63b6988e8fcf6badebfba2c97f82a6e5aef146f6b3aeb7d974aab6a9a5c8799cb881a7e85cb3b5a4b4c56eb8f19784b87f9c89bddae63fb6868ad0b580869583abd3488d87beb9d4478cbbfb95cf7e85beb9d3f449b2a7ffa7d74d96adf990c75b8e919b9bc837e2a3; captcha_session_v2=\"2|1:0|10:1646819601|18:captcha_session_v2|88:SHdtR2J3dHNMZWZZYVI3T3hidGFabGVkM24wN0tZQm5oY0pBaEU1Q21zZ0FOZ05jY1Uydnk1NmdCeUJ0L04rVQ==|6fa85c49dc3474e59dcd2f4f8ca442c5e7989d2f5c51ad023c97c3290081e5f0\"; _xsrf=a1c19548-cefd-4ccc-8ecc-786ee064f1fd; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1647336290; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1647336290; SESSIONID=NCfoRpWtZNC5PABC3YD6r12GxykScgH7dFv25DetWJK; JOID=WlkTBkuFvWxALIR1E4jM_-xI0BQOwvkJKnb9JWTX-ih2ec0-V-niWi8tinEVgdQ2NT4nTdeePTAzmAZ43NIicqM=; osd=V1scBE-Iv2NCKIl3HIrI8u5H0hADwPYLLnv_KmbT9yp5e8kzVebgXiIvhXMRjNY5NzoqT9icOT0xlwR80dAtcKc=; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1647336312|1647336288"}

zh_url = "https://www.zhihu.com/billboard"
zh_response = requests.get(zh_url, headers=headers)
web_content = zh_response.text

soup = BeautifulSoup(web_content, 'html.parser')#解析requests获取的数据
script_text = soup.find("script", id="js-initialData").get_text()

rule = r'"hotList":(.*?),"guestFeeds"'

result = re.findall(rule, script_text)  # 由正则化得到热搜规则下的脚本
temp = result[0].replace("false", "False").replace("true", "True")
#把js中的true, false换成python可读版
hot_list = eval(temp)


def get_tags(ex_url):
    html = requests.get(ex_url, headers=headers)
    html_content = html.text
    rules = r'<meta data-react-helmet="true" name="keywords" content="(.*?)"/>'
    tag = re.findall(rules, html_content)[0].replace(',', ';')
    return tag


counter = 0
today = datetime.date.today()
f = open('热搜榜-2022-02-25.csv', 'w', encoding='utf-8')

for tr in hot_list:
    counter = counter + 1
    name = tr['target']['titleArea']['text']
    url = tr['target']['link']['url']
    hot = tr['target']['metricsArea']['text']
    content = tr['target']['excerptArea']['text']
    tags = get_tags(url)

    print(counter, name, url, hot, tags, content)

    f.write(
        str(counter) + ','
        + name + ','
        + hot + ','
        + tags + ','
        + content + ','
        + url
        + '\n')

f.close()




