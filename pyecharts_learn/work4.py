from datetime import datetime

import pandas as pd
from pyecharts.charts import Map, Timeline
from pyecharts.options import TitleOpts, VisualMapOpts

# 读取数据
dataframe = pd.read_excel('CityData.xlsx')
provinceName = dataframe['provinceName'].tolist()[::-1]
cityName = dataframe['cityName'].tolist()[::-1]
city_confirmedCount = dataframe['city_confirmedCount'].tolist()[::-1]
updateTime = dataframe['updateTime'].tolist()[::-1]
updateTime_datatime = [0] * len(updateTime)
# 设置截止时间
deadline_time = datetime(2020, 4, 1, 0, 0, 0)
temp = provinceName[0]
province_confirmedCount_sum = {temp: 0}
city_confirmedCount_sum = {}
# 获取所有省份名称
for i in range(len(provinceName)):
    p = provinceName[i]
    if p == temp:
        continue
    else:
        temp = p
        if temp not in province_confirmedCount_sum:
            province_confirmedCount_sum[temp] = 0
# print(province_confirmedCount_sum)
# 数据处理
for i in range(len(updateTime)):
    t = updateTime[i]
    if t <= deadline_time:
        province_confirmedCount_sum[provinceName[i]] += city_confirmedCount[i]
        if updateTime[i + 1] != t:
            city_confirmedCount_sum[t] = province_confirmedCount_sum.copy()
            # print(province_confirmedCount_sum)
    else:
        continue

# print(city_confirmedCount_sum)
# for key, value in city_confirmedCount_sum.items():
#     print(key, value)
# 创建时间轴实例
timeline = Timeline()
for key, value in city_confirmedCount_sum.items():
    data_list = []
    for k, v in value.items():
        data_list.append((k, v))
    # 创建地图对象
    map = (
        Map()
        # 添加数据
        .add("各省确诊人数", data_list, "china")
        # 设置全局配置，定制分段的视觉映射
        .set_global_opts(
            title_opts=TitleOpts(title="2020年全国新冠患者人数随时间的变化过程"),
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
    )
    timeline.add(map, time_point=key)
# 绘图
timeline.render("全国疫情地图.html")
