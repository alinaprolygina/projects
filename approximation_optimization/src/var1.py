import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.optimize import *


C = 1.03439984
T = 1.75418438
g = 9.8


def xt(t, x):
    return C*t - C * 0.5 * sin(2*t) - x


def tx(x):
    return fsolve(xt, 0, x)


def func(t):
    if t == 0:
        return 0

    flux = np.sin(2 * t) / (1 - np.cos(2 * t))
    y = np.sqrt(C / g) * np.sqrt(1 + flux ** 2) * np.sqrt(1 - np.cos(2 * t))
    return y


def composite_simpson(a, b, n, f):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum_odd_ = []
    for x_ in x[2:-1:2]:
        tso = tx(x_)
        sum_odd_.append(f(tso))
    sum_odd = np.sum(sum_odd_)
    sum_even_ = []
    for x_ in x[1::2]:
        tse = tx(x_)
        sum_even_.append(f(tse))
    sum_even = np.sum(sum_even_)
    return h / 3. * (f(tx(x[0])) + 2 * sum_odd + 4 * sum_even + f(tx(x[-1])))


def error_cs(a, b, n, f):
    exact_integral = np.sqrt(2 * C / g) * T
    return np.abs(composite_simpson(a, b, n, f) - exact_integral)


def error_ctr(a, b, n, f):
    exact_integral = np.sqrt(2 * C / g) * T
    return np.abs(composite_trapezoid(a, b, n, f) - exact_integral)


def composite_trapezoid(a, b, n, f):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum_ = []
    for x_ in x[1:-1:1]:
        ts = tx(x_)
        sum_.append(f(ts))
    tr_sum = 2 * np.sum(sum_)
    return h / 2 * (f(tx(x[0])) + tr_sum + f(tx(x[-1])))


a = 0
b = 2
h_for_scaling = np.logspace(-2, 0, 50)

fig1, ax = plt.subplots()
n = [i for i in range(3, 9999)]
ax.loglog([(b - a) / n_ for n_ in n], [error_cs(a, b, n_, func) for n_ in n], 'o', markersize=1, label=r'simpson')
ax.loglog([(b - a) / n_ for n_ in n], [error_ctr(a, b, n_, func) for n_ in n], 'o', markersize=1, label=r'trapezoid')
# ax.loglog(h_for_scaling, h_for_scaling, 'k-', label=r'$O(h)$')
# ax.loglog(h_for_scaling, 10 ** (-2) * h_for_scaling ** 2, 'k-.', label=r'$O(h^2)$')
# ax.loglog(h_for_scaling, 10 ** (-3) * h_for_scaling ** 4, 'k--', label=r'$O(h^4)$')
ax.grid()
ax.set_xlabel('h')
ax.set_ylabel('E')
ax.legend()
plt.show()
