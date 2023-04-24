#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <cmath>
#include <string>

using namespace std;

//Параметры элементов схемы
const double R1 = 10000.0;
const double R2 = 1000.0;
const double C = 1e-6;
const double L = 1e-3;

const double Cb = 2e-12;
const double Ru = 1e+6;
const double Rb = 20;
const double MFt = 0.026;
const double It = 1e-12;
const double Re = 1;
const double T = 1e-4;

double I(double t) {
    return 10 * sin(2 * M_PI * t / T);
}

double Id(double p2, double p1) {
    double result = It * (exp((p2 - p1) / MFt) - 1);
    return result;
};

double dId(double p2, double p1) {
    double result = It * exp((p2 - p1) / MFt) / MFt;
    return result;
};

//Класс матриц
class Matrix {
private:
    vector<vector<double>> m = { {0.} };
    int nrow = 1;
    int ncol = 1;
    struct Max {
        double value;
        int row;
        int col;
    };
public:
    Matrix() = default;
    Matrix(int row, int col, double d = 0) :nrow{ row }, ncol{ col } {
        m.resize(row);
        for (int i = 0; i < row; i++) {
            m[i].resize(col);
            for (int j = 0; j < col; j++) {
                m[i][j] = d;
            }
        }
    }
    Matrix(vector<vector<double>> a) : m{ a }, nrow{ int(a.size()) }, ncol{ int(a[0].size()) } {}
    Matrix(const Matrix& a) : m{ a.m }, nrow{ a.nrow }, ncol{ a.ncol } {}
    ~Matrix() = default;
    vector<double>& operator[](int i) {
        return m[i];
    }

    vector<double> operator[](int i) const {
        return m[i];
    }

    friend ostream& operator<<(ostream& out, const Matrix& a) {
        out << fixed;
        for (int i = 0; i < a.nrow; i++) {
            for (int j = 0; j < a.ncol; j++)
                out << '\t' << a.m[i][j];
            out << '\n';
        }
        return out << defaultfloat;
    }

    Matrix operator-() const {
        Matrix result(nrow, ncol);
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                result[i][j] = -m[i][j];
            }
        }
        return result;
    }

    Matrix operator+(const Matrix& a) const {
        Matrix result(nrow, ncol);
        if (a.nrow != nrow || a.ncol != ncol) {
            cerr << "Error in operator +: matrices must be the same size!";
            exit(4);
        }
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                result[i][j] = m[i][j] + a[i][j];
            }
        }
        return result;
    }

    Matrix operator-(const Matrix& a) const {
        Matrix result(nrow, ncol);
        if (a.nrow != nrow || a.ncol != ncol) {
            cerr << "Error in operator -: matrices must be the same size!";
            exit(4);
        }
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                result[i][j] = m[i][j] - a[i][j];
            }
        }
        return result;
    }

    Matrix operator*(const Matrix& a) const {
        Matrix result(nrow, a.ncol);
        if (a.nrow != ncol || a.ncol != nrow) {
            cerr << "Error in operator *: matrices must be suitable for multiplication!";
            exit(4);
        }
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < a.ncol; j++) {
                for (int k = 0; k < ncol; k++) {
                    result[i][j] += m[i][k] * a[k][j];
                }
            }
        }
        return result;
    }

    Matrix operator*(double k) const {
        Matrix result(nrow, ncol);
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                result[i][j] = k * m[i][j];
            }
        }
        return result;
    }

    friend Matrix operator*(double k, const Matrix& a) {
        Matrix result(a.nrow, a.ncol);
        for (int i = 0; i < a.nrow; i++) {
            for (int j = 0; j < a.ncol; j++) {
                result[i][j] = k * a[i][j];
            }
        }
        return result;
    }

    Matrix operator/(double k) {
        Matrix result(nrow, ncol);
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                result[i][j] = m[i][j] / k;
            }
        }
        return result;
    }

    int row() const {
        return nrow;
    }

    int col() const {
        return ncol;
    }

    Max abs_max() const {
        double value = m[0][0];
        int row = 0;
        int col = 0;
        for (int i = 0; i < nrow; i++) {
            for (int j = 0; j < ncol; j++) {
                if (abs(m[i][j]) > value) {
                    value = abs(m[i][j]);
                    row = i;
                    col = j;
                }
            }
        }
        return { value,row,col };
    }

    Matrix transpose() const {
        Matrix result(ncol, nrow);
        for (int i = 0; i < ncol; i++)
            for (int j = 0; j < nrow; j++)
                result.m[i][j] = m[j][i];
        return result;
    }

    Matrix submatrix(int row_begin, int col_begin, int row_end, int col_end) const {
        if (row_begin < 0 || row_begin >row_end || row_end > nrow - 1 || col_begin<0 || col_begin>col_end || col_end > ncol - 1) {
            cerr << "Error in function submatrix: wrong submatrix size!\n";
            exit(5);
        }
        Matrix result(row_end - row_begin + 1, col_end - col_begin + 1);
        for (int i = 0; i < row_end - row_begin + 1; i++) {
            for (int j = 0; j < col_end - col_begin + 1; j++) {
                result[i][j] = m[row_begin + i][col_begin + j];
            }
        }
        return result;
    }
};

//Метод Гаусса c выбором главного элемента
Matrix gauss(const Matrix& coef, const Matrix& right_part) {
    if (coef.row() != coef.col() || coef.row() != right_part.row() || right_part.col() != 1) {
        cerr << "Error in function gauss(): size of coef-matrix must be [n]x[n] and size of right_part-matrix must be [n]x[1].\n";
        exit(-1);
    }
    Matrix a = coef;
    Matrix b = right_part;
    Matrix result(b.row(), 1);
    vector<int> p(a.row());//вектор перестановок столбцов матрицы коэффициентов и соответствующих им строк решения
    //Прямой ход метода Гаусса
    for (int i = 0; i < a.col() - 1; i++) {
        auto [max, row_max, col_max] = a.submatrix(i, i, a.row() - 1, a.col() - 1).abs_max();
        row_max += i;
        col_max += i;
        if (i != row_max) {//Перестановка строк
            swap(a[i], a[row_max]);
            swap(b[i], b[row_max]);
        }
        if (i != col_max) {//Перестановка столбцов
            for (int k = 0; k < a.row(); k++) {
                swap(a[k][i], a[k][col_max]);
                p[i] = col_max;
            }
        }
        if (abs(a[i][i]) < 1e-13) {
            cerr << "Error in fuction gauss(): coef-matrix must not be degenerate.\n";
            exit(-2);
        }
        for (int j = i + 1; j < a.row(); j++) {
            double m = a[j][i] / a[i][i];
            for (int k = i; k < a.col(); k++) {
                a[j][k] -= m * a[i][k];
            }
            b[j][0] -= m * b[i][0];
        }
    }
    //Обратный ход метода Гаусса
    if (abs(a[a.row() - 1][a.col() - 1]) < 1e-13) {
        cerr << "Error in fuction gauss(): coef-matrix must not be degenerate.\n";
        exit(-2);
    }
    for (int i = b.row() - 1; i > -1; i--) {
        double sum = 0.0;
        for (int j = i + 1; j < a.row(); j++) {
            sum += a[i][j] * result[j][0];
        }
        result[i][0] = (b[i][0] - sum) / a[i][i];
    }
    for (int i = p.size() - 1; i >= 0; i--) {//обратная перестановка строк решения
        if (p[i]) {
            swap(result[i][0], result[p[i]][0]);
        }
    }
    return result;
}

//Функция для вывода графиков с помощью gnuplot
void plot(vector<double> t, vector<double> p, string s, int j) {

    FILE* pipe = popen("gnuplot -persist", "w");

    if (!pipe) {
        cerr << "Gnuplot not found\n";
        exit(6);
    }
    fprintf(pipe, "$p << EOD\n");
    for (int i = 0; i < p.size(); i++) {
        fprintf(pipe, "%f\t%f\n", t[i], p[i]);
    }
    fprintf(pipe, "EOD\n");
    fprintf(pipe, "set xlabel 't, с'\nset ylabel '");
    fprintf(pipe, s.c_str());
    fprintf(pipe, "'\n");
    fprintf(pipe, "set title '");
    fprintf(pipe, s.c_str());
    fprintf(pipe, "'\n");
    fprintf(pipe, "set terminal png size 640, 480 \n");
    fprintf(pipe, "set output 'φ_%d.png'\n", j);
    fprintf(pipe, "set style line 1 lt 1 lw 1 pt 1 linecolor rgb \"red\"\n" );
    fprintf(pipe, "set xzeroaxis lt -1\n" );
    fprintf(pipe, "set grid xtics lc rgb '#555555' lw 1 lt 0\n" );
    fprintf(pipe, "set grid ytics lc rgb '#555555' lw 1 lt 0\n" );
    fprintf(pipe, "plot '$p' using 1:2 notitle w l ls 1\n");
    fflush(pipe);
    pclose(pipe);
}

void allplot(vector<double> t, vector<double> p1, vector<double> p2, vector<double> p3, vector<double> p4, string s) {

    FILE* pipe = popen("gnuplot -persist", "w");

    if (!pipe) {
        cerr << "Gnuplot not found\n";
        exit(6);
    }
    fprintf(pipe, "$p1 << EOD\n");
    for (int i = 0; i < p1.size(); i++) {
        fprintf(pipe, "%f\t%f\n", t[i], p1[i]);
    }
    fprintf(pipe, "EOD\n");
    fprintf(pipe, "$p2 << EOD\n");
    for (int i = 0; i < p2.size(); i++) {
        fprintf(pipe, "%f\t%f\n", t[i], p2[i]);
    }
    fprintf(pipe, "EOD\n");
    fprintf(pipe, "$p3 << EOD\n");
    for (int i = 0; i < p3.size(); i++) {
        fprintf(pipe, "%f\t%f\n", t[i], p3[i]);
    }
    fprintf(pipe, "EOD\n");
    fprintf(pipe, "$p4 << EOD\n");
    for (int i = 0; i < p4.size(); i++) {
        fprintf(pipe, "%f\t%f\n", t[i], p4[i]);
    }
    fprintf(pipe, "EOD\n");
    
    fprintf(pipe, "set xlabel 't, с'\nset ylabel '");
    fprintf(pipe, s.c_str());
    fprintf(pipe, "'\n");
    fprintf(pipe, "set title '");
    fprintf(pipe, s.c_str());
    fprintf(pipe, "'\n");
    fprintf(pipe, "set terminal png size 800, 640 \n");
    fprintf(pipe, "set output 'φ.png'\n");
    fprintf(pipe, "set style line 1 lt 1 lw 3 pt 1 linecolor rgb \"red\"\n" );
    fprintf(pipe, "set style line 2 lt 1 lw 1 pt 1 linecolor rgb \"green\"\n" );
    fprintf(pipe, "set style line 3 lt 1 lw 2 pt 1 linecolor rgb \"magenta\"\n" );
    fprintf(pipe, "set style line 4 lt 1 lw 1 pt 1 linecolor rgb \"blue\"\n" );
    fprintf(pipe, "set xzeroaxis lt -1\n" );
    fprintf(pipe, "set grid xtics lc rgb '#555555' lw 1 lt 0\n" );
    fprintf(pipe, "set grid ytics lc rgb '#555555' lw 1 lt 0\n" );
    fprintf(pipe, "plot '$p1' using 1:2 title 'phi_1' w l ls 1, '$p2' using 1:2 title 'phi_2' w l ls 2, '$p3' using 1:2 title 'phi_3' w l ls 3, '$p4' using 1:2 title 'phi_4' w l ls 4\n");
    fflush(pipe);
    pclose(pipe);
}

//Функция заполнения матрицы проводимости и вектора токов
void init(const int time_iteration, const double t, const double dt, Matrix& node_admittance, Matrix& current, const Matrix& basis, const vector<double>& uc, const vector<double>& ucb, const ::vector<double>& il) {
    current[0][0] = -I(t) + basis[0][0] / Re + basis[0][0] / R1 + C * (basis[0][0] - basis[1][0] - uc[time_iteration - 1]) / dt + (il[time_iteration - 1] + dt * (basis[0][0] - basis[1][0]) / L);
    current[1][0] = -C * (basis[0][0] - basis[1][0] - uc[time_iteration - 1]) / dt - (il[time_iteration - 1] + dt * (basis[0][0] - basis[1][0]) / L) +  Cb * (basis[1][0] - basis[2][0] - ucb[time_iteration - 1]) / dt + (basis[1][0] - basis[2][0]) / Ru - Id(basis[2][0], basis[1][0]);
    current[2][0] = -Cb * (basis[1][0] - basis[2][0] - ucb[time_iteration - 1]) / dt - (basis[1][0] - basis[2][0]) / Ru + Id(basis[2][0], basis[1][0]) + (basis[2][0] - basis[3][0]) / Rb;
    current[3][0] = -(basis[2][0] - basis[3][0]) / Rb + basis[3][0] / R2;

    node_admittance[0][0] = 1 / R1 + C / dt + dt / L + 1 / Re;
    node_admittance[0][1] = -C / dt - dt / L;
    node_admittance[1][0] = -C / dt - dt / L;
    node_admittance[1][1] = C / dt + dt / L + Cb / dt + 1 / Ru + dId(basis[2][0], basis[1][0]);
    node_admittance[1][2] = -Cb / dt - 1 / Ru - dId(basis[2][0], basis[1][0]);
    node_admittance[2][1] = -Cb / dt - 1 / Ru - dId(basis[2][0], basis[1][0]);
    node_admittance[2][2] = -Cb / dt + 1 / Ru + 1 / Rb + dId(basis[2][0], basis[1][0]);
    node_admittance[2][3] = - 1 / Rb;
    node_admittance[3][2] = -1 / Rb;
    node_admittance[3][3] = 1 / Rb + 1 / R2;

}

int main() {
    const int n_max = 8;//максимальное число итераций метода Ньютона
    const double dt_min = 1e-7;//минимальный шаг интегрирования по времени
    const double eps = 1e-10;//максимальное значение поправок
    const double eps_min = 1e-3;//нижняя граница для оценки локальной точности
    const double eps_max = 5e-2;//верхняя граница для оценки локальной точности
    const double t_max = 1e-3;//время расчёта
    double t = 0;//время
    double dt = dt_min;//шаг интегрирования по времени
    double dt_prev1 = dt, dt_prev2 = dt;//предыдущие шаги интегрирования по времени
    Matrix basis(4, 1);//вектор базиса метода (узловые потенциалы)
    Matrix basis_prev1(basis.row(), 1), basis_prev2(basis.row(), 1), basis_prev3(basis.row(), 1);//предыдущие значения базиса
    Matrix node_admittance(basis.row(), basis.row());//матрица узловых проводимостей
    Matrix current(basis.row(), 1);//вектор невязок
    vector<double> time;
    time.push_back(t);
    //Переменные состояния
    vector<double> uc;
    uc.push_back(0);
    vector<double> ucb;
    ucb.push_back(0);
    vector<double> il;
    il.push_back(0);
    vector<double> phi1, phi2, phi3, phi4;
    int time_iteration = 1, iter = 1;
    while (dt >= dt_min && t <= t_max) {
        Matrix delta(basis.row(), 1, eps_max + 1);//вектор поправок
        int n = 0;
        basis = ((dt_prev1 + dt) / dt) * (basis_prev1 - basis_prev2) + basis_prev2;//начальные приближения
        while (abs(delta.abs_max().value) > eps && n < n_max) {//метод Ньютона
            init(time_iteration, t, dt, node_admittance, current, basis, uc, ucb, il);
            delta = gauss(node_admittance, -current);
            basis = basis + delta;
            n++;
            iter++;
        }
        if (n > n_max) {
            dt /= 2;
            continue;
        }
        if (time_iteration > 2) {//оценка локальной точности
            double d = 0.5 * dt * dt * abs(((basis_prev1 - basis_prev2) * (1 / (dt_prev1 * dt_prev1)) - (basis_prev2 - basis_prev3) * (1 / (dt_prev1 * dt_prev2))).abs_max().value);
            if (d < eps_min) {
                t += dt;
                dt_prev2 = dt_prev1;
                dt_prev1 = dt;
                dt *= 2;
            }
            else if (d < eps_max) {
                t += dt;
                dt_prev2 = dt_prev1;
                dt_prev1 = dt;
            }
            else {
                dt /= 2;
                continue;
            }
        }
        else {
            t += dt;
            dt_prev2 = dt_prev1;
            dt_prev1 = dt;
        }
        basis_prev3 = basis_prev2;
        basis_prev2 = basis_prev1;
        basis_prev1 = basis;
        time.push_back(t);
        phi1.push_back(basis[0][0]);
        phi2.push_back(basis[1][0]);
        phi3.push_back(basis[2][0]);
        phi4.push_back(basis[3][0]);
        uc.push_back(basis[0][0] - basis[1][0]);
        ucb.push_back(basis[1][0] - basis[2][0]);
        il.push_back(il[time_iteration - 1] + dt * (basis[0][0] - basis[1][0]) / L);
        time_iteration++;
    }
    if (dt < dt_min) {
        cerr << "dt < dt_min at " << time_iteration << " time iteration!\n";
    }
    cout << "Итераций по времени: " << time_iteration << endl;
    cout << "Всего итераций: " << iter << endl;
    plot(time, phi1, "φ_1", 1);
    plot(time, phi2, "φ_2", 2);
    plot(time, phi3, "φ_3", 3);
    plot(time, phi4, "φ_4", 4);
    allplot(time, phi1, phi2, phi3, phi4, "φ");
    return 0;
}
