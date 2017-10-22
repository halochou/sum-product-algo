import numpy as np
from sum_product import SumProduct
from utils import hamming74_check_mat, normal_distr_mat, gen_signal
from math import sqrt
from random import choice

contents = [
    [0,0,0,0,0,0,0],
    [1,1,1,0,0,0,0],
    [1,0,0,1,1,0,0],
    [0,1,1,1,1,0,0],
    [0,1,0,1,0,1,0],
    [1,0,1,1,0,1,0],
    [1,1,0,0,1,1,0],
    [0,0,1,0,1,1,0],
    [1,1,0,1,0,0,1],
    [0,0,1,1,0,0,1],
    [0,1,0,0,1,0,1],
    [1,0,1,0,1,0,1],
    [1,0,0,0,0,1,1],
    [0,1,1,0,0,1,1],
    [0,0,0,1,1,1,1],
    [1,1,1,1,1,1,1]]

def build_graph(z, sigma, mode):
    G = SumProduct()
    G.add_var('x1', [0, 1])
    G.add_var('x2', [0, 1])
    G.add_var('x3', [0, 1])
    G.add_var('x4', [0, 1])
    G.add_var('x5', [0, 1])
    G.add_var('x6', [0, 1])
    G.add_var('x7', [0, 1])
    G.add_fac('f1', ['x1', 'x3', 'x5', 'x7'], hamming74_check_mat(), mode=mode)
    G.add_fac('f2', ['x2', 'x3', 'x6', 'x7'], hamming74_check_mat(), mode=mode)
    G.add_fac('f3', ['x4', 'x5', 'x6', 'x7'], hamming74_check_mat(), mode=mode)
    G.add_fac('p1', ['x1'], normal_distr_mat(z[0], sigma), mode=mode)
    G.add_fac('p2', ['x2'], normal_distr_mat(z[1], sigma), mode=mode)
    G.add_fac('p3', ['x3'], normal_distr_mat(z[2], sigma), mode=mode)
    G.add_fac('p4', ['x4'], normal_distr_mat(z[3], sigma), mode=mode)
    G.add_fac('p5', ['x5'], normal_distr_mat(z[4], sigma), mode=mode)
    G.add_fac('p6', ['x6'], normal_distr_mat(z[5], sigma), mode=mode)
    G.add_fac('p7', ['x7'], normal_distr_mat(z[6], sigma), mode=mode)

    return G

def test(content, sigma, mode):
    x, _, z = gen_signal(content, sigma)
    G = build_graph(z, sigma, mode)
    G.run(20)
    decoded = G.decode()
    diff = x - decoded
    num_errors = diff[diff!=0].shape[0]

    return num_errors

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('num_test', type=int, help='Times of test')
    parser.add_argument('deviation', type=float, help='Deviation of noise')
    parser.add_argument('mode', help='[spa | mpa]')
    args = parser.parse_args()

    sigma = sqrt(args.deviation)
    num_test = args.num_test
    error = 0
    print('Number of test:', args.num_test)
    print('Deviation', args.deviation)
    for i in range(num_test):
        # content = choice(contents)
        content = contents[0]
        new_error = test(content, sigma, args.mode)
        error += new_error
        # if new_error != 0:
            # print('new error:', new_error)
    bit_error_prob = error / (7 * num_test)
    print('Total error:', error)
    print('BER', bit_error_prob)
