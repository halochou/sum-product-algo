import numpy as np
from variable import Variable
from factor import Factor
from random import randrange

class SumProduct:
    def __init__(self):
        self.vars = {}
        self.factors = {}

    def add_var(self, name, values):
        self.vars[name] = Variable(name, values)

    def add_fac(self, name, nbr_names, mat, mode):
        neighbors = dict([(name, self.vars[name]) for name in nbr_names])
        self.factors[name] = Factor(name, neighbors, mat, mode)

    def _gen_all_marginal(self):
        for var in self.vars.values():
            var.gen_marginal()
            # if var.marginal[0] >= 0.5:
            #     print('MARGINAL:', var.name, var.marginal, '\t0')
            # else:
            #     print('MARGINAL:', var.name, var.marginal, '\t1')

    def run(self, iteration=20):
        for _ in range(iteration):
            for factor in self.factors.values():
                factor.update()
            for var in self.vars.values():
                var.update()

    def decode(self):
        self._gen_all_marginal()
        marginals = [(name, var.marginal) for name, var in self.vars.items()]
        # decoded = [0 if marginal[0] >= marginal[1] else 1 for name, marginal in sorted(marginals)]
        decoded = []
        for name, marginal in sorted(marginals):
            if marginal[0] > marginal[1]:
                decoded.append(0)
            elif marginal[0] < marginal[1]:
                decoded.append(1)
            else:
                decoded.append(randrange(0, 2))

        return np.array(decoded)
