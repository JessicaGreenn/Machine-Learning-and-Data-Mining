import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'  # 导入项目下的settings.py
# 手动初始化Django：
import django

django.setup()
from show.models import data
from django.db.models import Q

weibodata = data.objects.filter(Q(id__in=range(7100, 10000)) & Q(platform='微博'))
weibo_tag_dict = dict()
with open('weibolabel.txt', 'r+', encoding='utf-8') as f:  # a+ 写入时追加 不会覆盖原来
    for line in f.readlines():
        line = line.strip('\n').split(' ')
        weibo_tag_dict[line[0]] = line[1]

    for c in weibo_tag_dict.items():
        print(c)

# 保存微博category
with open('weibolabel.txt', 'a+', encoding='utf-8') as f:
    for resou in weibodata:
        if resou.tags not in weibo_tag_dict.keys():
            weibo_tag_dict[resou.tags] = '待定'
            f.write(resou.tags+' '+'待定'+'\n')
        else:
            resou.category = weibo_tag_dict[resou.tags]
            resou.save()

zhihudata = data.objects.filter(platform='知乎')
weibotag_set = set([key.strip('\n').split('-')[0] for key in weibo_tag_dict.keys()])

for resou in zhihudata:
    tag = set(resou.tags.split(';'))
    category = list(tag.intersection(weibotag_set))
    if len(category) > 0:
        # 前两种情况
        resou.category = weibo_tag_dict[category[0]]
        resou.save()
    else:
        # seg = jieba.cut(text, cut_all=False)
        # keyWords = jieba.analyse.tfidf("|".join(seg), topK=10, withWeight=True)
        # 第三种情况 可以文本分类
        continue
print("知乎热搜总数", data.objects.filter(platform='知乎').count())
print("知乎已分类数量", data.objects.filter(~Q(category='') & Q(platform='知乎')).count())
print("知乎未分类数量", data.objects.filter(Q(category='') & Q(platform='知乎')).count())
print("知乎已分类数量占比", ((data.objects.filter(~Q(category='') & Q(platform='知乎')).count()) / (data.objects.filter(platform='知乎')).count()))
# import pandas as pd
# df = pd.read_csv('hav.csv','r+', encoding='utf-8')
# print(df)

