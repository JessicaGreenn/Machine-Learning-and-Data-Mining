"""
@File    : 微博热搜榜.py
@Author  : Accelerator
@Time    : 2022/01/11 22:11
@notice  : 爬取微博热搜榜列表&热度&链接&分类&具体内容
"""
import time
from lxml import etree
import pandas as pd
from selenium import webdriver
import datetime
import time

detail_url = 'https://s.weibo.com/weibo?q=%23{}%23&Refer=top'    # 搜索页面
driver = webdriver.Chrome()
driver.switch_to.new_window('tab')
driver.get('https://s.weibo.com/top/summary')
original_window = driver.current_window_handle
time.sleep(5)

print('当前页面标题：'+driver.title)
print('当前页面地址：'+driver.current_url)
print('----------------微博热搜分割线----------------')

today = datetime.date.today()
f = open('./微博热搜榜-%s.csv' % today, 'a', encoding='utf-8')  # a 追加模式
counter = 0

# print(driver.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr[1]/td[2]/a')[0].text)
tr_list = driver.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
tr_list.pop(4)  # 去广告
tr_list.pop(8)  # 去广告
for tr in tr_list[1:]:
    str1 = tr.text.strip('\n').split(' ')
    if len(str1) == 2:
        name = str1[0]
        hot = str1[1]
    elif len(str1) == 3 or len(str1) == 4:
        name = str1[0]
        hot = str1[2]
    else:
        name = str1[0]
        hot = ' '

    url = detail_url.format(name)

    driver.switch_to.new_window('tab')
    driver.get(url)
    time.sleep(5)
    print('当前页面地址：' + driver.current_url)

    try:
        tags = driver.find_element_by_xpath(
            '//div[@class="card card-about"]//div[@class="card-content s-pg16"]/dl/dd[1]/a'
        ).accessible_name
        # ta = tags.accessible_name
        # print("ta:", ta)  # 有结果
        # tb = tags.get_attribute("textContent")
        # print("tb:", tb)  # 有结果
        # tc = tags.text
        # print("tc:", tc)  # 空字符
        print("tags:", tags)
    except:
        tags = '无分类'

    try:
        content = driver.find_element_by_xpath(
            '//div[@class="card card-topic-lead s-pg16"]/p'
        ).text
    except:
        content = ' '  # 微博导语有的会存在emoji表情，本地数据库识别不了会报错，暂时的做法是选择把这条热搜跳过，更改循环里的tr_list[1:]的索引跳过

    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(counter, name, url, hot, tags, content)

    counter += 1

    f.write(
        str(counter) + ','
        + name + ','
        + hot + ','
        + tags + ','
        + content + ','
        + url + ','
        + date + ','
        + '微博'
        + '\n')

    driver.close()
    driver.switch_to.window(original_window)

f.close()

