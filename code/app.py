from random import randrange
from random import random

from flask import Flask, render_template

# 注意导入对应图表
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Liquid
from pyecharts.charts import Pie
from pyecharts.faker import Faker
import pandas as pd

# 读取数据
cpu_info = pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + "2" + "/DataCollector01.csv")

for i in ['3', '4', '5', '6', '7']: # 拼接
    #print("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv")
    cpu_info = cpu_info.append(pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv"))

i = 0

app = Flask(__name__, static_folder="templates")

# 画图
def bar_base() -> Bar: # demo
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

# 注意缩进要严格一致
def liq_base() -> Liquid:
    global i
    c = (
        Liquid()
        .add("lq", [cpu_info['\\\\DESKTOP-5GTCQEM\\Processor(_Total)\\% Processor Time'].iat[i % 724] / 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="CPU Time"))
    )
    i = i + 1
    return c

def pie_base() -> Pie:
    c = (
    Pie()
        .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@app.route("/liquid")
def get_liquid():
    c = liq_base()
    return c.dump_options()

@app.route("/pie")
def get_pie():
    c = pie_base()
    return c.dump_options()

if __name__ == "__main__":
    app.run()