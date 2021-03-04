import numpy as np

data_in = np.random.randint(0, 100, size=20).reshape(4,5).tolist()
print(data_in)
# data_in[0] = np.random.normal(0, 2, len(data_in[0])).tolist()


tmp = data_in[0]
data_in[0] = (-(np.sum(data_in, axis=0) - data_in[0])).tolist()


print(data_in)
