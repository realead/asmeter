# asmeter

A tiny framework for measuring the speed of assembly instructions

## Prerequisites

   1. Linux x86-64
   2. python 2.7
   3. gcc
   4. sh

## Usage

 The framework measures `T` - the time needed for the following pseudo code (using operation `xor %rax,%rax` as example):
 
    for(outer_loop=0; outer_loop<NO;outer_loop++){
        xor %rax,%rax  #first call
        xor %rax,%rax  #second call
        ...
        xor %rax,%rax  #NI-th call
    } 
  
and calculates the average time per operation as `T/(NI*NO)`. As can be see in the section Results - the choice of `N0` and `NI` has an impact on the calculated average time per operation.

To start the analysis e.g. for the operation `xor %rax, %rax` with `NI=1000` and `NO=100` (in folder "src") :
   
    sh analyse_instruction.sh "xor %rax, %rax" 1000 100
  
Then the following happens:
   1. an assembler file is generated (see create_assembly.py)
   2. the generated file is compiled/build
   3. the program runs, the statistics evaluated 
   
The similar output can be seen:

    ############## ANALYZING 'xor %rax,%rax' #######################:

    Inside loop: 1000, loop cnt 100 
    Elapsed ticks 1769389
    xor %rax,%rax			4			0.3538778

    ############## DONE ANALYZING 'xor %rax,%rax' #######################:
    

With  `4` - number of bytes in the executables per instruction, `0.35` nanoseconds per instruction.

#### More than one instruction

It is possible to put more than one instruction into the loop, e.g.

    for(outer_loop=0; outer_loop<NO;outer_loop++){
        instruction 1  #first call
        instruction 2
        instruction 1  #second call
        instruction 2
        ...
        instruction 1  #NI-th call
        instruction 2
    } 

For this call your instructions with separator `S`, e.g.:

    sh analyse_instruction.sh "mov %rax, %rbx S mov %rbx, %rdx" 1000 100

#### Initialisation

it is possible to run initialisation code prior to the entry into the loop. For example for `div %rbx` we need `rbx` to be non-zero and `rdx` to be 0. That could be achieved by setting those values only once

    sh analyse_instruction.sh "div %rbx" 1000 1000 "mov \$1, %rbx S xor %edx, %edx"

as compared to

    sh analyse_instruction.sh "mov \$1, %rbx S xor %edx, %edx S div %rbx" 1000 1000
    
which would set the registers in every iteration.

## Conclusions

#### Meanings of running times

Given the results, which can be found further down, one can conclude the following:

The running time is composed of two parts:

   1. loading instructions (into the cache?)
   2. executing instructions
   
This can be easily seen by comparing the result for high number of inner instructions (`NI`) and for low number of inner instruction.

 The high number of inner instruction results in a big executable, with the whole code not fitting into the memory for instructions and thus every instruction must be loaded over and over again. I.e. for every execution, the instruction must be also loaded. For loading a byte ca. 0.1 ns is needed.

For low number of instruction, the executable size is small and stays the whole time in the memory for instruction (is fetched only once), so we can observe only the time needed for the execution and the time for loading can be neglegted.

The processor is doing a decent job interleaving the fetching and the execution of the instructions, so it can be stated

    T=max(T_load, T_exec)

This can be seen for example on the basis of `xor $65535, %rbx` in the first column - the times are proportional to the size of the instruction.

#### 16bit vs 32bit vs 64bit

For small loops/small executables which can be completely loaded into the memory, there is no difference between 32 and 64 bit.

Yet mostly, the 32bit operations have a smaller size. Thus they should be prefered in order to benefit from smaller loading times, but one should not expect much gain. However get a visible advantages the loops/executables must be pretty big.

16 bit integer operation offer no advanteges compared to 64 bit, but are for some operations (xor, mov) even slower.

The only exception are unsigned multiplication, for which the 64bit version is ca. 40% faster than 16 and 32 bit versions. But they all have the same speed for signed multiplication, which is as fast as 64bit unsigned mutliplication.

It is different for the division through: Here 16 and 32 bit a ca. 40% faster than 64 bit operations.

##### Costs of the operations:
  1. mov - 0.1 ns
  2. xor - 0.35ns, however xor of register with itself needs 0.1s but needs 1 byte less
  3. add - 0.35ns
  4. imul - 1.05ns
  5. mul - 1.05ns (64bit), 1.4ns (32bit)
  6. div - 7.5ns (32bit), 10ns (64bit)
  
#### Floating point operations

There is almost no difference between multiply and add - each operation costs ca. 1.05ns.  There is also no difference for these operations between double and single precision. Also a combimation of mutliply and add didn't change the costs.

However there is factor 50 difference between multiply and divide for double and almost factor 4 difference for single.

No impact of different float values (such as NaN) on the running time could be obserrvved (More testing needed).

## Results

These tables show the time needed per operation in nanoseconds. The time per operation varies depending on parameters `N0` and `NI`. 

### Integer operations

#### xorq vs xorl vs xorw

-- Xoring a register with itself (e.g. `xor %rax, %rax`):

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    xorw(3bytes)          0.40             0.40        0.35            0.35          0.35           0.35
    xorl(2bytes)          0.21             0.21        0.13            0.10          0.09           0.09
    xorq(3bytes)          0.31             0.31        0.20            0.17          0.11           0.09
 
*- results for NI=10^8, NO=50 the same as for NI=10^8, NO=500

-- Xoring two different registers  (e.g. `xor %rax, %rbx`):

    command         NI=10^8, NO=50     (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    xorw(3bytes)        0.40               0.40        0.35           0.35           0.35           0.35
    xorl(2bytes)        0.38               0.38        0.35           0.35           0.35           0.35
    xorq(3bytes)        0.40               0.40        0.35           0.35           0.35           0.35

-- Xoring register with constant 65535  (e.g. `xor $65535, %rbx`):

    command         NI=10^8, NO=50     (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    xorw(4bytes)        0.44               0.44        0.41           0.35           0.35           0.35
    xorl(5bytes)        0.50               0.50        0.47           0.37           0.35           0.35
    xorq(6bytes)        0.65               0.61        0.59           0.40           0.35           0.35 

-- Xoring register with constant a value at stack  (e.g. `xor (%rsp), %rbx`):

    command         NI=10^8, NO=50     (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    xorw(4bytes)        0.46               0.45        0.40           0.35           0.35           0.35
    xorl(3bytes)        0.40               0.40        0.36           0.35           0.35           0.35
    xorq(4bytes)        0.46               0.45        0.39           0.35           0.35           0.35 
    
#### movq vs movl vs movw 
-- moving a const (e.g. `xor $0, %rax`):

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    movw(4bytes)          1.35             1.18        1.15            1.15          1.15           0.35
    movl(5bytes)          0.57             0.52        0.46            0.27          0.12           0.09
    movq(7bytes)          0.86             0.72        0.69            0.37          0.19           0.09 
 
    
-- moving between registers (e.g. `xor %rbx, %rax`):

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    movw(3bytes)          0.39             0.40        0.35            0.35          0.35           0.35
    movl(2bytes)          0.21             0.21        0.13            0.11          0.09           0.09
    movq(3bytes)          0.29             0.29        0.20            0.16          0.10           0.09 
    
#### imulq vs imull vs imulw  

-- e.g. `imul %rbx, %rax`:

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    imulw(4bytes)          1.10             1.07        1.04            1.04          1.04           1.03
    imull(3bytes)          1.07             1.06        1.05            1.04          1.04           1.04
    imulq(4bytes)          1.08             1.08        1.06            1.04          1.04           1.03 
    
#### mulq vs mull vs mulw  
 
-- e.g. `mul %rbx, %rax`:

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    mulw(3bytes)          1.47             1.47        1.47            1.44          1.42           1.42
    mull(2bytes)          1.46             1.46        1.45            1.45          1.44           1.44
    mulq(3bytes)          1.06             1.06        1.07            1.06          1.04           1.04
    
### divq vs divl vs divw
    
-- e.g. `div %rbx`:

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    divw(3bytes)          7.93             7.94        7.96            8.10          7.98           7.98
    divl(2bytes)          7.60             7.57        7.60            7.55          7.55           7.55
    divq(3bytes)         10.85            10.99       10.85            10.85        10.85          10.85
        
#### addq vs addl vs addw  
 
-- e.g. `add %rbx, %rax`:

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    addw(3bytes)          0.40             0.40        0.35            0.35          0.35           0.35
    addl(2bytes)          0.38             0.38        0.35            0.35          0.35           0.35
    addq(3bytes)          0.40             0.40        0.36            0.35          0.35           0.35 
    
 
### Float operations
    
#### mulsd vs mulss

--- e.g. `mulsd %xmm1, %xmm0`: 

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    mulss(4bytes)          1.11             1.11        1.06            1.06          1.05           1.04
    mulsd(4bytes)          1.13             1.11        1.11            1.06          1.06           1.06
    
     
#### divsd vs divss

--- e.g. `divsd %xmm1, %xmm0`: 

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    divss(4bytes)          3.85            3.85        3.85            3.82          3.81            3.80
    divsd(4bytes)          50.0           50.0        50.2            50.3           50.0           50.0
  
#### addsd vs addss

--- e.g. `addsd %xmm1, %xmm0`: 

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    addss(4bytes)          1.07             1.08        1.07            1.05          1.05           1.05
    addsd(4bytes)          1.08             1.08        1.07            1.05          1.05           1.04
    
#### addsd+multsd vs addss+multss

--- e.g. `addsd %xmm1, %xmm0 S multsd %xmm1, %xmm0`: 

    command         NI=10^8, NO=50*    (10^7,500)  (10^6,5*10^3)  (10^5,5*10^4)  (10^4,5*10^5)  (10^3,5*10^6) 
    single(8bytes)        2.15             2.15        2.15            2.07          2.07           2.07
    double(8bytes)        2.16             2.15        2.19            2.09          2.08           2.06
    
        
## Future

  1. further operations
              
