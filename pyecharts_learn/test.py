from pyecharts import options as opts
from pyecharts.charts import Line, Timeline

# 创建时间序列数据
time_series = ["2020", "2021", "2022"]
data_2020 = [120, 150, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]
data_2021 = [130, 160, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370]
data_2022 = [140, 170, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380]

# 创建时间轴实例
timeline = Timeline()

# 为每个年份创建图表并添加到时间轴
for year, data in zip(time_series, [data_2020, data_2021, data_2022]):
    line = (
        Line()
        .add_xaxis(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        .add_yaxis("Sales", data)
        .set_global_opts(title_opts=opts.TitleOpts("Sales Data - " + year))
    )
    timeline.add(line, time_point=year)

# 渲染图表
timeline.render("timeline_chart.html")
