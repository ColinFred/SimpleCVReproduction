# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
import torch
from torchvision import transforms
from torchvision.datasets import CIFAR100


class Cutout(object):
    def __init__(self, length):
        self.length = length

    def __call__(self, img):
        h, w = img.size(1), img.size(2)
        mask = np.ones((h, w), np.float32)
        y = np.random.randint(h)
        x = np.random.randint(w)

        y1 = np.clip(y - self.length // 2, 0, h)
        y2 = np.clip(y + self.length // 2, 0, h)
        x1 = np.clip(x - self.length // 2, 0, w)
        x2 = np.clip(x + self.length // 2, 0, w)

        mask[y1: y2, x1: x2] = 0.
        mask = torch.from_numpy(mask)
        mask = mask.expand_as(img)
        img *= mask

        return img

def get_dataset(cls, cutout_length=0):
    MEAN = [0.5071, 0.4865, 0.4409]
    STD = [0.1942, 0.1918, 0.1958]
    transf = [
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),

    ]
    normalize = [
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD)
    ]
    cutout = []
    if cutout_length > 0:
        cutout.append(Cutout(cutout_length))

    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomResizedCrop((32,32)),
        transforms.ColorJitter(0.2,0.2,0.2,0.2),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD)
    ])
    valid_transform = transforms.Compose(normalize)

    if cls == "cifar100":
        dataset_train = CIFAR100(
            root="./data", train=True, download=True, transform=train_transform)
        dataset_valid = CIFAR100(
            root="./data", train=False, download=True, transform=valid_transform)
    else:
        raise NotImplementedError
    return dataset_train, dataset_valid

dataset_train, dataset_valid = get_dataset("cifar100")

train_loader = torch.utils.data.DataLoader(dataset_train, batch_size=4, shuffle=True, num_workers=2)

print(len(dataset_train), len(train_loader))