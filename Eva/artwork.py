import matplotlib.pyplot as plt
import numpy as np
import ast

y = np.zeros((9, 19))
with open('kaiyun.txt', 'r') as f:
    t, flag = [0], 0
    for line in f.readlines():
        print("flag:", flag)
        if line[0] != '0':
            continue
        flag += 1
        if int(flag % 5) == 0:
            t = np.array(t) / 5
            y[int(flag / 5) - 1] = t
            t = [0]
        else:
            print(len(line))
            tmp = line.strip().split(" ")[1:20]
            tmp = [ast.literal_eval(tmp[i]) for i in range(len(tmp))]
            t = np.array(tmp) + t

print(y)
fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(10, 10))

methods = ['Median', 'Trimmed mean', 'Krum', 'Ours']
attacks = ['Label shift', 'Gaussian', 'Model negation', 'Grad_Scale']
line_color = ['r', 'b', 'g']

for i in range(4):
    ax[0, i].set_title(methods[i])
    ax[i, 0].set_ylabel("Accuracy")
    ax[i, 3].set_ylabel(attacks[i])
    ax[i, 3].yaxis.set_label_position("right")
    ax[3, i].set_xlabel('epoch')

x = np.arange(0, 19, 1)

for i in range(4):
    ax[i, 3].plot(x, y[i], color=line_color[0], linestyle="--", linewidth=1.0)
    ax[i, 3].plot(x, y[-1], color=line_color[1], linestyle="--", linewidth=1.0)
    ax[i, 3].plot(x, y[i+4], color=line_color[2], linestyle="--", linewidth=1.0)

plt.show()
