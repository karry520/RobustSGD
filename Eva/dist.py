import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import ast


def static(data, bin):
    rst = [0 for i in range(bin + 1)]
    data_min = np.min(data)
    data_max = np.max(data)

    for i in data:
        dis = data_max - data_min
        index = (i - data_min) * bin / dis
        # print(int(index))
        rst[int(index)] += 1
    return rst


Data, Mu, Sigma, Max, Min = [], [], [], [], []
with open('grad.txt', 'r') as f:
    t, flag = [0], 0
    for line in f.readlines():
        tmp = line.strip().split(" ")
        flag += 1

        tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
        Data += tmp
        Mu += [np.mean(tmp)]
        Sigma += [np.var(tmp)]

        Max += [np.max(tmp)]
        Min += [np.min(tmp)]
# for i in range(int(len(Data) / 20)):
#     rst = []
#     rst = static(Data[i * 20:(i + 1) * 20], 4)
#     print(rst)
# y1 = static(Data[0:20], 4)
# y2 = static(Data[20:40], 4)
#
Data = np.array(Data)
Mu = np.repeat(Mu, 20)
Sigma = np.repeat(Sigma, 20)
stand_data = (Data - Mu) / Sigma

Max = np.repeat(Max, 20)
Min = np.repeat(Min, 20)
nomal_data = ((Data - Min) / (Max - Min))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()  # 设置seaborn默认格式
np.random.seed(0)  # 设置随机种子数
plt.rcParams['figure.figsize'] = (13, 5)
f = plt.figure()  # 确定画布
# plt.hist(Data[20:40], bins=20, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
f.add_subplot(1, 2, 1)
sns.distplot(nomal_data[100:120], bins=6,  kde=True,
             kde_kws={"color": "b", "alpha": 0.2, "linewidth": 1, "shade": True})  # 绘制频数直方图
plt.ylabel("Frequency", fontsize=10)
plt.xlabel("Values", fontsize=10)
plt.title("(a)", fontsize=12)
f.add_subplot(1, 2, 2)
sns.distplot(nomal_data[20:40], bins=6, kde=True,
             kde_kws={"color": "b", "alpha": 0.2, "linewidth": 1, "shade": True})  # 绘制密度直方图
plt.ylabel("Frequency", fontsize=10)
plt.xlabel("Values", fontsize=10)



plt.subplots_adjust(wspace=0.3)  # 调整两幅子图的间距
plt.show()

# x = np.arange(0, len(stand_data), 1)
#
# plt.plot(x, stand_data)
# plt.show()

# print(y)
# fig, ax = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 6))
#
# methods = ['Median', 'Trimmed mean', 'Krum', 'Ours']
# attacks = ['Label shift', 'Gaussian', 'Model negation', 'Grad_Scale']
# line_color = ['r', 'b', 'g']
#
# x = np.arange(1, 31, 1)
#
# # y_major_locator = MultipleLocator(0.05)
#
# for i in range(2):
#     for j in range(2):
#         ax[i, j].set_title(attacks[i * 2 + j])
#         ax[i, j].plot(x, y[i * 2 + j + 0], color=line_color[0], linestyle="--", linewidth=1.0, label='25%')
#         ax[i, j].plot(x, y[i * 2 + j + 4], color=line_color[1], linestyle="-.", linewidth=1.0, label='10%')
#         ax[i, j].plot(x, y[i * 2 + j + 8], color=line_color[2], linestyle=":", linewidth=1.0, label='50%')
#         ax[i, j].set_ylabel("Accuracy")
#         ax[i, j].set_xlabel('epochs')
#         # ax[i, j].yaxis.set_major_locator(y_major_locator)
#
#         ax[i, j].legend(loc='lower right', title="Byzantine")
# # plt.savefig('test.eps', dpi=600, format='eps')
# # plt.show()
