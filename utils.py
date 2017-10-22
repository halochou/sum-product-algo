import numpy as np
from math import sqrt, exp, pi

def hamming74_check_mat():
    mat = np.zeros((2,2,2,2))
    v = [0, 1]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    s = (v[i] + v[j] + v[k] + v[l]) % 2
                    mat[i, j, k, l] = 1 if s == 0 else 1e-10
    return mat

def normal_distr_mat(z, sigma):
    def normal(x, u, sigma):
        return 1/(sqrt(2*pi*sigma**2)) * exp(-1 * (x-u)**2/(2*sigma**2))
    # from scipy.stats import norm
    # normal = lambda x, u, sigma: norm.pdf(x, loc=u, scale=sigma)
    mat = np.zeros((2,))
    x = [1, -1]
    for i in range(2):
        mat[i] = normal(z, x[i], sigma)
    return mat

# def normal_distr_mat(z, sigma):
#     p = lambda x, z, n: (1 + exp(-2 * x * z / n)) ** (-1)
#     N0 = sigma ** 2 * 2
#     mat = np.zeros((2,))
#     mat[0] = p(1, z, N0)
#     mat[1] = p(-1, z, N0)
#     return mat

def gen_signal(content, sigma):
    x = np.array(content)
    y = -1 * (x * 2 - 1)
    n = np.random.normal(0, sigma, 7)
    return x, y, tuple(y + n)