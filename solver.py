#                          SAT Solver
#                          Frank Vega
#                        February 1, 2024
#        We use Z3 that is a theorem prover from Microsoft Research.

import argparse
import sys
import z3
z3.set_option(model=True)
z3.set_param("parallel.enable", False)
k=0
s=0
maximum=0
mapped = {}

def parse_dimacs(asserts):
    global mapped, k, maximum
    result = []
    for strvar in asserts:
        line = strvar.strip()
        if not line.startswith('p') and not line.startswith('c'):
            expr = line.split(" ")
            expr = expr[:-1]
            l = []
            for t in expr:
                v = int(t)
                l.append(v)
                value = abs(v)
                if value not in mapped:
                    mapped[value] = k
                    k += 1
                    maximum = value if (maximum < value) else maximum
            result.append(list(set(l)))        
    return result   
                       
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve an NP-complete problem from a DIMACS file.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    
    args = parser.parse_args()

    #Read and parse a dimacs file
    file = open(args.inputFile, 'r')
    #Format from dimacs
    asserts = file.readlines()    
    clauses = parse_dimacs(asserts[1:])
    