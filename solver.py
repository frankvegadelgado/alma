#                         MWX2SAT Solver
#                          Frank Vega
#                        February 2, 2024

import argparse
import sys
import collections
import time
mapped = {}
f = {}
g = {}
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
        return [(node[0]+1, node[1]+1, node[2]+f[node[0]+1], node[3]-g[node[0]+1]), 
        (node[0]+1, node[1], node[2]-g[node[0]+1], node[3]+f[node[0]+1])]

def bfs(start):
    
    logging("Start searching the solution")
    if timed:
        started = time.time()
    
    
    visited = set()
    queue = collections.deque([start])
    visited.add(start)
    hash = {}
    
    while queue:
        node = queue.popleft()
        neighbors = graph(node)
        for neighbor in neighbors:
            if neighbor not in visited:
                hash[neighbor] = node
                visited.add(neighbor)
                queue.append(neighbor)

    if timed:
        logging(f"Done searching the solution in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Done searching the solution")
    
                
                
    return (visited, hash)


def fill_data(clauses):
    global mapped, f, g, h
    
    logging("Start storing the memory data")
    if timed:
        started = time.time()
    
    for z in mapped:
        f[z], g[z] = 0, 0
        for list in clauses:
            if z in list:
                arr = [y for y in list if z != y]
                if z < arr[0]:
                    f[z] = f[z] + 1
                else:
                    g[z] = g[z] + 1
                
                            
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
            if len(expr) != 2:
                raise Exception("The Boolean formula must contain exactly 2 variables per each clause")
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
    
    
    (visited, hash) = bfs((0, 0, 0, 0))
    accept = False
    
    for k in range(len(mapped)):
        acceptance = (len(mapped), k+1, 0, 0)
        if acceptance in visited:
            truth = []
            while acceptance != (0, 0, 0, 0):
                node = hash[acceptance]
                neighbors = graph(node)
                if neighbors[0] == acceptance:
                    truth.append(acceptance[0])
                acceptance = node
            if len(truth) == k+1:        
                print("YES")
                print(truth, sep=", ")
                print(f"k = {len(truth)}")
                accept = True
                break
    if not accept:
        print("NO")