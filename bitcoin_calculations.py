import math


def AttackerSuccessProbability(q):
    z = 1
    p = 1.0 - q
    this_lambda = z * (q / p)
    summation = 1.0
    for k in range(z):
        poisson = math.exp(-this_lambda)
        for j in range(1, k):
            poisson *= this_lambda / j
        summation -= poisson * (1 - pow(q / p, z - k))
    return summation


def solve_for_P(P):
    for k in range(10, 45):
        q = k / 100

        print('q=' + str(q))









for i in range(1, 10):
    parameter = i * 5 / 100
    print(AttackerSuccessProbability(parameter))
