# -*- coding: utf-8 -*-


import torch
import torchvision
import numpy as np


def load_data_fashion_mnist(id, batch_size, resize=None, root='./Data/FashionMNIST', num_workers=20):
    """Download the fashion mnist dataset and then load into memory."""
    trans = []
    if resize:
        trans.append(torchvision.transforms.Resize(size=resize))
    trans.append(torchvision.transforms.ToTensor())

    transform = torchvision.transforms.Compose(trans)
    mnist_train = torchvision.datasets.FashionMNIST(root=root, train=True, download=True, transform=transform)
    mnist_test = torchvision.datasets.FashionMNIST(root=root, train=False, download=True, transform=transform)

    shuffle_dataset = True
    indices = list(range(len(mnist_train)))
    print(len(mnist_train))
    random_seed = 42

    train_split_length = int(len(mnist_train) / num_workers)
    test_split_length = int(len(mnist_test) / num_workers)

    print(train_split_length)
    print(test_split_length)
    if shuffle_dataset:
        np.random.seed(random_seed)
        np.random.shuffle(indices)
    train_sub_indices = indices[id * train_split_length: (id + 1) * train_split_length]
    test_sub_indices = indices[id * test_split_length: (id + 1) * test_split_length]

    train_sampler = torch.utils.data.SubsetRandomSampler(train_sub_indices, generator=None)
    test_sampler = torch.utils.data.SubsetRandomSampler(test_sub_indices, generator=None)

    train_iter = torch.utils.data.DataLoader(mnist_train, batch_size=batch_size, num_workers=0,
                                             sampler=train_sampler)
    test_iter = torch.utils.data.DataLoader(mnist_test, batch_size=batch_size, num_workers=0,
                                            sampler=test_sampler)

    return train_iter, test_iter
