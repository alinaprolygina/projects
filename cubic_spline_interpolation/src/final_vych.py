import numpy as np
import matplotlib.pyplot as plt


def qubic_spline_coeff(x_nodes, y_nodes):  # функция нахождения коэффициентов

    N = len(x_nodes)

    K1 = [0]  # верхняя диагональ
    K_1 = []  # нижняя диагональ
    K0 = [1]  # главная диагональ

    for i in range(N-2):  # заполнение главной диагонали
        K = 2*(x_nodes[i+2] - x_nodes[i])
        K0.append(K)
    K0.append(1)

    for i in range(N-2):  # заполнение нижней диагонали
        K = x_nodes[i+1] - x_nodes[i]
        K_1.append(K)
    K_1.append(0)

    for i in range(N-2):  # заполнение верхней диагонали
        K = x_nodes[i+2] - x_nodes[i+1]
        K1.append(K)

    A = np.diag(K0, 0)
    A1 = np.diag(K1, 1)
    A_1 = np.diag(K_1, -1)
    A = A + A1 + A_1  # объединение всех диагоналей в одну
    B = [0]  # матрица В

    for i in range(N-2):  # заполнение матрицы В
        B_ = (3/(x_nodes[i+2]-x_nodes[i+1])*(y_nodes[i+2]-y_nodes[i+1])) - (3/(x_nodes[i+1]-x_nodes[i])*(y_nodes[i+1]-y_nodes[i]))
        B.append(B_)
    B.append(0)

    A_T = np.linalg.inv(A)  # инвертирование матрицы А

    res_c = np.dot(A_T, B)  # вычисление с
    res_b = np.zeros((N))
    res_d = np.zeros((N))

    for i in range(N-1):  # вычисление коэффициентов
        res_b[i] = 1/(x_nodes[i+1]-x_nodes[i])*(y_nodes[i+1]-y_nodes[i]) - (x_nodes[i+1]-x_nodes[i])/3*(res_c[i+1]+2*res_c[i])
        res_d[i] = (res_c[i+1]-res_c[i])/(3*(x_nodes[i+1]-x_nodes[i]))

    qs_coeff = [res_b, res_c, res_d]  # объединение коэффициентов в общую матрицу

    return qs_coeff


def qubic_spline(x, qs_coeff, x_nodes, y_nodes):  # функция сплайна

    i = approx(x, x_nodes)
    S = y_nodes[i] + qs_coeff[0][i]*(x-x_nodes[i]) + qs_coeff[1][i]*(x-x_nodes[i])**2 + qs_coeff[2][i]*(x - x_nodes[i])**3

    return S


def approx(x, x_nodes):  # функция приближения точек к узлам
    i = 0 
    N = len(x_nodes)

    while((x > x_nodes[i]) and i < 10):

        i = i + 1

    if(x <= x_nodes[0]):
        i = 1

    if(x >= x_nodes[N-1]):
        i = N-1
    return i - 1


def d_qubic_spline(x, qs_coeff, x_nodes):  # функция вычисления производной сплайна

    i = approx(x, x_nodes)
    S_ = qs_coeff[0][i] + 2*qs_coeff[1][i]*(x-x_nodes[i]) + 3*qs_coeff[2][i]*(x-x_nodes[i])**2

    return S_


def l_i(i, x, x_nodes):  # вычисление базисного полинома Лагранжа
    li = 1
    for j in range(N): 
        if(i != j): 
            li = li * ((x-x_nodes[j])/(x_nodes[i]-x_nodes[j])) 
    return li


def L(x, x_nodes, y_nodes):  # вычисление интерполяционного полинома Лагранжа
    Lx = 0
    for i in range(N): 
        Lx = Lx + y_nodes[i]*(l_i(i, x, x_nodes))
    return Lx


x_nodes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # узлы x
y_nodes = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]  # узлы у

N = len(x_nodes)

m_coeff = qubic_spline_coeff(x_nodes, y_nodes)  # матрица коэффициентов

app = []  # массив 101 значения х
Sx = []  # массив значений сплайна
dS = []  # массив значений производной сплайна

j = 0

for i in range(101):  # заполнение массива app 101 значением
    app.append(j) 
    j = j + 0.01

for i in range(101):  # вычисление значений сплайнов для 101 значения
    S = qubic_spline(app[i], m_coeff, x_nodes, y_nodes) 
    S_ = d_qubic_spline(app[i], m_coeff, x_nodes) 
    Sx.append(S) 
    dS.append(S_)

Z = []  # массив погрешностей
Xt = []  # массив иксов с погрешностью
Yt = []  # массив игриков с погрешностью
Lagg = []  # вычисленные интерполянты Лагрнажа

for i in range(1000):  # заполнение массива погрешностей
    ZZ = [] 
    for j in range(N): 
        ZZ.append(np.random.normal(0, 0.01))
    Z.append(ZZ)

for i in range(1000):  # заполнение массива иксов с погрешностью
    Xtt = []
    for j in range(N):
        Xt_ = x_nodes[j] + Z[i][j] 
        Xtt.append(Xt_)
    Xt.append(Xtt)

for i in range(1000):  # заполнение массива игриков с погрешностью
    Ytt = []
    for j in range(N):
        Yt_ = y_nodes[j] + Z[i][j] 
        Ytt.append(Yt_)
    Yt.append(Ytt)

for i in range(1000):  # заполнение массива интерполянтов Лагранжа
    Laggg = []
    for j in range(101):
        Lagg_ = L(app[j], x_nodes, Yt[i]) 
        Laggg.append(Lagg_)
    Lagg.append(Laggg)
    
Sp = []  # массив сплайнов для интерполяции кубическим сплайном
    
for i in range(1000):  # заполнение массива сплайнами для интерполяции
    Spp = []
    for j in range(101):
        mx_coeff = qubic_spline_coeff(x_nodes, Yt[i])
        Sp_ = qubic_spline(app[j], mx_coeff, x_nodes, Yt[i])
        Spp.append(Sp_)
    Sp.append(Spp)

# Lagg = np.sort(Lagg, 0)  # сортировка интерполянтов Лагранжа по возрастанию
Sp = np.sort(Sp, 0)  # сортировка сплайнов

hl = Sp[49]  # нижняя граница доверительного интервала
hu = Sp[949]  # верхняя граница доверительного интервала
hm = Sp[499]  # средний сплайн

# hl = Lagg[49]
# hu = Lagg[949]
# hm = Lagg[499]

plt.figure()
# plt.scatter(x_nodes, y_nodes)  # вывод узлов
plt.grid() 
plt.plot(app, Sx)  # вывод кубического сплайна
plt.plot(app, dS)  # вывод производной сплайна
# plt.plot(app, hl)  # вывод нижней границы доверительного интервала
# plt.plot(app, hu)  # вывод верхней границы доверительного интервала
# plt.plot(app, hm)  # вывод усредненного значения
plt.xticks(np.arange(0, 1.1, 0.1))
# for i in range(1000):  # построение семейства графиков кубических сплайнов
#    plt.plot(app, Sp[i])
# for i in range(1000):  # построение семейства графиков интерполяции Лагранжа
#    plt.plot(app, Lagg[i])
plt.show()
# plt.savefig('qubic_spline_y.png')  # сохранение файлов
