from pyecharts import options as opts
from pyecharts.charts import Surface3D
import numpy as np


def generate_sphere_data(radius):
    data = []

    for theta in np.arange(0, 2 * np.pi, 0.1):
        for phi in np.arange(0, np.pi, 0.1):
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            data.append([x, y, z])
    return data


sphere_data = generate_sphere_data(5)

surface3d = (
    Surface3D()
    .add(
        series_name="Ball",
        data=sphere_data,
        xaxis3d_opts=opts.Axis3DOpts(type_="value", min_=-5, max_=5),
        yaxis3d_opts=opts.Axis3DOpts(type_="value", min_=-5, max_=5),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", min_=-5, max_=5),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=0,
            max_=5,
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
        title_opts=opts.TitleOpts(title='3、球面（半径为5）'),
    )
)

surface3d.render("work3_3.html")
