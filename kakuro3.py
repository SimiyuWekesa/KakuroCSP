from csp import Constraint, CSP
from typing import Generic, List, Optional

import sys
import time

codable = []
puzzle = []
clues = []
inputData = []
arr = []
i = 0
a = 0

class uniqConstraint(Constraint[tuple, int]):
    def __init__(self, var1, var2):
        super().__init__([var1, var2])
        self.var1 = var1
        self.var2 = var2

    def satisfied(self, assignment):
        if self.var1 not in assignment or self.var2 not in assignment:
            return True

        return assignment[self.var1] != assignment[self.var2]

class sumConstraint(Constraint[tuple, int]):
    def __init__(self, var, sums, vars):
        super().__init__([var])
        self.var = var
        self.sums = sums
        self.vars = vars

    def satisfied(self, assignment):
        keys = list(assignment.keys())
        values = list(assignment.values())
        pSum = 0
        pNum = 0

        if self.var not in assignment:
            return True
        else:
            for i in range(len(keys)):
                if keys[i] in self.vars:
                    pSum = pSum + assignment[keys[i]]
                    pNum = pNum + 1

            #print(pNum)
            if pNum == len(self.vars) and self.sums == pSum:
                return True
            elif pNum == len(self.vars) and self.sums != pSum:
                return False
            elif pNum < len(self.vars) and self.sums <= pSum:
                return False
            else:
                return True

with open('input.txt', 'r') as f:
    for line in f:
        inputData.append(line.strip())
        i = i + 1

for i in inputData[:8]:
    i = i.replace("f", "F")
    exec(i)
    codable.append(i)

codable.append(inputData[13])

for i in inputData[8:13]:
    puzzle.append(i.split(','))

flat_list = []
for sublist in puzzle:
    for i in sublist:
        flat_list.append(i)

for i in inputData[14:]:
    clues.append(i)

def constraintSort(row, column, sum, direction):
    coord = (row, column)
    sorted = (coord, sum, direction)

    arr.append(sorted)

def Kakuro(declarations, puzzle, clues):
    # Define variables
    variables = [(i, j) for i in range(1, rows + 1) for j in range(1, columns + 1)]
    a = 0

    for i in puzzle:
        if i != '0':
            del variables[a]
            a = a - 1
        a = a + 1

    # Define domains
    domains = {v: set(range(1, 10)) for v in variables}

    csp = CSP(variables, domains)

    # Define constraints
    for i in clues:
        if 'h' in i:
            i = i.replace("h", "'h'")
        elif 'v' in i:
            i = i.replace("v", "'v'")
        exec("constraintSort("+i+")")

    vCopy = variables
    for i in range(len(vCopy)):
        for j in range(len(vCopy)):
            if vCopy[i] != vCopy[j]:
                if vCopy[i][0] == vCopy[j][0] or vCopy[i][1] == vCopy[j][1]:
                    csp.addConstraint(uniqConstraint(vCopy[i], vCopy[j]))

    constDict = {}
    for clue in arr:
        cells = []
        i, j = clue[0]
        if clue[2] == 'h':
            for k in range(1, 5):
                if (i, j + k) in vCopy:
                    cells.append((i, j + k))
        else:
            for k in range(1, 5):
                if (i + k, j) in vCopy:
                    cells.append((i + k, j))

        constDict[clue[1]] = cells

    keys = constDict.keys()

    for i in keys:
        nums = constDict[i]
        for j in nums:
            csp.addConstraint(sumConstraint(j, i, nums))

    print()

    #Begin backtracking search to find solution
    solution = csp.backtracking()

    solved = [(i, j) for i in range(1, rows + 1) for j in range(1, columns + 1)]

    count = 0
    if solution is None:
        print("Failure to find solution")
    else:
        solVars = list(solution.keys())
        with open('output.txt', 'w') as f:
            for i in range(0, len(solved)):
                if solved[i] in solVars:
                    print(str(solution[solved[i]]) + ",", end='')
                    f.write(str(solution[solved[i]]) + ",")
                    count = count + 1
                else:
                    print('#,', end='')
                    f.write('#,')
                    count = count + 1
                if count == 5:
                    print()
                    f.write('\n')
                    count = 0

        print()

Kakuro(codable, flat_list, clues)

