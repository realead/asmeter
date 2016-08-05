
for cmd in "nop" "jmp L{loop_id} S L{loop_id}:"
do
    for pars  in "100000 50000" "10000 500000" "1000 5000000" 
    do
       sh analyse_instruction.sh "$cmd" $pars "movsd NAN_DOUBLE, %xmm0 S movsd NAN_DOUBLE, %xmm1"
    done 
done


