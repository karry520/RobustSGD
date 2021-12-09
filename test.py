import numpy as np

grad = np.random.randint(0,10, size=15)
grad.shape = (3, 5)
print(grad)
grad = np.delete(grad, 0, axis=0)
print(grad)
