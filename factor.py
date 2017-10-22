import numpy as np
from functools import reduce
from scipy.misc import logsumexp
from node import Node

class Factor(Node):
    def __init__(self, name, neighbors, mat, mode='spa'):
        super().__init__(name)

        assert tuple([nbr.dim for name, nbr in sorted(neighbors.items())]) == mat.shape

        self.neighbors = neighbors
        self.mat = mat
        self.mode = mode
        self.free_vars = sorted(neighbors.keys())

        for var in neighbors.values():
            self.income[var.name] = np.ones((var.dim,))
            var.neighbors[self.name] = self
            var.income[self.name] = np.ones((var.dim,))

    def gen_msg(self, down_name):
        def gen_shape(name, dim):
            index = self.free_vars.index(name)
            shape = [1 for _ in self.free_vars]
            shape[index] = dim
            return tuple(shape)

        up_names = sorted(list(set(self.income.keys()) - {down_name}))
        if len(up_names) == 0:
            return self.mat
        ups = [self.income[up_name].reshape(gen_shape(up_name, self.neighbors[up_name].dim)) for up_name in up_names]
        msg = reduce(np.multiply, ups)
        msg = msg * self.mat
        target_index = self.free_vars.index(down_name)
        squeeze_axis = tuple(sorted(list(set(range(len(self.free_vars))) - {target_index})))
        # msg = logsumexp(msg, axis=squeeze_axis)
        if self.mode == 'spa':
            msg = np.sum(msg, axis=squeeze_axis, keepdims=False)
        elif self.mode == 'mpa':
            msg = np.max(msg, axis=squeeze_axis, keepdims=False)
        else:
            assert False
        msg = self.normalize_msg(msg)

        return msg
