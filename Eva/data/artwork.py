import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import ast


def read_data(file, rows, type):
    y = np.zeros((rows, 120))
    with open(file, 'r') as f:
        t, flag, state = [0], 1, 1
        for line in f.readlines():
            if line[0] != '0':
                continue
            elif state % 2 != 0:
                if int(flag % 10) == 0:
                    t = np.array(t) / 9
                    y[int(flag / 10) - 1] = t * 100
                    t = [0]
                else:
                    tmp = line.strip().split(" ")[1:121]
                    tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
                    t = np.array(tmp) + t

                flag += 1
                state += 1
            else:
                state += 1
                continue
    if type == 'acc':
        return [y[i] for i in range(rows) if i % 2 == 0]
    elif type == 'loss':
        return [y[i] for i in range(rows) if i % 2 != 0]
    else:
        return y


files = ['mean.txt', 'median.txt',  'kaiyun.txt']
rows = [26, 26, 26]


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

fig, ax = plt.subplots(4, 3, sharex=True, sharey=True, figsize=(10, 9))
plt.subplots_adjust(wspace=0.1, hspace=0.1)

methods = ['Mean', 'Median', 'Ours']
attacks = ['Gaussian', 'Model negation', 'Grad_Scale', 'Label shift']
line_color = ['r', 'b', 'g', 'm']

x = np.arange(1, 121, 1)

for i, file in enumerate(files):
    y = read_data(file, rows[i], 'acc')
    for j in range(4):
        ax[j, i].plot(x, y[0], color=line_color[3], linestyle="-", linewidth=1.0, label='0%')
        ax[j, i].plot(x, y[j * 3 + 1], color=line_color[1], linestyle="-.", linewidth=1.0, label='10%')
        ax[j, i].plot(x, y[j * 3 + 2], color=line_color[0], linestyle="--", linewidth=1.0, label='25%')
        ax[j, i].plot(x, y[j * 3 + 3], color=line_color[2], linestyle=":", linewidth=1.0, label='50%')

        ax[j, i].legend(loc='lower right', title="Byzantine", fontsize='x-small')
        ax[j, i].set_rasterized(True)
        ax[j, i].set_yticks(np.arange(0, 100, 20))

for i in range(4):
    ax[i, 0].set_ylabel("Top-1 Acc.(%)")

    ax[i, 2].set_ylabel(attacks[i])
    ax[i, 2].yaxis.set_label_position("right")
for i in range(3):
    ax[3, i].set_xlabel('epochs')
    ax[0, i].set_title(methods[i])
fig.tight_layout()
# plt.savefig('test.eps', dpi=600, format='eps')
# plt.savefig('test.jpg')
plt.show()
