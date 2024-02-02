# ALMA| WX2SAT Solver

Instance: A Boolean formula $\phi$ in 2CNF using logic operators $\oplus$ (instead of using the operator $\vee$) and a positive integer $k$.

Question: Is there exists a satisfying truth assignment in which at most $k$ of the variables are true?
 
**Note: This problem is NP-complete (If any NP-complete can be solved in polynomial time, then $P = NP$)**.

# Research

This work is based on the manuscripts [Note for the Millennium Prize Problems](https://www.researchgate.net/publication/377808644_Note_for_the_Millennium_Prize_Problems) and [Note for the P versus NP Problem](https://www.researchgate.net/publication/377656601_Note_for_the_P_versus_NP_Problem).

# Theory

- A literal in a Boolean formula is an occurrence of a variable or its negation. A Boolean formula is in conjunctive normal form, or CNF, if it is expressed as an AND of clauses, each of which is the OR of one or more literals. A Boolean formula is in 2-conjunctive normal form or 2CNF, if each clause has exactly two distinct literals.

- A truth assignment for a Boolean formula $\phi$ is a set of values for the variables in $\phi$. The problem Weighted Xor 2-satisfiability problem (WX2SAT) asks whether a given Boolean formula $\phi$ in 2CNF has a satisfying truth assignment with at most $k$ true variables using logic operators $\oplus$ (instead of using the operator $\vee$).

Example
----- 

Instance: The Boolean formula $(x_{1} \oplus x_{2}) \wedge (x_{2} \oplus \rightharpoondown x_{3})$ where $\oplus$ (XOR), $\wedge$ (AND) and $\rightharpoondown$ (NOT) are the logic operations.

Answer: Yes (we can assign the variables $x_{1}$ as true from a truth assignment to the formula).

Input of this project
-----

The input is on [DIMACS](http://www.satcompetition.org/2009/format-benchmarks2009.html) formula with the extension .cnf.
  
Let's take as the **accept.cnf** from our previous example: The Boolean formula $(x_{1} \oplus x_{2}) \wedge (x_{2} \oplus \rightharpoondown x_{3})$ is
```  
p cnf 3 2
1 2 0
2 -3 0
```  

- The first line **p cnf 3 2** means there are 3 variables and 2 clauses.

- The second line **1 2 0** means the clause $(x_{1} \oplus x_{2})$ (Note that, the number *0* means the end of the clause).

- The third line **2 -3 0** means the clause $(x_{2} \oplus \rightharpoondown x_{3})$ (Note that, the number *0* means the end of the clause).

# Compile and Environment

Downloading and Installing
-----

Download and Install Python 3.0 or a greater version 

-----

# Build and Execute

To build and run from the command prompt:

```
git clone https://github.com/frankvegadelgado/alma.git
cd alma
```

On alma directory run

```
python solver.py -i accept.cnf
```

Finally, it would obtain in the console output:

```
YES
[1]
k = 1
```

which means the minimum amount of true variables is $k = 1$ for every possible satisfying truth assignment and the true variable is $x_{1}$ (i.e. $[1]$).

If we take a non-acceptance instance 

```
python solver.py -i reject.cnf
```

then it would obtain in the console output:

```
NO
```

# Command Options

On alma directory if you run

```
python solver.py -h
```

then you will obtain the following output

```
usage: solver.py [-h] -i INPUTFILE [-v] [-t]

Solve an NP-complete problem from a DIMACS file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        Input file path
  -v, --verbose         Enable verbose output
  -t, --timer           Enable timer output
```

where it is described all the possible options.

# Complexity

````diff
+ We solve this problem in polynomial time using dynamic programming.
+ Consequently, we deduce that P = NP.
````

# Code

- Python code by **Frank Vega**.

# License
- MIT.