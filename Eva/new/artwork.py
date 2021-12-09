import ast

import matplotlib.pyplot as plt
import numpy as np


def read_data(file, rows):
    y = np.zeros((rows, 120))
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
                tmp = line.strip().split(" ")[1:121]
                tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
                t = np.array(tmp) + t

            flag += 1

    return y


files = ['mean.txt', 'median.txt', 'krum.txt', 'kaiyun.txt']
rows = [13, 13, 13, 13]

# tmp, str = [], ''
# for i, file in enumerate(files):
#     y = read_data(file, rows[i])
#     print(file)
#     str += "{:.2f} \n".format(y[0][119])
#     for j in range(1, 13):
#         str += "{:.2f} {} ".format(y[j][119], '&')
#         if j % 3 == 0:
#             str += "\n"
#
#     print(str)
#
#     str = ''
# print(y[12][119])
# for j in range(13):
#     print(y[j][119])
# break

fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(10, 9))
plt.subplots_adjust(wspace=0.1, hspace=0.1)

methods = ['Mean', 'Median', 'Krum', 'Ours']
attacks = ['Gaussian', 'Model negation', 'Grad_Scale', 'Label shift']
line_color = ['r', 'b', 'g', 'm']
x_label = ['(a', '(b', '(c', '(d']
x_label3 = ['(a3)\n epochs', '(b3)\n epochs', '(c3)\n epochs', '(d3)\n epochs']
x = np.arange(1, 121, 1)

for i, file in enumerate(files):
    y = read_data(file, rows[i])
    for j in range(4):
        ax[j, i].plot(x, y[0], color=line_color[3], linestyle="-", linewidth=1.0, label='0%')
        ax[j, i].plot(x, y[j * 3 + 1], color=line_color[1], linestyle="-.", linewidth=1.0, label='10%')
        ax[j, i].plot(x, y[j * 3 + 2], color=line_color[0], linestyle="--", linewidth=1.0, label='25%')
        ax[j, i].plot(x, y[j * 3 + 3], color=line_color[2], linestyle=":", linewidth=1.0, label='50%')

        # ax[j, i].legend(loc='lower right', title="Byzantine", fontsize='x-small')
        ax[j, i].set_rasterized(True)
        ax[j, i].set_yticks(np.arange(0, 100, 20))

for i in range(len(files)):
    for j in range(3):
        ax[j, i].set_xlabel(x_label[i] + str(j) + ')', fontsize=12)

fontsize = 12
for i in range(4):
    ax[i, 0].set_ylabel("Top-1 Acc.(%)", fontsize=fontsize)

    ax[i, 3].set_ylabel(attacks[i], fontsize=fontsize)
    ax[i, 3].yaxis.set_label_position("right")
for i in range(4):
    ax[3, i].set_xlabel(x_label3[i], fontsize=fontsize)
    ax[0, i].set_title(methods[i], fontsize=fontsize)

fig.tight_layout()

fig.subplots_adjust(top=0.8, bottom=0.15)
ax.flatten()[-3].legend(title="Byzantine workers", loc='upper center', bbox_to_anchor=(1, -0.55), ncol=4)

# plt.savefig('test.eps', dpi=200, format='eps')
plt.savefig('test.pdf')
plt.show()
