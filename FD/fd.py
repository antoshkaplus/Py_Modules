
# solving Laplace equation

def Laplace(i, j, func, delta_x, delta_y):
    b = delta_x / delta_y
    b_sqr = b*b
    F = func
    return (F(i+1,j) + F(i-1,j) + b_sqr * (F(i,j+1) + F(i,j-1))) / (2. * (1 + b_sqr))

# lets say I have boundary conditions now

def LaplaceEqStep(i, j, func):
    F = func
    return (F(i + 1, j) + F(i - 1, j) + F(i, j + 1) + F(i, j - 1)) / 4.

def LaplaceEqStep_Compass(i, j, F_E, F_W, F_N, F_S):
    return (F_E(i+1, j) + F_W(i-1, j) + F_N(i, j+1) + F_S(i, j-1)) / 4.


import numpy as np

# N-1 by j and M-2 by i, so the matrix is (M-1)*(N-1)

M = 5
N = 4

# A u = d


def BoundarySolution(i, j):
    if j == 3: return 8.9
    if j == 0: return [6.1, 6.8, 7.7, 8.7, 9.8][i]
    if i == 0: return [6.1, 7.2, 8.4, 8.9][j]
    if i == 4: return [9.8, 9.4, 9.2, 8.9][j]

    return None


def Func_d(i, j):
    r = BoundarySolution(i, j)
    if r is None: return 0
    return -r

def Init_d():
    d = np.zeros((M - 2, N - 2))
    for i in range(1, M-1):
        for j in range(1, N-1):
            d[i-1, j-1] = LaplaceEqStep(i, j, Func_d)

    return np.reshape(d, ((M-2)*(N-2), 1))

def Func_A(i_adj, j_adj):
    # initializing a row
    a = np.zeros((M - 2, N - 2))
    a[i_adj, j_adj] = -1.
    if i_adj > 0: a[i_adj-1, j_adj] = 1./4
    if i_adj < M-2-1: a[i_adj+1, j_adj] = 1./4
    if j_adj > 0: a[i_adj, j_adj-1] = 1./4
    if j_adj < N-2-1: a[i_adj, j_adj+1] = 1./4.

    return np.reshape(a, (1, (M-2)*(N-2)))

def Init_A():
    A = np.zeros(((M - 2)*(N - 2), (M - 2)*(N - 2)))
    for i_adj in range(0, M-2):
        for j_adj in range(0, N-2):
            A[i_adj*(N-2) + j_adj] = Func_A(i_adj, j_adj)

    return A

A = Init_A()
d = Init_d()

print(A)
print(d)

print(np.linalg.solve(A, d))


def JacobiIteration(tolerance):
    u_0 = np.zeros((M-2, N-2))

    def func(i, j):
        r = BoundarySolution(i, j)
        if r is None: return u_0[i-1, j-1]

        return r

    u_1 = u_0.copy()

    iterations = 0
    while True:
        iterations += 1

        it = np.nditer(u_1, flags=['multi_index'])
        while not it.finished:
            i, j = it.multi_index
            u_1[i, j] = LaplaceEqStep(i+1, j+1, func)

            it.iternext()

        if np.linalg.norm((u_1 - u_0).flatten(), np.inf) < tolerance:
            break
        u_1, u_0 = u_0, u_1

    u_1 = np.transpose(u_1)
    return np.reshape(u_1, ((M-2)*(N-2), 1)), iterations

print(JacobiIteration(1e-3))


def GaussSeidelIteration(tolerance):
    u_0 = np.zeros((M-2, N-2))

    def func_0(i, j):
        r = BoundarySolution(i, j)
        if r is None: return u_0[i-1, j-1]

        return r

    def func_1(i, j):
        r = BoundarySolution(i, j)
        if r is None: return u_1[i-1, j-1]

        return r


    u_1 = u_0.copy()

    iterations = 0
    while True:
        iterations += 1

        it = np.nditer(u_1, flags=['multi_index'])
        while not it.finished:
            i, j = it.multi_index
            u_1[i, j] = LaplaceEqStep_Compass(i+1, j+1, func_0, func_1, func_0, func_1)

            it.iternext()

        if np.linalg.norm((u_1 - u_0).flatten(), np.inf) < tolerance:
            break
        u_1, u_0 = u_0, u_1

    u_1 = np.transpose(u_1)
    return np.reshape(u_1, ((M-2)*(N-2), 1)), iterations

print(GaussSeidelIteration(1e-3))