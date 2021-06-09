from __future__ import absolute_import

import torch

from .dynamic_resnet20 import *
from .masked_resnet20 import *
from .resnet20 import *
from .sample_resnet20 import *
from .slimmable_resnet20 import *
from .supernet import *

__model_factory = {
    'dynamic': dynamic_resnet20,
    'masked': masked_resnet20,
    'original': resnet20,
    'sample': sample_resnet20,
    'slimmable': slimmable_resnet20,
    'super': SuperNet
}


def show_available_models():
    """Displays available models

    """
    print(list(__model_factory.keys()))


def build_model(name, num_classes=100):
    avai_models = list(__model_factory.keys())
    if name not in avai_models:
        raise KeyError(
            'Unknown model: {}. Must be one of {}'.format(name, avai_models)
        )
    return __model_factory[name]()
