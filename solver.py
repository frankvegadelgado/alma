#                          SAT Solver
#                          Frank Vega
#                        February 1, 2024
#        We use Z3 that is a theorem prover from Microsoft Research.

import argparse
import sys
import z3
import collections
import time
mapped = {}
f = {}
g = {}
h = {}
log = False
timed = False
started = 0.0

def logging(message):
    if log:
        print(message)

def graph(node):
    global mapped, f, g, h
    if node[0] >= len(mapped):
        return []
    else:
        return [(node[0]+1, node[1]+f[node[0]+1]+g[node[0]+1]+h[node[0]+1], node[2]+f[node[0]+1]+h[node[0]+1], node[3]-g[node[0]+1]-h[node[0]+1]), 
        (node[0]+1, node[1], node[2]-g[node[0]+1], node[3]+f[node[0]+1])]

def bfs(start):
    
    logging("Start searching the solution")
    if timed:
        started = time.time()
    
    
    visited = set()
    queue = collections.deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        neighbors = graph(node)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    if timed:
        logging(f"Done searching the solution in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Done searching the solution")
    
                
                
    return visited


def fill_data(clauses):
    global mapped, f, g, h
    
    logging("Start storing the memory data")
    if timed:
        started = time.time()
    
    for z in mapped:
        f[z], g[z], h[z] = 0, 0, 0
        for list in clauses:
            if z in list:
                arr = [y for y in list if z != y]
                if z < arr[0] and z < arr[1]:
                    f[z] = f[z] + 1
                elif z > arr[0] and z > arr[1]:
                    g[z] = g[z] + 1
                else:
                    h[z] = h[z] + 1
                            
    if timed:
        logging(f"Done storing the memory data in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Done storing the memory data")
    
            

def parse_dimacs(asserts):
    global mapped, k, maximum
    result = []
    for strvar in asserts:
        line = strvar.strip()
        if not line.startswith('p') and not line.startswith('c'):
            expr = line.split(" ")
            expr = expr[:-1]
            l = []
            expr = list(set(expr))
            if len(expr) != 3:
                raise Exception("The Boolean formula must exactly 3 variables per each clause")
            for t in expr:
                v = int(t)
                l.append(v)
                value = abs(v)
                if value != v:
                    raise Exception("The Boolean formula must not contain negated variables")
                if value not in mapped:
                    mapped[value] = True
            result.append(l)        
    return result   
                       
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve an NP-complete problem from a DIMACS file.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = parser.parse_args()

    log = args.verbose
    timed = args.timer

    #Read and parse a dimacs file
    logging("Pre-processing started")
    if timed:
        started = time.time()
    file = open(args.inputFile, 'r')
    #Format from dimacs
    asserts = file.readlines()    
    clauses = parse_dimacs(asserts[1:])
    
    if timed:
        logging(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Pre-processing done")
    
    fill_data(clauses)
    
    
    states = bfs((0, 0, 0, 0))
    acceptance = (len(mapped), len(clauses), 0, 0)
    if acceptance not in states:
        print("NO")
    else:
        print("YES")