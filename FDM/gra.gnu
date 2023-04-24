#!/usr/bin/gnuplot -persistent
set size square
set output 'plot.eps'
set cbrange [0:350]
set xrange[0:15]
set yrange[0:11]
set palette rgbformulae 22,13,-31
set pm3d map
set pm3d flush begin ftriangles scansforwar interpolate 5,5
splot 'out.txt' using 1:2:3 with pm3d title 'var'
pause -1