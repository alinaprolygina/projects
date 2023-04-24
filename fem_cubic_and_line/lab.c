#include <stdio.h>
#include <math.h>
#include <stdlib.h>

void makeSLAU1 (int nodesNum, int i, int j, double fem_size, double a, double b, double c, double d, double* mainArr, double* left_vector)
{
    mainArr[i*nodesNum + i] += -a/fem_size - b/2. + c*fem_size/3.;
    mainArr[i*nodesNum + j] += a/fem_size + b/2. + c*fem_size/6.;
    mainArr[j*nodesNum + i] += a/fem_size - b/2. + c*fem_size/6.;
    mainArr[j*nodesNum + j] += -a/fem_size + b/2. + c*fem_size/3.;
    left_vector[i] += -d*fem_size/2.;
    left_vector[j] += -d*fem_size/2.;
}

void makeSlae3 (int nodesNum, int i, int j, int k, int h, double fem_size, double a, double b, double c, double d, double* mainArr, double* left_vector)
{
    mainArr[i*nodesNum + i] += -a*37/ (10*fem_size) - b/2. + c*8*fem_size/105.;
    mainArr[i*nodesNum + j] += a*189/ (40*fem_size) + b*57/80. + c*33*fem_size/560.;
    mainArr[i*nodesNum + k] += -a*27/ (20*fem_size) - b*3/10. - c*3*fem_size/140.;
    mainArr[i*nodesNum + h] += a*13/ (40*fem_size) + b*7/80. + c*19*fem_size/1680.;
    mainArr[j*nodesNum + i] += a*189/ (40*fem_size) - b*57/80. + c*33*fem_size/560.;
    mainArr[j*nodesNum + j] += -a*54/ (5*fem_size) + c*27*fem_size/70.;
    mainArr[j*nodesNum + k] += a*297/ (40*fem_size) + b*81/80. - c*27*fem_size/560.;
    mainArr[j*nodesNum + h] += -a*27/ (20*fem_size) - b*3/10. - c*3*fem_size/140.;
    mainArr[k*nodesNum + i] += -a*27/ (20*fem_size) + b*3/10. - c*3*fem_size/140.;
    mainArr[k*nodesNum + j] += a*297/ (40*fem_size) - b*81/80. - c*27*fem_size/560.;
    mainArr[k*nodesNum + k] += -a*54/ (5*fem_size) + c*27*fem_size/70.;
    mainArr[k*nodesNum + h] += a*189/ (40*fem_size) + b*57/80. + c*33*fem_size/560.;
    mainArr[h*nodesNum + i] += a*13/ (40*fem_size) - b*7/80. + c*19*fem_size/1680.;
    mainArr[h*nodesNum + j] += -a*27/ (20*fem_size) + b*3/10. - c*3*fem_size/140.;
    mainArr[h*nodesNum + k] += a*189/ (40*fem_size) - b*57/80. + c*33*fem_size/560.;
    mainArr[h*nodesNum + h] += -a*37/ (10*fem_size) + b/2. + c*8*fem_size/105.;
    left_vector[i] += -d*fem_size/8.;
    left_vector[j] += -d*3*fem_size/8.;
    left_vector[k] += -d*3*fem_size/8.;
    left_vector[h] += -d*fem_size/8.;
}

void first_border (int nodesNum, double* mainArr, double* left_vector, int i,
                   double a, double bVal)
{
    for (int j = 0; j < nodesNum; ++j)
    {
        mainArr[i*nodesNum+j] = 0;
    }
    mainArr[i*nodesNum+i] = 1;
    left_vector[i] = bVal;
}

void border2 (int nodesNum, double* mainArr, double* left_vector, int i, double
a, double bVal)
{
    if (i == 0)
    {
        left_vector[i] += bVal * a;
    }
    else
    {
        left_vector[i] -= bVal * a;
    }
}

void SLAUsolve (int nodesNum, double* amp, double* mainArr, double* left_vector)
{
    for (int i = 0; i < nodesNum; ++i)
    {
        for (int j = i+1; j < nodesNum; ++j)
        {
            double c = (mainArr[j*nodesNum+i])/ (mainArr[i*nodesNum+i]);
            for (int k = i; k < nodesNum; ++k)
            {
                mainArr[j*nodesNum+k] -= mainArr[i*nodesNum+k] * c;
            }
            left_vector[j] -= left_vector[i] * c;
        }
    }
    for (int i = nodesNum-1; i >= 0; --i)
    {
        double tmp = 0;
        for (int j = i+1; j < nodesNum; ++j)
        {
            tmp += amp[j] * mainArr[i*nodesNum+j];
        }
        amp[i] = (left_vector[i] - tmp)/mainArr[i*nodesNum+i];
    }
}

int main (int argc, char** argv)
{
    int femType = atoi (argv[2]);
    int count_fem = atoi (argv[1]);
    int nodesNum = count_fem*femType+1;
    double mainArr[nodesNum*nodesNum], left_vector[nodesNum];
    double a = 4;
    double b = 0;
    double c = -6;
    double d = 11;
    if (femType != 1 && femType != 3)
    {
        printf ("Type must be 1 or 3!!\n");
        exit (0);
    }
    double valX[nodesNum], trued[nodesNum], amp[nodesNum];
    double lft = 2.0,vRight = 12.0;
    double fem_size = (vRight-lft)/ count_fem;
    FILE *pointer_file;
    for (int i = 0; i < nodesNum; ++i)
        valX[i] = lft + (vRight-lft) * i / (nodesNum-1);
// True solve
    double C1 = 18.9142689829;
    double C2 = 0.00000172579;
    for (int i = 0; i < nodesNum; ++i)
    {
        trued[i] = C1*exp (-sqrt(3/2.)*valX[i])+C2*exp
                (sqrt(3/2.)*valX[i])+11/6.;
    }
// Computing
    for (int i = 0; i < nodesNum*nodesNum; ++i) mainArr[i] = 0;
    for (int i = 0; i < nodesNum; ++i) left_vector[i] = 0;
    for (int i = 0; i < count_fem; ++i)
    {
        if (femType == 1)
        {
            makeSLAU1 (nodesNum, i*femType, i*femType+1, fem_size, a, b, c, d, mainArr, left_vector);
        }else if (femType == 3)
        {
            makeSlae3 (nodesNum, i*femType, i*femType+1, i*femType+2, i*femType+3, fem_size, a, b, c, d, mainArr, left_vector);
        }
    }
    border2 (nodesNum, mainArr, left_vector, 0, a, -2);
    first_border (nodesNum, mainArr, left_vector, nodesNum-1, a, 6);
    SLAUsolve (nodesNum, amp, mainArr, left_vector);
    double errAbs = 0.;
    for (int i = 0; i < nodesNum-1; ++i)
    {
        double err = fabs (amp[i]-trued[i]);
        if (err > errAbs) errAbs = err;
    }
    printf ("Max ERROR: %lf\n", errAbs);

    // Gnuplot
    FILE* gp = popen("gnuplot -persist", "w");
    fprintf(gp, "$Analytic << EOD\n");
    for (size_t i = 0; i < nodesNum; i++) {
        fprintf(gp, "%lf %lf\n", valX[i], amp[i]);
    }
    if (femType == 1){
        fprintf(gp, "EOD\n");
        fprintf(gp, "$linear << EOD\n");
        for (size_t i = 0; i < nodesNum; i++) {
            fprintf(gp, "%lf %lf\n", valX[i], trued[i]);
        }
        fprintf(gp, "EOD\n");
        fprintf(gp, "set grid\n");
        fprintf(gp, "plot '$linear' using 1:2 with lp lc '#DC143C' lw 2.5 pt 7 ps 0.5 title ' Linear solution ', '$Analytic' using 1:2 with lines lc rgb '#00FF00' lt 1 lw 1.5 title ' Analytic solution ',\n");
    }else{
        fprintf(gp, "EOD\n");
        fprintf(gp, "$Cube << EOD\n");
        for (size_t i = 0; i < nodesNum; i++) {
            fprintf(gp, "%lf %lf\n", valX[i], trued[i]);
        }
        fprintf(gp, "EOD\n");
        fprintf(gp, "set grid\n");
        fprintf(gp, "plot '$Cube' using 1:2 with lp lc '#FF0000' lw 2.5 pt 7 ps 0.5 title ' Cube solution ', '$Analytic' using 1:2 with lines lc rgb '#00FF00' lt 1 lw 1.5 title ' Analytic solution ',\n");
    }

// Output in file
    pointer_file = fopen ("output.txt", "w");
    for (int i = 0; i < nodesNum; ++i)
    {
        fprintf (pointer_file, "%lf\t%lf\t%lf\t%e\n", valX[i], amp[i], trued[i], fabs(amp[i]-trued[i]));
    }
    return 0;
}
