import math
from typing import Union

import pyecharts.options as opts
from pyecharts.charts import Surface3D


def float_range(start: int, end: int, step: Union[int, float], round_number: int = 2):
    temp = []
    while True:
        if start < end:
            temp.append(round(start, round_number))
            start += step
        else:
            break
    return temp


def surface3d_data():
    for t0 in float_range(-5, 5, 0.05):
        y = t0
        for t1 in float_range(-5, 5, 0.05):
            x = t1
            z = math.exp((x ** 2 + y ** 2) * (-0.5)) * (1 / (2 * math.pi))
            yield [x, y, z]


(
    Surface3D()
    .add(
        series_name="",
        shading="color",
        data=list(surface3d_data()),
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, height=40, depth=100),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            dimension=2,
            max_=1,
            min_=-1,
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
        title_opts=opts.TitleOpts(title='2、二维正态分布曲面（标准正态分布）'),
    )
    .render("work3_2.html")
)
