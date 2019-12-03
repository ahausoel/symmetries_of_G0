#asdf
p \
"g0_0021.dat" u 1:2 w lp,\
"g0_2100.dat" u (-$1):($2) w lp,\
"g0_0021.dat" u ($1):($3) w lp,\
"g0_2100.dat" u (-$1):(-$3) w lp
pause -1
