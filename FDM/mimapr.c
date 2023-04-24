#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#define CIRCLE_CONSTRAIN 10
#define RIGTH_CONSTRAINT 350
#define TOP_CONSTRAINT 350
#define BOTTOM_CONSTRAINT 300

int M, N; //размерность пластины
long double **A; // массив коэффициентов
long double *b; // массив значений
int *num; // массив номеров узлов
long double c = 1; // удельная теплоемкость
long double ro = 1; // плотность 
long double lyambda = 1; // коэффициент теплопроводности
long double dx = 0.5;
long double dy = 0.5;

//заполнение матриц для точек не на границах
void make_matrix(int id, int k) {

	long double a = lyambda / c / ro;
	A[k][num[id + M]] = a / dy / dy;
	A[k][num[id - M]] = a / dy / dy;
	A[k][num[id + 1]] = a / dx / dx;
	A[k][num[id - 1]] = a / dx / dx;
	A[k][num[id]] = - (2 * a / dx / dx) - (2 * a / dy / dy);
}

//заполнение граничных условий
void mysolver(void) {

	int i, j; // столбцы, строки
	int x, y;
	int k = 0;
	int id;
	float l, m; // лямбда, мю
	int r = 3/dx - 1; // радиус
	long double a = lyambda / c / ro;
	//Перебираем всю матрицу
	for (j = 0; j < N; j++)
	{
		for (i = 0; i < M; i++)
		{
			// printf("%d %d \n" , i, j);
			id = j * M + i; //номер текущего элемента
			x = i - (5/dx);
			y = j - (3/dy);
			if (((x*x + y*y) >= r*r) && (i >= M-r) && (j >= N-r)) //за круглой границей
			{
				continue;
			}
			else if (((x*x + y*y) <= r*r) && (((x+1)*(x+1) + y*y) > r*r) && ((x*x + (y+1)*(y+1)) < r*r) && (i > M-r) && (j > N-r)) //около круглой границы // по х за границей
			{
				m = (sqrt(r*r - y*y) - x) / dx;
				A[k][num[id + M]] = a / dy / dy;
				A[k][num[id - M]] = a / dy / dy;
				A[k][num[id - 1]] = 2 * a / (m+1) / dx / dx; 
				A[k][num[id]] = - (2 * a / m / dx / dx) - (2 * a / dy / dy);
				b[k] = (-2) * a * CIRCLE_CONSTRAIN / m / (m+1) / dx / dx;
			}
			else if (((x*x + y*y) <= r*r) && (((x+1)*(x+1) + y*y) < r*r) && ((x*x + (y+1)*(y+1)) > r*r) && (i > M-r) && (j > N-r)) //около круглой границы // по у за границей
			{
				l = (sqrt(r*r - x*x) - y) / dy;
				A[k][num[id + 1]] = a / dx / dx;
				A[k][num[id - 1]] = a / dx / dx;
				A[k][num[id - M]] = 2 * a / (l+1) / dy / dy;
				A[k][num[id]] = - (2 * a / dx / dx) - (2 * a / m / dy / dy);
				b[k] = (-2) * a * CIRCLE_CONSTRAIN / l / (l+1) / dy / dy;
			}
			else if (((x*x + y*y) <= r*r) && (((x+1)*(x+1) + y*y) >= r*r) && ((x*x + (y+1)*(y+1)) >= r*r) && (i > M-r) && (j > N-r)) //около круглой границы // обе за границей
			{
				m = (sqrt(r*r - y*y) - x) / dx;
				l = (sqrt(r*r - x*x) - y) / dy;
				A[k][num[id - M]] = 2 * a / (l+1) / dy / dy;
				A[k][num[id - 1]] = 2 * a / (m+1) / dx / dx;
				A[k][num[id]] = - (2 * a / m / dx / dx) - (2 * a / l / dy / dy);
				b[k] = ((-2) * a * CIRCLE_CONSTRAIN / m / (m+1) / dx / dx) + ((-2) * a * CIRCLE_CONSTRAIN / l / (l+1) / dy / dy);
			}
			else if (j == 0) //нижняя граница
			{
				A[k][num[id]] = 1;
				b[k] = BOTTOM_CONSTRAINT;
			}
			else if (j == N - 1) //верхняя граница
			{
				A[k][num[id]] = 1;
				b[k] = TOP_CONSTRAINT;
			}
			else if (i == 0) //левая граница
			{
				A[k][num[id+1]] = 1;
				A[k][num[id]] = -1 - dx;
				b[k] = 0;
			}
			else if (i == M - 1) //правая граница
			{
				A[k][num[id]] = 1;
				b[k] = RIGTH_CONSTRAINT;
			}
			else
			{
				make_matrix(id, k);
			}
			
			k++;
		}
	}
}

void gauss(int n) { //решение систем с помощью метода Гаусса
	int i, j, k;
	long double a;
	//прямой ход метода Гаусса
	for (k = 0; k < n; k++)
		for (j = k + 1; j < n; j++)
		{
			a = - A[j][k] / A[k][k];
			b[j] += b[k] * a;
			for (i = k ; i < n; i++)
				A[j][i] += A[k][i] * a;
		}
	//Обратный ход метода Гаусса
	b[n - 1] /= A[n - 1][n - 1];
	for (i = n - 2; i >= 0; i--)
	{
		for (j = i + 1; j < n; j++)
			b[i] -= b[j] * A[i] [j];
		b[i] /= A[i][i];
	}
}

int main(int argc, char* argv[])
{

	int i, j, k, r, x, y;
	int n; // счетчик узлов
	M = 8/dx; //размерность матрицы
	N = 6/dy;
	num = (int*) malloc(sizeof(long double) * N * M); //  массив для хранения номеров узлов
	n = 0; // счетчик для заполнения узлов
	r = 3/dx-1; // радиус
	
	// заполнение матрицы номеров
	for (j = 0; j < N; j++) { // строки
		for (i = 0; i < M; i++) { // столбцы
		
	 		x = i - (5/dx); // расстояние по x
			y = j - (3/dy); // расстояние по y
			
			if (((x*x + y*y) >= r*r) && (i >= M-r) && (j >= N-r))
			{ // если за границей
				num[j * M + i] = -1;
				
			}
			else
			{
				num[j * M + i] = n;
				n++;
			}
			// printf("%d ",num[j * M + i]);
			}
		// printf("\n");
	}
	
	for (j = N-1; j >= 0; j--) {
		for (i = 0; i < M; i++)
			if(num[j * M + i] != (-1))
				printf("%d\t",num[j * M + i]);
		printf("\n");
		}
	printf("\n\n");
	
	A = (long double**) malloc(sizeof(long double*) * n); //создаем массивы для коэффициентов и искомых значений
	b = (long double*) malloc(sizeof(long double) * n);
	
	for (k = 0; k < n; k++)
	{
		A[k] = (long double*) malloc(sizeof(long double) * n); //массив коэффициентов двумерный
	}
	
	memset(b, 0, sizeof(long double) * n); // обнуление х
	
	for (i = 0; i < n; i++)
		memset(A[i], 0, sizeof(long double) * n); // обнуление А
		
	mysolver();
	gauss(n);
	
	for (j = N-1; j >= 0; j--)
	{
		for (i = 0; i < M; i++)
		{
			x = i - (5/dx);
			y = j - (3/dy);
			
			if (((x*x + y*y) >= r*r) && (i >= M-r) && (j >= N-r))
				continue;
				
			printf("%.0f\t",(double) b[num[j * M + i]]);
			// fprintf(fd, "%d\t%d\t%f\n", i, j, (double) b[num[j * M + i]]);
		}
		printf("\n");
		// fprintf(fd, "\n");
	}
	
	printf("\n\n");
	
	FILE *fd = fopen("out.txt", "w");
	
	for (j = 0; j < N; j++)
	{
		for (i = 0; i < M; i++)
		{
			x = i - (5/dx);
			y = j - (3/dy);
			
			if (((x*x + y*y) >= r*r) && (i >= M-r) && (j >= N-r))
				continue;
				
			// printf("%.0f\t",(double) b[num[j * M + i]]);
			fprintf(fd, "%d\t%d\t%f\n", i, j, (double) b[num[j * M + i]]);
		}
		// printf("\n");
		fprintf(fd, "\n");
	}
	fclose(fd);
	
	FILE *fg = fopen("gra.gnu", "w");
	fprintf(fg, "#!/usr/bin/gnuplot -persistent\n");
	fprintf(fg, "set size square\n");
	fprintf(fg, "set output 'plot.eps'\n");
	fprintf(fg, "set cbrange [0:350]\n");
	fprintf(fg, "set xrange[0:%d]\nset yrange[0:%d]\n", M - 1, N - 1);
	fprintf(fg, "set palette rgbformulae 22,13,-31\n");
	fprintf(fg, "set pm3d map\n");
	fprintf(fg, "set pm3d flush begin ftriangles scansforwar interpolate 5,5\n");
	fprintf(fg, "splot 'out.txt' using 1:2:3 with pm3d title 'var'\n");
	fprintf(fg, "pause -1");
	//fclose(fg);
	system("gnuplot gra.gnu");
	return 0;
}
