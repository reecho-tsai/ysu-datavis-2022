from random import randrange
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Bar

import pandas as pd

i = 0

app = Flask(__name__, static_folder="templates")
cpu_info = pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + "2" + "/DataCollector01.csv")

for i in ['3', '4', '5', '6', '7']:
    #print("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv")
    cpu_info = cpu_info.append(pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv"))

cpu_time = cpu_info['\\\\DESKTOP-5GTCQEM\\Processor(_Total)\\% Processor Time']

def bar_base() -> Bar:
    global i
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例" + str(i), subtitle="我是副标题"))
    )
    i = i + 1
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()
