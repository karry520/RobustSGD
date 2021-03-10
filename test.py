import numpy as np

data = np.random.randint(0, 100, size=7 * 44426).reshape(7, 44426)
y = np.random.randint(0, 100, size=7).reshape(7, 1)
y_mean = np.mean(y, axis=0)
print(np.mean(data, axis=0).shape)
print(y_mean)
rst = data * y
print(data.shape)
print(y.shape)
print(rst.shape)
