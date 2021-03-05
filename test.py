import numpy as np

data = np.random.randint(-15, 15, size=100).reshape(10, 10)
print(data)

first_mean = np.mean(data, axis=0)
print(first_mean)
mask1 = first_mean >= data
compare1 = np.array(np.sum(mask1, axis=0) > np.sum(~mask1, axis=0), dtype=int)

tmp1 = mask1 & compare1
tmp2 = ~mask1 & ~compare1
mask = tmp1 | tmp2

second_mean = np.sum(data * mask, axis=0) / np.sum(mask, axis=0)
print(second_mean)
mask2 = second_mean >= data
tmp1 = mask2 & mask
tmp2 = ~mask2 & mask
compare2 = np.array(np.sum(tmp1, axis=0) > np.sum(tmp2, axis=0), dtype=int)

mask = (tmp1 & compare2) | (tmp2 & ~compare2)
print(mask)
print(data[np.argmax(np.sum(mask, axis=1)), :])
print(np.sum(data * mask, axis=0) / np.sum(mask, axis=0))
