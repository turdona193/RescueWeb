set terminal png transparent size 640,240
set size 1.0,1.0

set terminal png transparent size 640,480
set output 'lines_of_code_by_author.png'
set key left top
set xdata time
set timefmt "%s"
set format x "%Y-%m-%d"
set grid y
set ylabel "Lines"
set xtics rotate
set bmargin 6
plot 'lines_of_code_by_author.dat' using 1:2 title "NicholasTurdo" w lines, 'lines_of_code_by_author.dat' using 1:3 title "Lee Page" w lines, 'lines_of_code_by_author.dat' using 1:4 title "Edward Banner" w lines, 'lines_of_code_by_author.dat' using 1:5 title "Tim Simmons" w lines, 'lines_of_code_by_author.dat' using 1:6 title "Jeremy" w lines, 'lines_of_code_by_author.dat' using 1:7 title "kosowsjm195" w lines, 'lines_of_code_by_author.dat' using 1:8 title "Brian C. Ladd" w lines, 'lines_of_code_by_author.dat' using 1:9 title "Sonja Costa" w lines, 'lines_of_code_by_author.dat' using 1:10 title "Jeff" w lines, 'lines_of_code_by_author.dat' using 1:11 title "pagel194" w lines, 'lines_of_code_by_author.dat' using 1:12 title "Bill Kline" w lines
