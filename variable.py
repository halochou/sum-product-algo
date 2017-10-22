import numpy as np
from functools import reduce
from node import Node

class Variable(Node):
    def __init__(self, name, values):
        super().__init__(name)
        self.dim = len(values)
        self.values = values

    def gen_msg(self, down_name):
        up_names = sorted(list(set(self.income.keys()) - {down_name}))
        if len(up_names) == 0:
            return np.ones((self.dim,))
        ups = [self.income[up_name] for up_name in up_names]
        msg = reduce(np.multiply, ups)
        msg = self.normalize_msg(msg)
        return msg

    def gen_marginal(self):
        self.marginal = reduce(np.multiply, self.income.values())
        self.marginal = self.normalize_msg(self.marginal)
        # self.marginal = np.exp(self.marginal)