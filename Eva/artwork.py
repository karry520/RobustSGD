import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import ast


# y = np.zeros((13, 30))
# with open('kaiyun.txt', 'r') as f:
#     t, flag = [0], 0
#     for line in f.readlines():
#         # print("flag:", flag)
#         if line[0] != '0':
#             continue
#         flag += 1
#         if int(flag % 10) == 0:
#             # print(t[25])
#             t = np.array(t) / 9
#             y[int(flag / 10) - 1] = t * 100
#             t = [0]
#         else:
#             tmp = line.strip().split(" ")[1:31]
#             tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
#             t = np.array(tmp) + t


def read_data(file, rows):
    y = np.zeros((rows, 30))
    with open(file, 'r') as f:
        t, flag = [0], 1
        for line in f.readlines():
            if line[0] != '0':
                continue
            if int(flag % 10) == 0:
                t = np.array(t) / 9
                y[int(flag / 10) - 1] = t * 100
                t = [0]
            else:
                tmp = line.strip().split(" ")[1:31]
                tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
                t = np.array(tmp) + t

            flag += 1

    return y


# gaussian, model_neg, grad_scal, label_inv = [], [], [], []
# a, b, c,d = [], [], [], []
# for i in range(3):
#     gaussian = y[i * 4][29]
#     model_neg = y[i * 4 + 1][29]
#     grad_scal = y[i * 4 + 2][29]
#     label_inv = y[i * 4 + 3][29]
#
#     a += ["%.2f $" % gaussian]
#     b += ["%.2f $" % model_neg]
#     c += ["%.2f $" % grad_scal]
#     d += ["%.2f $" % label_inv]
# print(a)
# print(b)
# print(c)
# print(d)
# print(y)
fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(14, 10))
plt.subplots_adjust(wspace=0.1, hspace=0.1)

methods = ['Mean', 'Median', 'Krum', 'Ours']
attacks = ['Label shift', 'Gaussian', 'Model negation', 'Grad_Scale']
line_color = ['r', 'b', 'g', 'm']

# files = ['mean.txt', 'median.txt', 'krum.txt', 'kaiyun.txt']
# rows = [5, 13, 13, 13]
files = ['median.txt', 'krum.txt', 'kaiyun.txt']
rows = [13, 13, 13]

x = np.arange(1, 31, 1)

for i, file in enumerate(files):
    y = read_data(file, rows[i])
    for j in range(4):
        ax[j, i].plot(x, y[-1], color=line_color[3], linestyle="-", linewidth=1.0, label='0%')
        ax[j, i].plot(x, y[i * 3], color=line_color[1], linestyle="-.", linewidth=1.0, label='10%')
        ax[j, i].plot(x, y[i * 3 + 3], color=line_color[0], linestyle="--", linewidth=1.0, label='25%')
        ax[j, i].plot(x, y[i * 3 + 6], color=line_color[2], linestyle=":", linewidth=1.0, label='50%')

        ax[j, i].legend(loc='lower right', title="Byzantine")

for i in range(4):
    ax[i, 0].set_ylabel("Top-1 Acc.(%)")
    ax[3, i].set_xlabel('epochs')
    ax[0, i].set_title(methods[i])
    ax[i, 3].set_ylabel(attacks[i])
    ax[i, 3].yaxis.set_label_position("right")
# plt.savefig('test.eps', dpi=600, format='eps')
plt.show()
