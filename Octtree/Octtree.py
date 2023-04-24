import numpy as np
from math import fabs
import os 
import os.path

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Цикл для сравнения двух массивов вершин куба и точек stl файла
def Optimize(vertex,cub,x):
	a = 0
	b = 0
	for i in range(x):
		a1 = 0
		for k in range(3):
			if vertex[i][k] <= cub[0][k]: 
				a1 = a1 + 1
			if vertex[i][k] >= cub[4][k]:
				a1 = a1 + 1
			if a1 == 6:
				a = a + 3

	for i in range(x):
		for j in range(8):
			ki = 0
			a1 = 0
			for k in range(3):
				if vertex[i][k] <= cub[0][k]: 
					a1 = a1 + 1
				if vertex[i][k] >= cub[4][k]:
					a1 = a1 + 1
				if a1 == 6:
					for m in range(3):
						if fabs(vertex[i][m] - cub[j][m]) <= dm * kf:
							ki = ki + 1
			if ki == 3:
				b = b + 3
				break

	if a == b:
		for i in range(x):
			for j in range(8):
				ki = 0
				a1 = 0
				for k in range(3):
					if vertex[i][k] <= cub[0][k]: 
						a1 = a1 + 1
					if vertex[i][k] >= cub[4][k]:
						a1 = a1 + 1
					if a1 == 6:
						for m in range(3):
							if fabs(vertex[i][m] - cub[j][m]) <= dm * kf:
								ki = ki + 1
				if ki == 3:
					vertex[i] = cub[j]
					break
					
				
	mas = [a, b]
	return(mas, vertex)

# Функция рекурсивного деления
def Octtree(vertex,cub,n,x):
	n = n + 1
	print(n)
	cub0 = [cub[0],							
	  	[cub[0][0],cub[0][1],cub[0][2] - dm/(2**n)],	
	  	[cub[0][0] - dm/(2**n),cub[0][1],cub[0][2] - dm/(2**n)],
	  	[cub[0][0] - dm/(2**n),cub[0][1],cub[0][2]],	
	  	[cub[0][0] - dm/(2**n),cub[0][1] - dm/(2**n),cub[0][2] - dm/(2**n)],
	  	[cub[0][0],cub[0][1] - dm/(2**n),cub[0][2] - dm/(2**n)],
	  	[cub[0][0],cub[0][1] - dm/(2**n),cub[0][2]],	
	  	[cub[0][0] - dm/(2**n),cub[0][1] - dm/(2**n),cub[0][2]]]
	mas1 = Optimize(vertex, cub0, x)
	vertex = mas1[1]
	if mas1[0][0] != mas1[0][1]:
		vertex = Octtree(vertex,cub0,n,x)

	for i in range(1, 8):
		cubi = [cub0[i],
	  		[cub0[i][0],cub0[i][1],cub0[i][2] - dm/(2**n)],	
	  		[cub0[i][0] - dm/(2**n),cub0[i][1],cub0[i][2] - dm/(2**n)],
	  		[cub0[i][0] - dm/(2**n),cub0[i][1],cub0[i][2]],	
	  		[cub0[i][0] - dm/(2**n),cub0[i][1] - dm/(2**n),cub0[i][2] - dm/(2**n)],
	  		[cub0[i][0],cub0[i][1] - dm/(2**n),cub0[i][2] - dm/(2**n)],
	  		[cub0[i][0],cub0[i][1] - dm/(2**n),cub0[i][2]],	
	  		[cub0[i][0] - dm/(2**n),cub0[i][1] - dm/(2**n),cub0[i][2]]]
		mas2 = Optimize(vertex, cubi, x)
		vertex = mas2[1]
		if mas2[0][0] != mas2[0][1]:
			vertex = Octtree(vertex,cubi,n,x)
	return vertex

# Ввод названий файлов
print("Введите название исходного stl файла: ")
file1 = input() + ".stl"
fi = os.path.exists(file1)

while fi != True:
	print("Такого файла нет")
	print("Ладно, дам вам еще попытку Юрий Валерьевич: ")
	file1 = input() + ".stl"
	fi = os.path.exists(file1)

print("Придумайте название выходному stl файлу: ")
file2 = input() + ".stl"
rr = 0
while rr == 0: 
	while file1 == file2:
		print("Нельзя повторяться ")
		print("Попробуйте еще раз: ")
		file2 = input() + ".stl"
	if not set("/:*?\"\\<>|").isdisjoint(file2) == True:
		print("Не используйте спец. символы для названия файла ")
		print("Попробуйте еще раз: ")
		file2 = input() + ".stl"
	else:
		rr = 1


print("Коэффициент: ")
kf = input()
rr = 0
while rr == 0: 
	while is_number(kf) == False:
		print("Число должно быть число ")
		print("Попробуйте еще раз: ")
		kf = input()
	kf = float(kf)
	if kf < 0 or kf > 1:
		print("Число должно быть от 0 до 1 ")
		print("Попробуйте еще раз: ")
		kf = input()
	else:
		rr = 1

facet = [] # Массив нормалей треугольников
vertex = [] # Двумерный массив координат вершин треугольников

# Открываем наш stl файл и записываем координаты в 2 массива
for l in open(file1, "r") :
    l = l.split()
    if l[0] == "facet" : facet.append(list(map( float, l[-3:] )))
    elif l[0] == "vertex" : vertex.append(list(map( float, l[-3:] )))


# Найдем максимальную и минимальную точки
mx = max((max(_) for _ in vertex))
mi = min((min(_) for _ in vertex))

# Находим колличество треугольников
x = len(vertex)

# Создаем массивы минимумов и максимумов по координатам
min_ = [mx, mx, mx]
max_ = [mi, mi, mi]

# Находим минимумы и максимумы по координатам
for i in range(x):
	for j in range(3):
		if vertex[i][j] > max_[j]:
			max_[j] = vertex[i][j]

for i in range(x):
	for j in range(3):
		if vertex[i][j] < min_[j]:
			min_[j] = vertex[i][j]

# Находим габаритные размеры фигуры
d = np.array(max_) - np.array(min_)

# Находим большую сторону, она же будет стороной куба
dm = max(d)

# Найдем точки вершин куба
cub = [max_,							
	  [max_[0],max_[1],max_[2] - dm],	
	  [max_[0] - dm,max_[1],max_[2] - dm],
	  [max_[0] - dm,max_[1],max_[2]],	
	  [max_[0] - dm,max_[1] - dm,max_[2] - dm],
	  [max_[0],max_[1] - dm,max_[2] - dm],
	  [max_[0],max_[1] - dm,max_[2]],	
	  [max_[0] - dm,max_[1] - dm,max_[2]]]

masd = Optimize(vertex,cub,x)
vertex = masd[1]
if masd[0][0] != masd[0][1]:
	vertex = Octtree(vertex,cub,0,x)

# Создаем stl файл и записываем результат работы программы 
l = open(file2, "w")
l.write ("solid " + file2 + "\n")
m = 0

for n  in range(int(len(vertex) / 3)):
    l.write ("facet normal {} {} {}\n".format(facet[n][0],facet[n][1],facet[n][2]))
    l.write ("outer loop\n")
    l.write ("vertex {} {} {}\n".format(vertex[m][0],vertex[m][1],vertex[m][2]))
    l.write ("vertex {} {} {}\n".format(vertex[m + 1][0],vertex[m + 1][1],vertex[m + 1][2]))
    l.write ("vertex {} {} {}\n".format(vertex[m + 2][0],vertex[m + 2][1],vertex[m + 2][2]))
    l.write ("endloop\n")
    l.write ("endfacet\n")
    m = m + 3

l.write ("endsolid " + file2 + "\n")
l.close()

os.startfile(file1)
os.startfile(file2) 