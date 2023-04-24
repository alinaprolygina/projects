#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from statistics import mean

I = 5

pulse_eu = []
pulse_imp = []
pulse_ru = []

r = {
    'TS' : [0.02, 0.2, -65, 6],
    'PS' : [0.02, 0.25, -65, 6],
    'C' : [0.02, 0.2, -50, 2],
    'FS' : [0.1, 0.2, -65, 2],
     }


def f1(u, v):
    return 0.04*(v**2) + 5*v + 140 - u + I


def f2(u, v):
    return a*(b*v - u)
    
    
def euler(x_0, t_n, f, h):
    m = int(t_n / h)
    v = np.zeros((m + 1,))
    u = np.zeros((m + 1,))
    t = np.linspace(0, t_n, m + 1)
    vpulse=[]
    v[0], u[0] = x_0
    for i in range(m):
        v[i + 1] = v[i] + h * f[0](u[i], v[i])
        u[i + 1] = u[i] + h * f[1](u[i], v[i])
        if(v[i+1] >= 30):
            vpulse.append(v[i])
            v[i+1] = c
            u[i+1] = u[i+1] + d
            pulse_eu.append(h*(i+1))

    return t, v, pulse_eu, vpulse


def implicit_euler(x_0, t_n, f, h):
    m = int(t_n / h)
    v = np.zeros((m + 1,))
    u = np.zeros((m + 1,))
    t = np.linspace(0, t_n, m + 1)
    v[0], u[0] = x_0
    vpulse=[]
    def imp_f1(vi_1, ui, vi):
        return vi_1 - vi - h*f[0](ui, vi_1)

    def imp_f2(ui_1, ui, vi):
        return ui_1 - ui - h*f[1](ui_1, vi)
    
    for i in range(m):

        v[i+1] = (optimize.root(imp_f1, v[i], args = (u[i], v[i]))).x
        u[i+1] = (optimize.root(imp_f2, u[i], args = (u[i], v[i]))).x
        if(v[i+1] >= 30):
            vpulse.append(v[i])
            v[i+1] = c
            u[i+1] = u[i+1] + d
            pulse_imp.append(h*(i+1))

    return t, v, pulse_imp, vpulse


def runge_kutta(x_0, t_n, f, h):
    m = int(t_n / h)
    v = np.zeros((m + 1,))
    u = np.zeros((m + 1,))
    t = np.linspace(0, t_n, m + 1)
    vpulse=[]
    v[0], u[0] = x_0
    for i in range(m):
        k1_v = h*f[0](u[i], v[i])
        k1_u = h*f[1](u[i], v[i])
        k2_v = h*f[0](u[i] + k1_u/2, v[i] + k1_v/2)
        k2_u = h*f[1](u[i] + k1_u/2, v[i] + k1_v/2)
        k3_v = h*f[0](u[i] + k2_u/2, v[i] + k2_v/2)
        k3_u = h*f[1](u[i] + k2_u/2, v[i] + k2_v/2)
        k4_v = h*f[0](u[i] + k3_u, v[i] + k3_v)
        k4_u = h*f[1](u[i] + k3_u, v[i] + k3_v)
        v[i + 1] = v[i] + (1/6)*(k1_v + 2*k2_v + 2*k3_v + k4_v)
        u[i + 1] = u[i] + (1/6)*(k1_u + 2*k2_u + 2*k3_u + k4_u)
        if(v[i+1] >= 30):
            vpulse.append(v[i])
            v[i+1] = c
            u[i+1] = u[i+1] + d
            pulse_ru.append(h*(i+1))

    return t, v, pulse_ru, vpulse


f = [f1, f2]
t_n = 300
h = 0.1

fig, ax = plt.subplots(4, 1, figsize=(14, 20))
names = ['Tonic spiking', 'Phasic spiking', 'Chattering', 'Fast spiking']
for i, j, ax_ in zip(['TS', 'PS', 'C', 'FS'], names, ax):
    a = r[i][0]
    b = r[i][1]
    c = r[i][2]
    d = r[i][3]
    x_0 = [c, b*c]
    t_eu, v_eu, pulse_eu1, vpulse = euler(x_0, t_n, f, h)
    print(pulse_eu1)
    # print(c - mean(vpulse))
    # vpulse.clear()
    pulse_eu1.clear()
    t_ru, v_ru, pulse_ru1, vpulse = runge_kutta(x_0, t_n, f, h)
    print(pulse_ru1)
    # print(c - mean(vpulse))
    # vpulse.clear()
    pulse_ru1.clear()
    t_imp, v_imp, pulse_imp1, vpulse = implicit_euler(x_0, t_n, f, h)
    print(pulse_imp1)
    # print(c - mean(vpulse))
    # vpulse.clear()
    pulse_imp1.clear()
    ax_.set_title(j, loc='left')
    ax_.plot(t_eu, v_eu, '.--', linewidth=1, color='black', label=r'$w_i$(euler)')
    ax_.plot(t_ru, v_ru, '.--', linewidth=1, color='magenta', label=r'$w_i$(runge-kutta)')
    ax_.plot(t_imp, v_imp, '.--', linewidth=2, color='blue', label=r'$w_i$(implicit euler)')
    ax_.set_xlabel(r'$t$', fontsize=10)
    ax_.set_ylabel(r'$v$', fontsize=10)
    ax_.grid()
    ax_.legend(loc='upper center', fontsize=8)
plt.show()
