import plotly.graph_objects as go
import pandas as pd
data = pd.read_csv("datascrapy.csv")
weibodata = data.loc[data['platform'] == '微博']
zhihudata = data.loc[data['platform'] == '知乎']
category_num_dictw1, category_num_dictw2 = {}, {}
for resou1 in weibodata.values:
#   print(resou1[4])
    category_num_dictw1[resou1[4]] = category_num_dictw1.get(resou1[4], 0) + 1
#    category_num_dictw.setdefault(resou[4], 0)
#    category_num_dictw[resou[4]] += 1
for resou2 in zhihudata.values:
#    print(resou2[4])
    category_num_dictw2[resou2[4]] = category_num_dictw2.get(resou2[4], 0) + 1
labels = list(category_num_dictw1.keys())
print(labels)
NODES = dict(
label = ['微博', '知乎'] + labels,
    color = ['dodgerblue', 'seagreen'] + ['silver'] * 14,)
#color = ["seagreen",'darkgreen', "seagreen", 'dodgerblue', 'blue', 'darkviolet', 'pink', 'yellow', 'orange', "red", 'black', 'grey', 'gold', "silver", "brown", "chocolate" ],)

LINKS = dict(
  source = [0] * 14 + [1] * 14, # 链接的起点或源节点
  target = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] * 2, # 链接的目的地或目标节点
  value =  list(category_num_dictw1.values()) + list(category_num_dictw2.values()), # 链接的宽度（数量）
  color = ['lightskyblue'] * 14 + ['lightseagreen'] * 14,)
# 链接的颜色
# 目标节点：       3-Gold          4-Silver        5-Bronze
#  color = [
#  "seagreen", "dodgerblue", 'blue', 'darkviolet', 'pink', 'yellow', "orange", 'red', 'black', 'grey', "gold", "silver", "brown",'chocolate' ,
#  "seagreen", "dodgerblue", 'blue', 'darkviolet', 'pink', 'yellow', "orange", 'red', 'black', 'grey', "gold", "silver", "brown", 'chocolate',
#  ],)
data = go.Sankey(node = NODES, link = LINKS)
fig = go.Figure(data)
fig.show()
