import numpy as np
import matplotlib.pyplot as plt

N_ex = 800
N_br = 200
h = 0.5
t_n = 1000

a = np.hstack((0.02 * np.ones(N_ex), 0.02 + 0.08 * np.random.uniform(0, 1) * np.ones(N_br)))
b = np.hstack((0.2 * np.ones(N_ex), 0.25 - 0.05 * np.random.uniform(0, 1) * np.ones(N_br)))
c = np.hstack((-65. + 15 * np.random.uniform(0, 1, N_ex) ** 2 * np.ones(N_ex), -65 * np.ones(N_br)))
d = np.hstack((8 - 6 * np.random.uniform(0, 1, N_ex) ** 2 * np.ones(N_ex), 2 * np.ones(N_br)))

W = np.hstack((0.5 * np.random.uniform(0, 1, (N_ex + N_br, N_ex)), -np.random.uniform(0, 1, (N_ex + N_br, N_br))))

ksi = np.random.uniform(0, 1, N_ex)
dzeta = np.random.uniform(0, 1, N_br)


def network_euler(N_ex, N_br, h,  t_n):

    v = -65. * np.ones(N_ex + N_br)
    u = b * v

    network_pulses = []
    for t in np.arange(t_n, step=h):
        pulse = v >= 30
        v[pulse] = c[pulse]
        u[pulse] = u[pulse] + d[pulse]
        pulse_index = np.where(pulse)
        if len(pulse_index[0]) != 0:
            network_pulses.append([t, pulse_index[0]])
        I = np.hstack((5 * ksi, 2 * dzeta))
        I += np.sum(W[:, pulse], axis=1)
        v = v + h * (0.04 * v ** 2. + 5. * v + 140. - u + I)
        u = u + h * (a * (b * v - u))

    return network_pulses


T = network_euler(N_ex, N_br, h, t_n)
fig, ax = plt.subplots(1, 1)
print(len(T))
for i in T:
    for j in i[1]:
        if(j < N_ex):
            color = 'magenta'
        else:
            color = 'blue'
        plt.plot([i[0]], [j], '.', color=color)

plt.xticks(np.arange(0, 1100, 100), color='black')
plt.yticks(np.arange(0, 1100, 100), color='black')
ax.set_xlabel(r'$time$', color='black')
ax.set_ylabel(r'$neuron\_id$', color='black')
plt.grid(color='black')
plt.show()
