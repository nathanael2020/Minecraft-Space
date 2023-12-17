from settings import SEED
from numba import njit
from opensimplex.internals import _noise2, _noise3, _init
from opensimplex import random_seed
from random import random

perm, perm_grad_index3 = _init(seed=int(random() * 196659000))


@njit(cache=True)
def noise2(x, y):
#    perm, perm_grad_index3 = _init(random_seed())
    return _noise2(x, y, perm)


@njit(cache=True)
def noise3(x, y, z):
#    perm, perm_grad_index3 = _init(random_seed())
    return _noise3(x, y, z, perm, perm_grad_index3)
