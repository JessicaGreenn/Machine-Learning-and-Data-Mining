# 首先需要导入我们需要使用的包，其中pandas用于数据整理，pyecharts用于绘图
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
data = pd.read_csv("datascrapy.csv")
weibodata = data.loc[data['platform'] == '微博']

zhihudata = data.loc[data['platform'] == '知乎']
category_num_dictw1, category_num_dictw2 = {}, {}
count1, count2 = 0, 0
for resou1 in weibodata.values:
    if resou1[4] == None:
        continue
    count1 += 1
    category_num_dictw1[resou1[4]] = category_num_dictw1.get(resou1[4], 0) + 1
print(count1)
# 十四个领域
fields1 = list(category_num_dictw1.keys())


# 多少条
num1 = list(category_num_dictw1.values())
for resou2 in zhihudata.values:
    if resou2[4] == None:
        continue
    count2 += 1
    category_num_dictw2[resou2[4]] = category_num_dictw2.get(resou2[4], 0) + 1
print(category_num_dictw2)
del category_num_dictw2['社会;江苏;热点话题;人口贩运;徐州丰县生育八孩女子事件']
category_num_dictw2['社会'] += 1
del category_num_dictw2['宽带;中国联通;通信;网速;套餐']
category_num_dictw2['科技'] += 1
del category_num_dictw2['其他']
category_num_dictw2['未知'] += 2
del category_num_dictw2['荣耀']
category_num_dictw2['科技'] += 3
for k in list(category_num_dictw2.keys()):
    if category_num_dictw2[k] == 22:
        del category_num_dictw2[k]

category_num_dictw2['未知'] += 22


print(count2)
# 十四个领域
fields2 = list(category_num_dictw2.keys())
# 多少条
num2 = list(category_num_dictw2.values())

# 颜色集设置
color_series = ['#FAE927','#9ECB3C','#3DBA78','#1E91CA','#2D3D8E', '#7D3990','#D52178',
                '#D44C2D','#D99D21','#CF7B25', '#FAE927','#9ECB3C','#3DBA78','#1E91CA']
'''
# 定序版：按十四个领域的顺序输出图形
# 创建数据框
df = pd.DataFrame({'fields': fields, 'num': num})
# 降序排序
# df.sort_values(by='num', ascending=True, inplace=True)
# 提取数据
v = df['fields'].values.tolist()
d = df['num'].values.tolist()

# 实例化Pie类
pie1 = Pie(init_opts=opts.InitOpts(width='800px', height='1350px'))

# 设置颜色
pie1.set_colors(color_series)

# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie1.add("", [list(z) for z in zip(v, d)],radius=["20%", "90%"],center=["30%", "30%"],rosetype="area",is_clockwise=False)

# 设置全局配置项
pie1.set_global_opts(title_opts=opts.TitleOpts(title='Hot Topics Distribution'),
                     legend_opts=opts.LegendOpts(is_show=False),toolbox_opts=opts.ToolboxOpts())

# 设置系列配置项
pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", 
                                               font_size=12,formatter="{b}:{c}条", font_weight="bold", font_family="Microsoft YaHei"))

# 生成html文档
pie1.render('Hot Topics Distribution.html')
'''
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
pie1.add("", [list(z) for z in zip(v, d)],radius=["20%", "90%"],center=["30%", "30%"],rosetype="area",is_clockwise=False)

# 设置全局配置项
pie1.set_global_opts(title_opts=opts.TitleOpts(title='微博热搜话题分布'),
                     legend_opts=opts.LegendOpts(is_show=False),toolbox_opts=opts.ToolboxOpts())

# 设置系列配置项
pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", 
                                               font_size=12,formatter="{b}:{c}条", font_weight="bold", font_family="Microsoft YaHei"))

# 生成html文档
pie1.render('WeiboHTD-ranked.html')

#知乎数据以此类推
df = pd.DataFrame({'fields': fields2, 'num': num2})
df.sort_values(by='num', ascending=False, inplace=True)

v = df['fields'].values.tolist()
d = df['num'].values.tolist()

pie2 = Pie(init_opts=opts.InitOpts(width='800px', height='1350px'))

pie2.set_colors(color_series)

pie2.add("", [list(z) for z in zip(v, d)],radius=["20%", "50%"],center=["30%", "30%"],rosetype="area",is_clockwise=False)

pie2.set_global_opts(title_opts=opts.TitleOpts(title='知乎热搜话题分布'),
                     legend_opts=opts.LegendOpts(is_show=False),toolbox_opts=opts.ToolboxOpts())

pie2.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside",
                                               font_size=12,formatter="{b}:{c}条", font_weight="bold", font_family="Microsoft YaHei"))

pie2.render('ZhihuHTD-ranked.html')
