from random import randrange
from random import random

from flask import Flask, render_template
from flask.json import jsonify

# 注意导入对应图表
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Liquid
from pyecharts.charts import Pie
from pyecharts.faker import Faker
import pandas as pd
import numpy as np

# 读取CPU数据
cpu_info = pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + "2" + "/DataCollector01.csv")

for i in ['3', '4', '5', '6', '7']: # 拼接
    #print("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv")
    cpu_info = cpu_info.append(pd.read_csv("../dataset/cpu/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv"))

j = 0

# read mem info

memory_info = pd.read_csv(
    "../dataset/memory/DESKTOP-5GTCQEM_20221009-000434/DataCollector01.csv")

for i in ['5', '6', '7', '8', '9']:  # 拼接
    memory_info = memory_info.append(pd.read_csv(
        "../dataset/memory/DESKTOP-5GTCQEM_20221009-00043" + i + "/DataCollector01.csv"))

LiquidNum = 0 #水球图使用数据下标
barNum = 0 #折线图使用数据下标

# disk & network info

# 读取数据
disk_info = pd.read_csv("../dataset/disk/DESKTOP-5GTCQEM_20221009-000394/DataCollector01.csv")
network_info = pd.read_csv("../dataset/network/DESKTOP-5GTCQEM_20221009-000399/DataCollector01.csv")
# 读取数据
memory_info = pd.read_csv("../dataset/memory/DESKTOP-5GTCQEM_20221009-000434/DataCollector01.csv")

for i in ['5', '6', '7', '8', '9']:  # 拼接
    disk_info = disk_info.append(pd.read_csv(
        "../dataset/disk/DESKTOP-5GTCQEM_20221009-00039" + i + "/DataCollector01.csv"))

for i in ['0', '1', '2', '3', '4']:  # 拼接
    network_info = network_info.append(pd.read_csv(
        "../dataset/network/DESKTOP-5GTCQEM_20221009-00040" + i + "/DataCollector01.csv"))

for i in ['5', '6', '7', '8', '9']:  # 拼接
    memory_info = memory_info.append(pd.read_csv(
        "../dataset/memory/DESKTOP-5GTCQEM_20221009-00043" + i + "/DataCollector01.csv"))

tmp1 = disk_info['(PDH-CSV 4.0) (']
dd = np.array(tmp1)
time = dd.tolist()

tmp2 = disk_info['\\\\DESKTOP-5GTCQEM\\PhysicalDisk(1 C: E:)\\% Disk Time']
dd1 = np.array(tmp2)
disk_time = dd1.tolist()

tmp3 = disk_info['\\\\DESKTOP-5GTCQEM\\PhysicalDisk(1 C: E:)\\Avg. Disk sec/Transfer']
dd3 = np.array(tmp3)
transfer = dd3.tolist()

tmp4 = network_info['\\\\DESKTOP-5GTCQEM\\Network Interface(Realtek PCIe GbE Family Controller)\\Bytes Total/sec']
dd4 = np.array(tmp4)
sec = dd4.tolist()

app = Flask(__name__, static_folder="templates")

# CPU liquid
def liq_base() -> Liquid:
    global j
    c = (
        Liquid()
        .add("lq", [cpu_info['\\\\DESKTOP-5GTCQEM\\Processor(_Total)\\% Processor Time'].iat[j % 724] / 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="CPU Time"))
    )
    j = j + 1
    return c

#获取实时单条Mem内存数据，水球图使用
def MemoryUsage_base() -> Liquid:
    global LiquidNum
    c = (
        Liquid()
        .add("lq", [memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Committed Bytes'].iat[LiquidNum % 724] / memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Commit Limit'].iat[LiquidNum % 724]])
        .set_global_opts(title_opts=opts.TitleOpts(title="memory Usage"))
    )
    LiquidNum = LiquidNum + 1
    return c

#Mem折线图使用
def MemoryUsageThree_base():
    global barNum
    tNow = memory_info['(PDH-CSV 4.0) ('].iat[barNum % 724]
    print(tNow)
    tNow =tNow[11:19]
    Avail=memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Available Bytes'].iat[barNum % 724]/1024/1024/1024
    Committed=memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Committed Bytes'].iat[barNum % 724]/1024/1024/1024
    Limit=memory_info['\\\\DESKTOP-5GTCQEM\\Memory\\Commit Limit'].iat[barNum % 724]/1024/1024/1024
    Usage=(Committed/Limit)*100
    Avail=format(Avail, '.2f')
    Committed=format(Committed, '.2f')
    Limit=format(Limit, '.2f')
    Usage=format(Usage, '.2f')
    barNum= barNum+ 1
    return jsonify({"tNow": tNow, "avail": Avail,"Committed": Committed,"Limit": Limit,"Usage": Usage})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/memory")
def mem():
    return render_template("memory.html")

@app.route("/disk")
def ndisk_load():
    return render_template("disk.html")

@app.route("/network")
def network_load():
    return render_template("network.html")

#水球图使用，在用
@app.route("/MemoryUsage")
def get_MemoryUsage():
    c = MemoryUsage_base()
    return c.dump_options()

#回滚更新使用，在用
@app.route("/MemoryUsageThree")
def get_MemoryUsageThree():
    c = MemoryUsageThree_base()
    return c

@app.route("/liquid")
def get_liquid():
    c = liq_base()
    return c.dump_options()

ans = 0


@app.route('/diskData/')  # 路由
def setData():
    # now = datetime.datetime.now().strftime('%H:%M:%S')
    global ans
    now = time[ans][11:19]
    print('时间：', now)
    y = disk_time[ans % 724]
    #data = {'time':now,'data':random.randint(1,100)}
    data = {'time': now, 'data': y}
    print('数据：', data)
    ans = ans + 1
    return jsonify(data)  # 将数据以字典的形式传回


count0 = 0


@app.route('/diskData1/')  # 路由
def setData1():
    global count0
    now = time[count0][11:19]
    print('时间：', now)
    #y = '%.5f'%float(transfer[count0% 724])
    y = transfer[ count0 % 724]
    #data = {'time':now,'data':random.randint(1,100)}
    data = {'time': now, 'data': y}
    print('数据：', data)
    count0 = count0 + 1
    return jsonify(data)  # 将数据以字典的形式传回


count = 0


@app.route('/diskData2/')  # 路由
def setData2():
    global count
    now = time[count0][11:19]
    print('时间：', now)
    y = sec[count]
    #y2 = sec2[count]
    #data = {'time':now,'data':random.randint(1,100)}
    data = {'time': now, 'data': y}
    print('数据：', data)
    count = count + 1
    return jsonify(data)  # 将数据以字典的形式传回


if __name__ == "__main__":
    app.run()