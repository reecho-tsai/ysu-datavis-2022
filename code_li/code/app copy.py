import os
from random import randrange
from random import random

from flask.json import jsonify
from flask import Flask, render_template

# 注意导入对应图表
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.charts import Liquid
from pyecharts.charts import Pie
from pyecharts.faker import Faker
import pandas as pd
import datetime  # 导入时间和随机数模块:


# os.chdir("E:\\专业课资料\\5大三 上\\数据可视化\\燕山大学第一届数据可视化挑战赛介绍/code")  # 将执行目录切换到代码所在目录

# 读取数据
memory_info = pd.read_csv(
    "../dataset/memory/DESKTOP-5GTCQEM_20221009-000434/DataCollector01.csv")

for i in ['5', '6', '7', '8', '9']:  # 拼接
    memory_info = memory_info.append(pd.read_csv(
        "../dataset/memory/DESKTOP-5GTCQEM_20221009-00043" + i + "/DataCollector01.csv"))

LiquidNum = 0  # 水球图使用数据下标
barNum = 0  # 折线图使用数据下标

app = Flask(__name__, static_folder="templates")

# 获取实时单条Mem内存数据，水球图使用


def MemoryUsage_base() -> Liquid:
    global LiquidNum
    c = (
        Liquid()
        .add("lq", [memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Committed Bytes'].iat[LiquidNum % 724] / memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Commit Limit'].iat[LiquidNum % 724]])
        .set_global_opts(title_opts=opts.TitleOpts(title="memory Usage"), visualmap_opts=opts.VisualMapOpts(precision=2))
    )
    LiquidNum = LiquidNum + 1
    return c

# 获取实时单条Mem内存数据，折线图使用


def get_MemoryUsageOnce():
    global barNum
    c = memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Committed Bytes'].iat[barNum %
                                                                        724] / memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Commit Limit'].iat[barNum % 724]
    barNum = barNum + 1
    return c

# Mem折线图使用


def MemoryUsageThree_base():
    global barNum
    tNow = memory_info['(PDH-CSV 4.0) ('].iat[barNum % 724]
    print(tNow)
    tNow = tNow[11:19]
    Avail = memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Available Bytes'].iat[barNum %
                                                                            724]/1024/1024/1024
    Committed = memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Committed Bytes'].iat[barNum %
                                                                                724]/1024/1024/1024
    Limit = memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Commit Limit'].iat[barNum %
                                                                         724]/1024/1024/1024
    Usage = Committed/Limit
    Avail = format(Avail, '.2f')
    Committed = format(Committed, '.2f')
    Limit = format(Limit, '.2f')
    Usage = format(Usage, '.2f')
    barNum = barNum + 1
    return jsonify({"tNow": tNow, "avail": Avail, "Committed": Committed, "Limit": Limit, "Usage": Usage})


# 初始化折线图
def MemoryUsageList_base() -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(num) for num in range(10)])
        .add_yaxis(
            series_name="",
            y_axis=[get_MemoryUsageOnce() for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Mem"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@app.route("/")
def index():
    return render_template("index.html")

# 水球图使用，在用


@app.route("/MemoryUsage")
def get_MemoryUsage():
    c = MemoryUsage_base()
    return c.dump_options()

# 增量更新使用，备用


@app.route("/MemoryUsageLine")
def get_MemoryUsageList():
    c = MemoryUsageList_base()
    return c.dump_options()


@app.route("/MemoryUsageData")
def get_MemoryUsageData():
    global barNum
    c = get_MemoryUsageOnce()
    return jsonify({"name": barNum-1, "value": c})  # 将数据以字典形式传回

# 回滚更新使用，备用


@app.route("/MemoryUsageTime")
def get_MemoryUsageTime():
    now = datetime.datetime.now().strftime('%H:%M:%S')
    c = get_MemoryUsageOnce()
    return jsonify({"time": now, "data": c})  # 将数据以字典形式传回

# 回滚更新使用，在用


@app.route("/MemoryUsageThree")
def get_MemoryUsageThree():
    c = MemoryUsageThree_base()
    return c


if __name__ == "__main__":
    app.run()
