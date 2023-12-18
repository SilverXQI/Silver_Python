import os
import pandas as pd
from pyecharts.charts import Timeline, Map
from pyecharts.options import TitleOpts, VisualMapOpts


def load_aqi_data_to_dict(folder_path):
    aqi_data_dict = {}

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            year_month = file_name.split('.')[0]  # 从文件名获取年月

            # 读取CSV文件
            data = pd.read_csv(file_path)

            # 将DataFrame转换为字典
            aqi_dict = dict(zip(data['Province'], data['AQI']))

            # 将转换后的字典添加到总字典中
            aqi_data_dict[year_month] = aqi_dict

    return aqi_data_dict


# 使用示例
folder_path = 'G:\\Data\\OutSecond'  # 替换为AQI数据文件夹的路径
aqi_data = load_aqi_data_to_dict(folder_path)

# 打印结果查看
for year_month, aqi in aqi_data.items():
    print(f"{year_month}: {aqi}")

timeline = Timeline()
for key, value in aqi_data.items():
    data_list = []
    for k, v in value.items():
        data_list.append((k, v))
    # 创建地图对象
    map = (
        Map()
        # 添加数据
        .add("各省空气污染状况", data_list, "china")
        # 设置全局配置，定制分段的视觉映射
        .set_global_opts(
            title_opts=TitleOpts(title="大气污染时空态势分析"),
            visualmap_opts=VisualMapOpts(
                is_show=True,  # 是否显示
                is_piecewise=True,  # 是否分段
                pieces=[
                    {"min": 1, "max": 9, "label": "1~9", "color": "#E0FFFF"},  # 浅蓝色
                    {"min": 10, "max": 19, "label": "10~19", "color": "#ADD8E6"},
                    {"min": 20, "max": 29, "label": "20~29", "color": "#87CEEB"},
                    {"min": 30, "max": 39, "label": "30~39", "color": "#6495ED"},
                    {"min": 40, "max": 49, "label": "40~49", "color": "#4169E1"},
                    {"min": 50, "max": 59, "label": "50~59", "color": "#1E90FF"},
                    {"min": 60, "max": 69, "label": "60~69", "color": "#0000FF"},
                    {"min": 70, "max": 79, "label": "70~79", "color": "#0000CD"},
                    {"min": 80, "max": 89, "label": "80~89", "color": "#00008B"},
                    {"min": 90, "max": 99, "label": "90~99", "color": "#191970"},  # 深蓝色
                    {"min": 100, "label": "100+", "color": "#8B0000"},  # 深红色
                ]

            )
        )
    )
    timeline.add(map, time_point=key)
# 绘图
timeline.render("AQI.html")
