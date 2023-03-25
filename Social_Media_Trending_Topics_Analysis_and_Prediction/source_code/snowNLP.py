#import os
#import sys
#sys.path.append(os.path.dirname(os.path.abspath('.')))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'  # 导入项目下的settings.py
# 手动初始化Django：
#import django
#django.setup()

# 导入SnowNLP库
from snownlp import SnowNLP
#from show.models import data
import math

from pyecharts.charts import Bar, Pie
from pyecharts import options as opts  # 用于设值全局配置和系列配置

import pandas as pd
all = pd.read_csv('datascrapy.csv')

for resou in all.values[6500:]:
    title = resou[1]
    text = resou[8]
    s = SnowNLP(title + ' ' + text)
    resou[13] = s.sentiments
#    resou.save()

weibodata = all.loc[all['platform'] == '微博']

all_tags = {}
all_senti = {'positive': 0, 'negative': 0, 'neutral': 0}
all_senti10 = [0]*11
neg_resou = []
for resou in weibodata.values:
    p_tags = resou[3].strip('\n').split('-')[0] #一级分类
    all_tags.setdefault(p_tags, 0)
    all_tags[p_tags] += 1

    all_senti10[math.floor(float(resou[13]) * 10)] += 1
    if math.floor(float(resou[13])) == 0:
        neg_resou.append(resou[1])

    if float(resou[13]) > 0.65:
        all_senti['positive'] += 1
    elif float(resou[13]) < 0.35:
        all_senti['negative'] += 1
    else:
        all_senti['neutral'] += 1
#print(neg_resou)

data_pair = [list(z) for z in zip(all_tags.keys(), all_tags.values())]   # 饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
(   # 初始化配置项，内部可设置颜色
    Pie(
        init_opts=opts.InitOpts(bg_color="#f0fcff")
    )
    .add(
        series_name="微博热搜tags分析",  # 系列名称，即该饼图的名称
        data_pair=data_pair,  # 系列数据项，格式为[(key1,value1),(key2,value2)]
        rosetype="radius",  # 通过半径区分数据大小 “radius” 和 “area” 两种
        radius="55%",  # 饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        # radius=["15%", "50%"],   # 饼图内圈和外圈的大小比例
        center=["40%", "60%"],  # 饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        label_opts=opts.LabelOpts(formatter="{b}:{c}", is_show=True, position="center"),  # 标签配置项
    )
    .set_global_opts(  # 全局设置
        title_opts=opts.TitleOpts(  # 设置标题
            title="微博热搜话题类型占比分布",  # 名字
            pos_left="center",  # 组件距离容器左侧的位置
            pos_top="20",  # 组件距离容器上方的像素值
            title_textstyle_opts=opts.TextStyleOpts(color="#000"),  # 设置标题颜色
            ),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical", is_show=True),  # 图例配置项，参数 是否显示图里组件 # scroll滚动图例，vertical竖直显示
    )
    .set_series_opts(  # 系列设置
        tooltip_opts=opts.TooltipOpts(
            trigger="tr", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.4)", formatter="{b}: {c}"),  # 设置标签颜色
    )
    .render("../show/templates/show/weibodatadraw.html")
)

data_pair1 = [list(z) for z in zip(all_senti.keys(), all_senti.values())]   # 饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
(   # 初始化配置项，内部可设置颜色
    Pie(
        init_opts=opts.InitOpts(bg_color="#f0fcff") #2c343c
    )
    .add(
        series_name="微博热搜sentiment分析",  # 系列名称，即该饼图的名称
        data_pair=data_pair1,  # 系列数据项，格式为[(key1,value1),(key2,value2)]
        rosetype="radius",  # 通过半径区分数据大小 “radius” 和 “area” 两种
        radius="55%",  # 饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        # radius=["15%", "50%"],   # 饼图内圈和外圈的大小比例
        center=["50%", "50%"],  # 饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        label_opts=opts.LabelOpts(formatter="{b}:{c}", is_show=True, position="center"),  # 标签配置项
    )
    .set_global_opts(  # 全局设置
        title_opts=opts.TitleOpts(  # 设置标题
            title="微博热搜情感分析",  # 名字
            pos_left="center",  # 组件距离容器左侧的位置
            pos_top="20",  # 组件距离容器上方的像素值
            title_textstyle_opts=opts.TextStyleOpts(color="#000"),  # 设置标题颜色
            ),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical", is_show=True),  # 图例配置项，参数 是否显示图里组件 # scroll滚动图例，vertical竖直显示
    )
    .set_series_opts(  # 系列设置
        tooltip_opts=opts.TooltipOpts(
            trigger="tr", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.5)", formatter="{b}: {c}"),  # 设置标签颜色
    )
    .render("../show/templates/show/weibodatasenti.html")
)

bar = (
    Bar()
    .add_xaxis(["0-", "0.1-", "0.2-", "0.3-", "0.4-", "0.5-", "0.6-", "0.7-", "0.8-", "0.9-", "1"])
    .add_yaxis("情感分析数值分布", all_senti10)
)
bar.render("../show/templates/show/weibodatasentidis.html")

# # 一、分词
# print(s.words)
# # 二、词性标注
# tags = [x for x in s.tags]
# print(tags)
# # 三、断句
# print(s.sentences) # ['李达康就是这样的人', '她穷哭出声', '不攀龙附凤', '不结党营私', '不同流合污', '不贪污受贿', '也不伪造政绩', '手下贪污出事了他自责用人不当', '服装厂出事了他没想过隐瞒', '後面這些是繁體字']
# # 四、情绪判断，返回值为正面情绪的概率，越接近1表示正面情绪，越接近0表示负面情绪
# text1 = '周鸿祎不理解35岁被职场抛弃'
# text2 = '不工作真的会很开心吗'
# s1 = SnowNLP(text1)
# s2 = SnowNLP(text2)
# print(text1, s1.sentiments) # 这部电影真心棒，全程无尿点 0.9842572323704297
# print(text2, s2.sentiments) # 这部电影简直烂到爆 0.0566960891729531
# # 五、拼音
# print(s.pinyin)
# # ['li', 'da', 'kang', 'jiu', 'shi', 'zhe', 'yang', 'de', 'ren', '，', 'ta', 'qiong', 'ku', 'chu', 'sheng', '，', 'bu', 'pan', 'long', 'fu', 'feng', '，', 'bu', 'jie', 'dang', 'ying', 'si', '，', 'bu', 'tong', 'liu', 'he', 'wu', '，', 'bu', 'tan', 'wu', 'shou', 'hui', '，', 'ye', 'bu', 'wei', 'zao', 'zheng', 'ji', '，', 'shou', 'xia', 'tan', 'wu', 'chu', 'shi', 'liao', 'ta', 'zi', 'ze', 'yong', 'ren', 'bu', 'dang', '，', 'fu', 'zhuang', 'chang', 'chu', 'shi', 'liao', 'ta', 'mo', 'xiang', 'guo', 'yin', 'man', '，', '後', 'mian', '這', 'xie', 'shi', 'fan', '體', 'zi']
# # 六、繁体转简体
# print(s.han) # 李达康就是这样的人，她穷哭出声，不攀龙附凤，不结党营私，不同流合污，不贪污受贿，也不伪造政绩，手下贪污出事了他自责用人不当，服装厂出事了他没想过隐瞒，后面这些是繁体字
#
# # 七、关键字抽取
# text3 = '''
# 导语：360创始人周鸿祎在社交媒体表示，不知道为什么中国人好像35岁就老了，美国硅谷很多主力程序员都超过35岁。你没有写过十万行以上的代码，没有这种代码的积累，你不可能做一个优秀的程序员。
# '''
#
# s = SnowNLP(text3)
# print(s.keywords(limit=10)) # ['故宫', '年', '米', '外', '中心', '世界', '建筑', '北京', '宫', '保护']
#
# # 八、概括总结文章
# print(s.summary(limit=4)) # ['北京故宫 以 三 大殿 为 中心', '2012 年 1 月 至 2018 年 6 月', '[ 7 ]     2019 年 3 月 4 日', '北京故宫 于 明成祖 永乐 四年 （ 1406 年 ） 开始 建设']
#
#
# # 九、信息衡量
# '''
# TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。
#
# TF词频越大越重要，但是文中会的“的”，“你”等无意义词频很大，却信息量几乎为0，这种情况导致单纯看词频评价词语重要性是不准确的。因此加入了idf
#
# IDF的主要思想是：如果包含词条t的文档越少，也就是n越小，IDF越大，则说明词条t越重要
#
# TF-IDF综合起来，才能准确的综合的评价一词对文本的重要性。
# '''
# s = SnowNLP([
#     ['性格', '善良'],
#     ['温柔', '善良', '善良'],
#     ['温柔', '善良'],
#     ['好人'],
#     ['性格', '善良'],
# ])
# print(s.tf) # [{'性格': 1, '善良': 1}, {'温柔': 1, '善良': 2}, {'温柔': 1, '善良': 1}, {'好人': 1}, {'性格': 1, '善良': 1}]
# print(s.idf) # {'性格': 0.33647223662121295, '善良': -1.0986122886681098, '温柔': 0.33647223662121295, '好人': 1.0986122886681098}
#
#
# # 十、文本相似性
# print(s.sim(['温柔'])) # [0, 0.2746712135683371, 0.33647223662121295, 0, 0]
# print(s.sim(['善良'])) # [-1.0986122886681098, -1.3521382014376737, -1.0986122886681098, 0, -1.0986122886681098]
# print(s.sim(['好人'])) # [0, 0, 0, 1.4175642434427222, 0]