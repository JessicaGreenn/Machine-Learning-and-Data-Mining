import os
import sys

from pyecharts.commons.utils import JsCode

#sys.path.append(os.path.dirname(os.path.abspath('.')))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'  # 导入项目下的settings.py
# 手动初始化Django：
#import django

#django.setup()
#from show.models import data

from pyecharts.charts import Bar, Pie, Radar
from pyecharts import options as opts  # 用于设值全局配置和系列配置
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'
import pandas as pd
data = pd.read_csv("datascrapy.csv")
print(data.shape)
#data1 = pd.DataFrame(data)
weibodata = data.loc[data['platform'] == '微博']
print(weibodata)
temp = data.groupby('platform').count()['name'].reset_index().sort_values(by='name',ascending=False)
print(temp)


category_num_dictw = {}
for resou in weibodata.values:
    print(resou[4])
    category_num_dictw.setdefault(resou[4], 0)
    category_num_dictw[resou[4]] += 1

total_w = sum(category_num_dictw.values())
print(total_w)

data_pairw = sorted(category_num_dictw.items(), key=lambda x: x[1], reverse=True)
# data_pair = [list(z) for z in zip(category_num_dict.keys(), category_num_dict.values())]   # 饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
(  # 初始化配置项，内部可设置颜色
    Pie(
        init_opts=opts.InitOpts(bg_color="#f0fcff")
    )
        .add(
        series_name="微博热搜tags分析",  # 系列名称，即该饼图的名称
        data_pair=data_pairw,  # 系列数据项，格式为[(key1,value1),(key2,value2)]
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
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical", is_show=True),
        # 图例配置项，参数 是否显示图里组件 # scroll滚动图例，vertical竖直显示
    )
        .set_series_opts(  # 系列设置
        tooltip_opts=opts.TooltipOpts(
            trigger="tr", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.4)", formatter="{b}: {c}"),  # 设置标签颜色
    )
        .render("./weibo.html")
)

zhihudata = data.loc[data['platform'] == '知乎']

category_num_dictz = {'未知': 0}
for resou in zhihudata.values:
    if resou[4]:
        category_num_dictz.setdefault(resou[4], 0)
        category_num_dictz[resou[4]] += 1
    else:
        category_num_dictz['未知'] += 1

total_z = sum(category_num_dictz.values())
print(total_z)

data_pairz = sorted(category_num_dictz.items(), key=lambda x: x[1], reverse=True)
# data_pair = [list(z) for z in zip(category_num_dict.keys(), category_num_dict.values())]   # 饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
(  # 初始化配置项，内部可设置颜色
    Pie(
        init_opts=opts.InitOpts(bg_color="#f0fcff")
    )
        .add(
        series_name="知乎热搜tags分析",  # 系列名称，即该饼图的名称
        data_pair=data_pairz,  # 系列数据项，格式为[(key1,value1),(key2,value2)]
        rosetype="radius",  # 通过半径区分数据大小 “radius” 和 “area” 两种
        radius="55%",  # 饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        # radius=["15%", "50%"],   # 饼图内圈和外圈的大小比例
        center=["40%", "60%"],  # 饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        label_opts=opts.LabelOpts(formatter="{b}:{c}", is_show=True, position="center"),  # 标签配置项
    )
        .set_global_opts(  # 全局设置
        title_opts=opts.TitleOpts(  # 设置标题
            title="知乎热搜话题类型占比分布",  # 名字
            pos_left="center",  # 组件距离容器左侧的位置
            pos_top="20",  # 组件距离容器上方的像素值
            title_textstyle_opts=opts.TextStyleOpts(color="#000"),  # 设置标题颜色
        ),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical", is_show=True),
        # 图例配置项，参数 是否显示图里组件 # scroll滚动图例，vertical竖直显示
    )
        .set_series_opts(  # 系列设置
        tooltip_opts=opts.TooltipOpts(
            trigger="tr", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.4)", formatter="{b}: {c}"),  # 设置标签颜色
    )
        .render("./zhihu.html")
)

print(category_num_dictw)
print(category_num_dictz)

df = pd.DataFrame(0, index=category_num_dictw.keys(), columns=['微博', '知乎'])
df.loc[:, '微博'] = category_num_dictw.values()

for ca in df.index:
    df.loc[ca, '知乎'] = category_num_dictz[ca]
df = df.drop(index=['未知'])
print(df)

df.plot.bar(stacked=False, alpha=0.5)
plt.title('微博知乎热搜类型对比')
# plt.show()

df1 = df.copy(deep=True)  # 深拷贝, df=df1只是引用
for ca in df.index:
    df1.loc[ca, '微博'] = df.loc[ca, '微博'] / (total_w - category_num_dictw['未知'])
    df1.loc[ca, '知乎'] = df.loc[ca, '知乎'] / (total_z - category_num_dictz['未知'])
print(df1)
df1.plot.bar(stacked=False, alpha=0.5)
plt.title('微博知乎各类热搜占比对比')
# plt.show()

# 从指定时间段读取数据库
'''from django.utils import timezone
from datetime import timedelta

now = timezone.now()
# start = now - timedelta(hours=23,minutes=59,seconds=59)  # 过去24h的一天内
start = now - timedelta(hours=now.hour + 24 * 13, minutes=now.minute, seconds=now.second)  # 从今天零点开始的今天内
print(start)
end = start + timedelta(hours=23, minutes=59, seconds=59)
print(end)
# CurrentDayData = data.objects.filter(date__gt=start, platform='知乎')
weibodata_time = data.objects.filter(date__range=(start, end), platform='微博')
zhihudata_time = data.objects.filter(date__range=(start, end), platform='知乎')
df_time = pd.DataFrame(0, index=category_num_dictw.keys(), columns=['微博', '知乎'])

for resou in weibodata_time:
    if resou.category:
        df_time.loc[resou.category, '微博'] += 1
    else:
        df_time.loc['未知', '微博'] += 1
for resou in zhihudata_time:
    if resou.category:
        df_time.loc[resou.category, '知乎'] += 1
    else:
        df_time.loc['未知', '知乎'] += 1

print(df_time)
total_w_day = sum(df_time.loc[:, '微博'])
total_z_day = sum(df_time.loc[:, '知乎'])
total_w_day_weizhi = df_time.loc['未知', '微博']
total_z_day_weizhi = df_time.loc['未知', '知乎']
print(total_w_day, total_z_day, total_w_day_weizhi, total_z_day_weizhi)

df_time = df_time.drop(index=['未知'])
df_time.plot.bar(stacked=False, alpha=0.5)
plt.title('2月23日微博知乎热搜类型对比')
#plt.show()

df1_time = df_time
for ca in df.index:
    df1_time.loc[ca, '微博'] = df_time.loc[ca, '微博'] / (total_w_day - total_w_day_weizhi)
    df1_time.loc[ca, '知乎'] = df_time.loc[ca, '知乎'] / (total_z_day - total_z_day_weizhi)
print(df1_time)
df1_time.plot.bar(stacked=False, alpha=0.5)
plt.title('2月23日微博知乎各类热搜占比对比')
#plt.show()
'''

# 雷达图
def resou_radar(v1, v2, maxv, timeflag):
    radar1 = (
        Radar()
            .add_schema(  # 添加schema架构
            schema=[
                opts.RadarIndicatorItem(name='社会', max_=maxv),  # 设置指示器名称和最大值
                opts.RadarIndicatorItem(name='职场', max_=maxv),
                opts.RadarIndicatorItem(name='时事', max_=maxv),
                opts.RadarIndicatorItem(name='娱乐', max_=maxv),
                opts.RadarIndicatorItem(name='财经', max_=maxv),
                opts.RadarIndicatorItem(name='情感', max_=maxv),
                opts.RadarIndicatorItem(name='知识&教育', max_=maxv),
                opts.RadarIndicatorItem(name='搞笑', max_=maxv),
                opts.RadarIndicatorItem(name='体育', max_=maxv),
                opts.RadarIndicatorItem(name='生活', max_=maxv),
                opts.RadarIndicatorItem(name='ACGM', max_=maxv),
                opts.RadarIndicatorItem(name='科技', max_=maxv),
                opts.RadarIndicatorItem(name='健康', max_=maxv),
            ],
            # shape='circle'  # 设置雷达图类型圆形
        )
            .add('微博', [v1], color="#f9713c", label_opts=opts.LabelOpts(formatter=JsCode("function (params) {return "
                                                                                         "params.value + '%'}")))  #
            # 添加一条数据，参数1为数据名，参数2为数据，参数3为颜色
            .add('知乎', [v2], color="#4169E1", label_opts=opts.LabelOpts(formatter=JsCode("function (params) {return "
                                                                                         "params.value + '%'}")))
            .set_global_opts(title_opts=opts.TitleOpts(title='雷达图'),
                             )
    )
    if timeflag:
        radar1.render('radar_time.html')
    else:
        radar1.render('radar.html')


v1 = df1['微博'].tolist()  # 数据必须为二维数组，否则会集中一个指示器显示
for i in range(len(v1)):
    v1[i] = round(v1[i] * 100, 1)
print(v1)
v2 = df1['知乎'].tolist()
for i in range(len(v2)):
    v2[i] = round(v2[i] * 100, 1)
print(v2)

resou_radar(v1, v2, maxv=30, timeflag=False)


'''v1 = df1_time['微博'].tolist()
for i in range(len(v1)):
    v1[i] = round(v1[i] * 100, 1)
print(v1)

v2 = df1_time['知乎'].tolist()
for i in range(len(v2)):
    v2[i] = round(v2[i] * 100, 1)
print(v2)

resou_radar(v1, v2, maxv=44, timeflag=True)
'''


# 序列距离
def seq_distance(wcnd, zcnd):
    print(1)


def seq_distance_time(wcndt, zcndt):
    print(2)


seq_distance(category_num_dictw, category_num_dictz)
# seq_distance_time(category_num_dictw_time , category_num_dictztime)