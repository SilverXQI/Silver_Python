import pandas as pd
from pyecharts.charts import Map
from pyecharts.options import TitleOpts, VisualMapOpts

dataframe = pd.read_excel('CityData.xlsx')
countryName = dataframe['countryName'].tolist()
provinceName = dataframe['provinceName'].tolist()
cityName = dataframe['cityName'].tolist()
city_confirmedCount = dataframe['city_confirmedCount'].tolist()
city_suspectedCount = dataframe['city_suspectedCount'].tolist()
city_curedCount = dataframe['city_curedCount'].tolist()
city_deadCount = dataframe['city_deadCount'].tolist()
updateTime = dataframe['updateTime'].tolist()
temp = provinceName[0]
data_dict = {temp: 0}
print(len(provinceName))
for i in range(len(provinceName)):
    p = provinceName[i]
    # print(p)
    if p == temp:
        data_dict[temp] += city_confirmedCount[i]
    else:
        temp = p
        if temp not in data_dict:
            data_dict[temp] = 0
        data_dict[temp] += city_confirmedCount[i]

data_list = list(tuple(data_dict.items()))
print(data_list)
# 创建地图对象
map = Map()
# 添加数据
map.add("各省确诊人数", data_list, "china")
# 设置全局配置，定制分段的视觉映射
map.set_global_opts(
    title_opts=TitleOpts(title="全国疫情地图"),
    visualmap_opts=VisualMapOpts(
        is_show=True,  # 是否显示
        is_piecewise=True,  # 是否分段
        pieces=[
            {"min": 1, "max": 99, "lable": "1~99人", "color": "#CCFFFF"},
            {"min": 100, "max": 999, "lable": "100~9999人", "color": "#FFFF99"},
            {"min": 1000, "max": 4999, "lable": "1000~4999人", "color": "#FF9966"},
            {"min": 5000, "max": 9999, "lable": "5000~99999人", "color": "#FF6666"},
            {"min": 10000, "max": 99999, "lable": "10000~99999人", "color": "#CC3333"},
            {"min": 100000, "lable": "100000+", "color": "#990033"},
        ]
    )
)
# 绘图
map.render("全国疫情地图.html")
