import math
import pyecharts.options as opts
from pyecharts.charts import Line3D

week_en = "Saturday Friday Thursday Wednesday Tuesday Monday Sunday".split()
clock = (
    "12a 1a 2a 3a 4a 5a 6a 7a 8a 9a 10a 11a 12p "
    "1p 2p 3p 4p 5p 6p 7p 8p 9p 10p 11p".split()
)

print(clock)
data = []
for t in range(0, 25000):
    _t = t / 1000
    x = 5 * math.cos(_t)
    y = 5 * math.sin(_t)
    z = 0.5 * _t
    data.append([x, y, z])

(
    Line3D()
    .add(
        "",
        data,
        xaxis3d_opts=opts.Axis3DOpts(data=clock, type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(data=week_en, type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            dimension=2,
            max_=15,
            min_=0,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        ),
        title_opts=opts.TitleOpts(title='●	1、螺旋曲线（半径为5，每旋转一周z坐标增加π，弹簧）'),
    )
    .render("work3_1.html")
)
