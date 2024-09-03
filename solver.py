#                         MWX2SAT Solver
#                          Frank Vega
#                       Sept 3rd, 2024

import argparse
import sys
import time
import networkx 
mapped = {}
log = False
timed = False
started = 0.0
userinput = 1

def logging(message):
    if log:
        print(message)

def independent_vertex_cover(graph):
    logging("Start searching the solution")
    if timed:
        started = time.time()
    
    solution = []
    
    if networkx.algorithms.bipartite.is_bipartite(graph):
        components = networkx.connected_components(graph)
        for component in components:    
            G = networkx.Graph(networkx.induced_subgraph(graph, component))
            matching = networkx.bipartite.maximum_matching(G)
            vertex_cover = networkx.bipartite.to_vertex_cover(G, matching)
            solution = solution + list(vertex_cover)
    
    if timed:
        logging(f"Done searching the solution in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Done searching the solution")
    
    if len(solution) > 0:
        return solution
    else:
        return None
    
  
def fill_graph(clauses):
    global mapped
    
    logging("Start creating the polynomial time reduction")
    if timed:
        started = time.time()
    edges = []
    
    
    for list in clauses:
        edges.append((list[0], list[1]))        
    graph = networkx.Graph()
    graph.add_edges_from(edges)  
    if timed:
        logging(f"Done polynomial time reduction in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Done polynomial time reduction")
    
    return graph
            

def parse_dimacs(asserts):
    global mapped
    result = []
    cvars = 1
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
        elif line.startswith('p'):
            expr = line.split(" ")
            cvars = int(expr[2])
    for i in range(cvars):
        if (i + 1) not in mapped:
            raise Exception(f"The Boolean formula must contain all variables between 1 and {cvars}")
    return result   
                       
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve an NP-complete problem from a DIMACS file.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = parser.parse_args()

    log = args.verbose
    timed = args.timer
    
    #Read the parameter k
    try: 
        userinput = int(input("Enter the positive integer k:")) 
    except ValueError: 
        raise Exception("That's not an integer")
    
    if userinput <= 0:
        raise Exception("That's not a positive integer")
    print("You entered %d"%userinput)

    
    #Read and parse a dimacs file
    logging("Pre-processing started")
    if timed:
        started = time.time()
    file = open(args.inputFile, 'r')
    #Format from dimacs
    asserts = file.readlines()    
    clauses = parse_dimacs(asserts)
    
    if timed:
        logging(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Pre-processing done")
    
    graph = fill_graph(clauses)
    
    
    answer = independent_vertex_cover(graph)

    if answer is None:
        print("NO")
    else:
        if len(answer) <= userinput:
            print("YES")
            print(answer, sep=", ")
            print(f"k = {len(answer)}")
        else:
            print("NO")
        