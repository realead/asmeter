

def decode_code(code):
    return[ "\t"+x+"\n" for x in code.split("S")]    
    

def check_code(code, code_name):
    bad_strings=["%rcx", "%ecx", "%cx", "%cl", "%ch"]
    for bad in bad_strings:
        if bad in code:
            print >> sys.stderr, "Error: An usage of", bad, "in", code_name, "detected, it may interfere with the boilerplate wrapper, please use any other register"
            print >> sys.stderr, "exiting, no asm_file created"
            exit(42)
    
import argparse
import sys

parser = argparse.ArgumentParser(description='AT&T assembler creator')
parser.add_argument('-c', type=str,
                    help='command which should be injected')
parser.add_argument('-a', type=str, default="",
                    help='initialization code')
parser.add_argument('-f', type=str, default="out.s",
                    help='file name of the resulting assembly')
parser.add_argument('-r', type=int, default=10**4, 
                    help='how many time the code must be inserted inside the loop (default 10000)')
parser.add_argument('-i', type=int, default=10**4,
                    help='the number of times the loop must be repeated (default 10000)')
                                        
args = parser.parse_args()

check_code(args.c, "command")
check_code(args.a, "initialization command")

decoded_code=decode_code(args.c)
decoded_ini_code=decode_code(args.a)

with open(args.f, "w") as f:
    f.write("""
.section  .rodata
cpu_time:
	.string	"%llu\\n"
DOUBLE:#1.00001
	.long	2086323314
	.long	1072693258   
FLOAT:#1.00001
    .long	1065353300
NAN_DOUBLE:
    .long	0
	.long	2146959360
.section .text
    .globl _start
_start:
    call clock
    pushq %rax\n""") 
    
    f.writelines(decoded_ini_code)
    
    f.write("\tmovq ${0}, %rcx\n".format(args.i))
    f.write(
"""loop_start:    
    cmpq $0, %rcx
    je end
    decq %rcx\n""")
    
    for k in xrange(args.r):
        f.writelines(decoded_code)
        
    f.write(
"""    jmp loop_start
end:
    call clock
    popq %rbx
    subq %rbx, %rax

#prepare printf call:
    movq $cpu_time, %rdi
    movq %rax, %rsi
    xorl %eax, %eax
    call printf

#exit status 0
    movq $0, %rdi    
    call exit\n""")
    
