#sentimentAnalysis.py
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

data = pd.read_csv("datascrapy.csv")
weibodata = data.loc[data['platform'] == '微博']
zhihudata = data.loc[data['platform'] == '知乎']
category_num_dictw1, category_num_dictw2 = {}, {}
for resou1 in weibodata.values:
    if 0 <= float(resou1[13]) <= 0.2:
        category_num_dictw1['消极'] = category_num_dictw1.get('消极', 0) + 1
    if 0.2 <= float(resou1[13]) <= 0.4:
        category_num_dictw1['较消极'] = category_num_dictw1.get('较消极', 0) + 1
    if 0.4 <= float(resou1[13]) <= 0.6:
        category_num_dictw1['中性'] = category_num_dictw1.get('中性', 0) + 1
    if 0.6 <= float(resou1[13]) <= 0.8:
        category_num_dictw1['较积极'] = category_num_dictw1.get('较积极', 0) + 1
    if 0.8 <= float(resou1[13]) <= 1.0:
        category_num_dictw1['积极'] = category_num_dictw1.get('积极', 0) + 1

for resou2 in zhihudata.values:
    if 0 <= float(resou2[13]) <= 0.2:
        category_num_dictw2['消极'] = category_num_dictw2.get('消极', 0) + 1
    if 0.2 <= float(resou2[13]) <= 0.4:
        category_num_dictw2['较消极'] = category_num_dictw2.get('较消极', 0) + 1
    if 0.4 <= float(resou2[13]) <= 0.6:
        category_num_dictw2['中性'] = category_num_dictw2.get('中性', 0) + 1
    if 0.6 <= float(resou2[13]) <= 0.8:
        category_num_dictw2['较积极'] = category_num_dictw2.get('较积极', 0) + 1
    if 0.8 <= float(resou2[13]) <= 1.0:
        category_num_dictw2['积极'] = category_num_dictw2.get('积极', 0) + 1
# 十四个领域
fields1 = list(category_num_dictw1.keys())
fields2 = list(category_num_dictw2.keys())
# 多少条
num1 = list(category_num_dictw1.values())
num2 = list(category_num_dictw2.values())

# 颜色集设置
color_series = ['#FAE927','#9ECB3C','#3DBA78','#1E91CA','#2D3D8E',
                '#7D3990','#D52178', '#D44C2D','#D99D21','#CF7B25']
# 排序版：按照满意度排序的结果输出图形
# 创建数据框
df = pd.DataFrame({'fields': fields1, 'num': num1})
# 降序排序
df.sort_values(by='num', ascending=False, inplace=True)
# 提取数据
v = df['fields'].values.tolist()
d = df['num'].values.tolist()

# 实例化Pie类
pie1 = Pie(init_opts=opts.InitOpts(width='800px', height='1350px'))

# 设置颜色
pie1.set_colors(color_series)

# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie1.add("", [list(z) for z in zip(v, d)],radius=["20%", "60%"],center=["30%", "30%"],rosetype="area",is_clockwise=False)

# 设置全局配置项
pie1.set_global_opts(title_opts=opts.TitleOpts(title='微博热搜情感分布'),
                     legend_opts=opts.LegendOpts(is_show=False),toolbox_opts=opts.ToolboxOpts())

# 设置系列配置项
pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside",
                                               font_size=12,formatter="{b}:{c}条", font_weight="bold", font_family="Microsoft YaHei"))

# 生成html文档
pie1.render('WeiboHSD-ranked.html')

#知乎数据以此类推
df = pd.DataFrame({'fields': fields2, 'num': num2})
df.sort_values(by='num', ascending=False, inplace=True)

v = df['fields'].values.tolist()
d = df['num'].values.tolist()

pie2 = Pie(init_opts=opts.InitOpts(width='800px', height='1350px'))

pie2.set_colors(color_series)

pie2.add("", [list(z) for z in zip(v, d)],radius=["20%", "60%"],center=["30%", "30%"],rosetype="area",is_clockwise=False)

pie2.set_global_opts(title_opts=opts.TitleOpts(title='知乎热搜情感分布'),
                     legend_opts=opts.LegendOpts(is_show=False),toolbox_opts=opts.ToolboxOpts())

pie2.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside",
                                               font_size=12,formatter="{b}:{c}条", font_weight="bold", font_family="Microsoft YaHei"))

pie2.render('ZhihuHSD-ranked.html')
