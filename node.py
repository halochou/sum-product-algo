import numpy as np
from scipy.misc import logsumexp

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.income = {}
        # self.received = set()
        # self.converged = False

    def __repr__(self):
        return self.name

    def gen_msg(self, name):
        assert False

    def normalize_msg(self, msg):
        assert len(msg.shape) == 1
        # msg = msg - logsumexp(msg)
        msg = msg / msg.sum()

        return msg

    def recv(self, src, msg):
        # print(src, '->', self.name, msg)
        self.income[src] = msg
        # self.received.add(src)
        # if len(self.received) == len(self.income):
            # print(self.name, 'converged')

    def update(self):
        for name, node in self.neighbors.items():
            msg = self.gen_msg(name)
            node.recv(self.name, msg)
            # node.income[self.name] = msg

    def send(self, target):
        msg = self.gen_msg(target)
        self.neighbors[target].recv(self.name, msg)