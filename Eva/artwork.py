import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import ast

y = np.zeros((13, 30))
with open('bak/kaiyun.txt', 'r') as f:
    t, flag = [0], 0
    for line in f.readlines():
        # print("flag:", flag)
        if line[0] != '0':
            continue
        flag += 1
        if int(flag % 10) == 0:
            # print(t[25])
            t = np.array(t) / 9
            y[int(flag / 10) - 1] = t * 100
            t = [0]
        else:
            tmp = line.strip().split(" ")[1:31]
            tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
            t = np.array(tmp) + t

# gaussian, model_neg, grad_scal, label_inv = [], [], [], []
a, b, c,d = [], [], [], []
for i in range(3):
    gaussian = y[i * 4][29]
    model_neg = y[i * 4 + 1][29]
    grad_scal = y[i * 4 + 2][29]
    label_inv = y[i * 4 + 3][29]

    a += ["%.2f $" % gaussian]
    b += ["%.2f $" % model_neg]
    c += ["%.2f $" % grad_scal]
    d += ["%.2f $" % label_inv]
print(a)
print(b)
print(c)
print(d)
# print(y)
# fig, ax = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 6))
# plt.subplots_adjust(wspace=0.2, hspace=0.3)
#
# methods = ['Median', 'Trimmed mean', 'Krum', 'Ours']
# attacks = ['(a) Label shift', '(b) Gaussian', '(c) Model negation', '(d) Grad_Scale']
# line_color = ['r', 'b', 'g', 'm']
#
# x = np.arange(1, 31, 1)
#
#
# # y_major_locator = MultipleLocator(0.05)
#
# for i in range(2):
#     for j in range(2):
#         ax[i, j].set_title(attacks[i * 2 + j])
#         ax[i, j].plot(x, y[i * 2 + j + 8], color=line_color[2], linestyle=":", linewidth=1.0, label='50%')
#         ax[i, j].plot(x, y[i * 2 + j + 0], color=line_color[0], linestyle="--", linewidth=1.0, label='25%')
#         ax[i, j].plot(x, y[i * 2 + j + 4], color=line_color[1], linestyle="-.", linewidth=1.0, label='10%')
#         ax[i, j].plot(x, y[-1], color=line_color[3], linestyle="-", linewidth=1.0, label='0%')
#         ax[i, j].set_ylabel("Top-1 Acc.(%)")
#         ax[i, j].set_xlabel('epochs')
#         # ax[i, j].yaxis.set_major_locator(y_major_locator)
#
#         ax[i, j].legend(loc='lower right', title="Byzantine")
# plt.savefig('test.eps', dpi=600, format='eps')
# plt.show()
