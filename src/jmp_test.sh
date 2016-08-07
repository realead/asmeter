

sh analyse_instruction.sh "jmp .LoooooooooooooooooooooongLabel{loop_id} S .LoooooooooooooooooooooongLabel{loop_id}:" 10000 50000 
sh analyse_instruction.sh "jmp .L{loop_id} S .L{loop_id}:" 5000 500000
sh analyse_instruction.sh "jmp .L{loop_id} S .L{loop_id}:" 2500 500000 
sh analyse_instruction.sh "jmp .L{loop_id} S .L{loop_id}:" 1000 500000 



