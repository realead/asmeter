
import argparse

parser = argparse.ArgumentParser(description='prints ')
parser.add_argument('-u', type=float,
                    help='running time in seconds')
parser.add_argument('-r', type=int, 
                    help='how many time the code is inserted inside')
parser.add_argument('-i', type=int, 
                    help='the number of times the loop is repeated')
                                        
args = parser.parse_args()


#in POSTFIX CLOCK_PER_SECOND is 10**6
factor_for_ns=1000
print args.u*factor_for_ns/(args.i*args.r)

    
