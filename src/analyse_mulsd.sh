

#initialize xmm0 und xmm1 und teste for double and single

for cmd in "mulsd %xmm1,%xmm0" "mulss %xmm1,%xmm0"
do
    for pars  in "100000000 50" "10000000 500" "1000000 5000" "100000 50000" "10000 500000" "1000 5000000" 
    do
       sh analyse_instruction.sh "$cmd" $pars "movsd NAN_DOUBLE, %xmm0 S movsd NAN_DOUBLE, %xmm1"
    done 
done


