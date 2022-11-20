import os
import pandas as pd
import matplotlib.pyplot as plt

# 包含五个元素列表的一个图形
#如果输入的参数只是一个一维的列表，那么这个数组会被当成y轴处理，x轴是列表的索引

plt.ylabel("grade")  #y轴增加标签
plt.savefig('te01',dpi=600)  #dpi是指每个英寸包含600个像素点（质量挺高的了）
plt.show()
os.chdir("D:\\燕山大学第一届数据可视化挑战赛介绍\\code")#将执行目录切换到代码所在目录
cpu_data_path="..\\dataset\\cpu\\DESKTOP-5GTCQEM_20221009-000402\\DataCollector01.csv"#数据相对路径
disk_data_path="..\\dataset\\disk\\DESKTOP-5GTCQEM_20221009-000394\\DataCollector01.csv"#数据相对路径
memory_data_path="..\\dataset\\memory\\DESKTOP-5GTCQEM_20221009-000434\\DataCollector01.csv"#数据相对路径
network_data_path="..\\dataset\\network\\DESKTOP-5GTCQEM_20221009-000399\\DataCollector01.csv"#数据相对路径
data = pd.read_csv( memory_data_path)#读取数据
#print(data)#打印数据
#print(data.describe())#计算基本的统计数据
#print(data.head(3))#前三行
#print(data.loc[8])#第九行
#print(data.loc[range(4,6)])#第四到第六行（左闭右开）的数据子集
#row_index = data.index.values  # 行号： 数组形式<class 'numpy.ndarray'> [0 1 2 3 4 5 6 7 8]
#print('行号是：%s' % row_index)
#col_index = data.columns.values  # 列名： 数组形式<class 'numpy.ndarray'>['姓名' '性别' '年龄' '住址' '爱好']
#print('列名是：%s' % col_index)
row_num = len(data.index.values)  # 行数
print('行数是：%s' % row_num)
col_num = len(data.columns.values)  # 列数
print('列数是：%s' % col_num)
for i in range(1,col_num):
    colunm_name=data.columns.values[i]#按索引下标从列名数组中获取列名
    print(i,": ",colunm_name,data[colunm_name].describe())#打印
    plt.plot(data[colunm_name].astype(float))#调用plt画图，数据为data中按列名索引的数据并强转为float类型
    plt.xlabel(colunm_name)  #x轴增加标签列名
    #plt.savefig('te01',dpi=600)  #保存文件，路径和dpi
    plt.show(block=False)#不设block=False系统会认为这是一个可交互窗口，会等在这里不往下走
    plt.pause(1)#暂停一秒等待
    plt.close()#关闭当前窗口，继续往下走
