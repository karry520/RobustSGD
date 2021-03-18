import numpy as np

a = np.random.randint(0, 10, size=40).reshape((20, -1)).tolist()
print(a)
s = [a[i][1] for i in range(20)]
print(s)
tmp = ""
for i in s:
    tmp += str(i) + " "
# for i in s:
#     tmp += s[i]
with open("Eva/grad.txt", 'a+') as f:
    f.write(tmp)
    f.write('\n')
