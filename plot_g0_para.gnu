#asdf
p \
"g0_0021.dat" u 1:2 w lp,\
"g0_0120.dat" u (-$1):(-$2) w lp,\
"g0_0021.dat" u ($1):($3) w lp,\
"g0_0120.dat" u (-$1):($3) w lp
pause -1
