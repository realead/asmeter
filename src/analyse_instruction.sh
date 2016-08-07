# analyses a command:
# $1 - command to analyse

#build:

INSIDE_LOOP=${2:-100000}
LOOP_RUNS=${3:-100000}

INI_CODE=${4:-""}

echo "\n############## ANALYZING '$1' #######################:\n"

echo "Inside loop: $INSIDE_LOOP, loop cnt $LOOP_RUNS "

python2.7 create_assembly.py -c "$1" -f asm_file.s -r $INSIDE_LOOP -i $LOOP_RUNS -a "$INI_CODE"
gcc -O2 -nostdlib asm_file.s -o prog -lc

### command size:
FILESIZE=$(stat -c%s prog)
BYTES_PER_COMMAND=$(($FILESIZE/$INSIDE_LOOP))


### time needed:
#ELAPSED_TIME=$( { time -f %U ./prog > /dev/null; } 2>&1 )
ELAPSED_TICKS=$(./prog)
echo "Elapsed ticks $ELAPSED_TICKS"

#python, because shell is a pain with floats:
NANOSEC_PER_OPERATION=$(python2.7 calc_speed.py -u $ELAPSED_TICKS -r $INSIDE_LOOP -i $LOOP_RUNS)

echo "$1\t\t\t$BYTES_PER_COMMAND\t\t\t$NANOSEC_PER_OPERATION"

echo "\n############## DONE ANALYZING '$1' #######################:\n"



