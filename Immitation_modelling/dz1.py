import numpy as np
import csv
from random import randrange
import matplotlib.pyplot as plt

P = np.array([[0.2, 0.24, 0.19, 0.2, 0.17],
              [0.13, 0.22, 0.2, 0.2, 0.25],
              [0.16, 0.22, 0.2, 0.2, 0.22],
              [0.22, 0.2, 0.17, 0.2, 0.21],
              [0.19, 0.25, 0.22, 0.16, 0.18]])

n = 100
states = [i+1 for i in range(5)]

def print_matr(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j] = round(m[i][j], 3)
        print(m[i])

def mark_iter(n, m, states):
    current_s = randrange(1,6)
    states_tr = [current_s]
    n_entry=[0 for _ in range(len(states))]
    for _ in range(n-1):
        per_ver = m[current_s-1]
        n_entry[current_s-1]+=1
        next_s = np.random.choice(states, p=per_ver)
        current_s=next_s
        states_tr.append(current_s)
    return n_entry, states_tr

def marginal_probabilities(P):
    A = P.T - np.eye(len(states), dtype=float)
    A[-1] = np.full(len(states), 1)
    b = np.zeros(len(states))
    b[-1] = 1.
    p = np.linalg.solve(A, b)
    return p, [list(p) for _ in range(len(states))], list(p).count(0)!=len(p)

p, pred_mat_per, erg = marginal_probabilities(P)
print("Выполнение критерия эргогодичности:")
print(erg)
print("Предельные вероятности:")
print(p)
print("Предельная матрица переходов:")
print_matr(pred_mat_per)

x=[i+1 for i in range(n)]
n_entry_exp=[[0 for _ in range(20)] for _ in range(len(states))]

plt.grid()
plt.ylabel("Состояния")
plt.xlabel("Переходы")
plt.yticks(np.arange(0, len(states)+1, step=1))
print("Относительные частоты:")
for i in range(20):
    myDictionary, tr = mark_iter(n, P, states)

    for j in range(len(states)):
        n_entry_exp[j][i] = myDictionary[j]/n

    print(i+1
          , "& ",myDictionary[0]/n
          , "& ",myDictionary[1]/n
          , "& ",myDictionary[2]/n
          ,"& ",myDictionary[3]/n
          ,"& ",myDictionary[4]/n, "\\\\")
    
    plt.plot(x, tr, 'o--',linewidth = 0.7, markeredgewidth = 0.1)
print("Среднеквадратичные отклонения:")
for i in range(len(states)):
    print('%.3f'%np.sqrt(20*np.var(n_entry_exp[i])/(20-1)), "& ")
plt.show()
