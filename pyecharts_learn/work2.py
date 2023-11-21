import random
from pyecharts import options as opts
from pyecharts.charts import Bar3D

data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
with open("daily-minimum-temperatures-in-me.csv", "r") as f:
    data = f.read()
data = data.split('\n')
data = data[1:-1]
data = [d.split(',') for d in data]

data = data[0:-2]
for i in range(len(data)):
    data[i][0] = data[i][0][1:-1].split('-')
time = []
for i in range(365):
    time.append(data[i][0][1] + '-' + data[i][0][2])
c = (
    Bar3D()
    .add(
        "",
        [[f"{d[0][1]}-{d[0][2]}", d[0][0], d[1]] for d in data],
        xaxis3d_opts=opts.Axis3DOpts(time, type_="category"),
        yaxis3d_opts=opts.Axis3DOpts([(i + 1980) for i in range(10)], type_="category"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=20),
        title_opts=opts.TitleOpts(title="Daily minimum temperatures in Melbourne, Australia, 1981-1990"),
    )
    .render("work2.html")
)
