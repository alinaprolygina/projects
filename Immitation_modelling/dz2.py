import os
import csv
import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

# Исходные данные
with open('Task2.csv') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    print(', '.join(row))

# Чтение из исходного файла
df = pd.read_csv('Task2.csv', header=None)
matrix = df.to_numpy()
matrix

# Расчёт предельных вероятностей для состояний, отмеченных синим в таблице (1, 5, 11, 14)
matrix_blue = np.array([[0.12, 0.24, 0.52, 0.12],
                       [0.12, 0.12, 0.64, 0.12],
                       [0.23, 0.26, 0.27, 0.24],
                       [0., 0.36, 0.64, 0.]])
a_blue = matrix_blue.transpose() - np.eye(4)
a_blue[3, :] = 1.
b = np.zeros(4)
b[3] = 1.

pi_0_blue = np.linalg.solve(a_blue, b)
pi_0_blue

# Расчёт предельных вероятностей для состояний, отмеченных зелёным в таблице (4, 7, 10, 15)
matrix_green = np.array([[0.18, 0.31, 0.27, 0.24],
                       [0.76, 0., 0.24, 0.],
                       [0.76, 0., 0.12, 0.12],
                       [0.4, 0.24, 0., 0.36]])
a_green = matrix_green.transpose() - np.eye(4)
a_green[3, :] = 1.
b = np.zeros(4)
b[3] = 1.
pi_0_green = np.linalg.solve(a_green, b)
pi_0_green

# Расчёт предельных вероятностей для состояний, отмеченных жёлтым в таблице (6, 12, 13)
matrix_yellow = np.array([[0.24, 0.64, 0.12],
                       [0.37, 0.37, 0.26],
                       [0.12, 0.64, 0.34]])
a_yellow = matrix_yellow.transpose() - np.eye(3)
a_yellow[2, :] = 1.
b = np.zeros(3)
b[2] = 1.
pi_0_yellow = np.linalg.solve(a_yellow, b)
pi_0_yellow

# Получение матрицы вероятностей переходов для состояний, отмеченных серым в таблице (2, 3, 8, 9)
matrix_gray = np.array([[0.12, 0.56, 0.09, 0.23, 0., 0., 0.],
                        [0.11, 0.13, 0.09, 0.08, 0.59, 0., 0.],
                        [0.18, 0.2, 0.16, 0.22, 0., 0., 0.24],
                        [0.12, 0.11, 0.19, 0.15, 0., 0.43, 0.],
                        [0., 0., 0., 0., 1., 0., 0.],
                        [0., 0., 0., 0., 0., 1., 0.],
                        [0., 0., 0., 0., 0., 0., 1.]])
matrix_gray

# Возведение матрицы вероятностей переходов для серых состояний в 100 степень для получения предельной матрицы переходов
matrix_gray_100 = matrix_gray
for i in range(100):
  matrix_gray_100 = matrix_gray_100.dot(matrix_gray_100)
matrix_gray_100

# Получение предельных вероятностей для серых состояний при старте из определённого серого состояния
matrix_gray_100_p = matrix_gray_100[0:4, 4:7]
matrix_gray_100_p

# Получение предельных вероятностей для серых состояний при равновероятном старте из любого серого состояния
pi_0_gray_equal = np.array([0.25, 0.25, 0.25, 0.25]) @ matrix_gray_100_p
pi_0_gray_equal

# Установка параметров для проведения множества экспериментов
rd.seed(0)
experiment_count = 10
step_count = 100

# Получение и запись результатов экспериментов
results = []
for t in range(15):
  for tt in range(experiment_count):
    result_current = []
    # Определение стартового состояния
    i = t

    for ttt in range(step_count):
      # Случайный выбор перехода
      rnd_value = rd.random()
      j = 0
      while rnd_value > 0.:
        if (j == 15):
          j = rd.choice([2, 3, 8, 9])
          break
        rnd_value -= matrix[i][j]
        j += 1
      # Запись совершённого перехода
      result_current.append(j)
      i = j-1
    # Запись шагов в рамках одного эксперимента
    results.append(result_current)

# Переопределение номеров состояний для близкого расположения на графике состояний из одного класса
results_sorted = [1, 12, 13, 5, 2, 9, 6, 14, 15, 7, 3, 10, 11, 4, 8]

for i in range(15):
  for j in range(experiment_count):
    for k in range(step_count):
      results[i*experiment_count + j][k] = results_sorted[results[i*experiment_count + j][k] - 1]

# Вывод на графике результатов обработки заданного числа экспериментов для каждого из стартовых состояний, помеченных синим (1, 5, 11, 14)
plot_count = 1
for i in [0, 4, 10, 13]:
  for j in range(plot_count):
    plt.plot(results[i*experiment_count + j])
# Для расположения графика на всём промежутке [1; 15] по оси OY
plt.plot(0, 15)
plt.plot(0, 1)
plt.show()

# Вывод на графике результатов обработки заданного числа экспериментов для каждого из стартовых состояний, помеченных зелёным (4, 7, 10, 15)
plot_count = 1
for i in [3, 6, 9, 14]:
  for j in range(plot_count):
    plt.plot(results[i*experiment_count + j])
# Для расположения графика на всём промежутке [1; 15] по оси OY
plt.plot(0, 15)
plt.plot(0, 1)
plt.show()

# Вывод на графике результатов обработки заданного числа экспериментов для каждого из стартовых состояний, помеченных жёлтым (6, 12, 13)
plot_count = 1
for i in [5, 11, 12]:
  for j in range(plot_count):
    plt.plot(results[i*experiment_count + j])
# Для расположения графика на всём промежутке [1; 15] по оси OY
plt.plot(0, 15)
plt.plot(0, 1)
plt.show()

# Вывод на графике результатов обработки заданного числа экспериментов для каждого из стартовых состояний, помеченных серым (2, 3, 8, 9)
plot_count = 2
for i in [1, 2, 7, 8]:
  for j in range(plot_count):
    plt.plot(results[i*experiment_count + j])
# Для расположения графика на всём промежутке [1; 15] по оси OY
plt.plot(0, 15)
plt.plot(0, 1)
plt.show()
