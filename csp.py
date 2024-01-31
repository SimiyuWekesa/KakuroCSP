from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V')
D = TypeVar('D')

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...


class CSP(Generic[V, D]):
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                print("Should have a domain")

    def addConstraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                print("Variable not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking(self, assignment: Dict[V, D] = {}):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]

        first = unassigned[0]
        for value in self.domains[first]:
            asgnCopy = assignment.copy()
            asgnCopy[first] = value

            if self.consistent(first, asgnCopy):
                result = self.backtracking(asgnCopy)

                if result is not None:
                    return result

        return None

    def mac(csp, var, value, assignment, removals, constraint_propagation):
        return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

    def forward_checking(csp, var, value, assignment, removals):
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b):
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    return False
        return True

    def AC_3(csp) -> bool:
        queue = deque(csp.constraints)

        while queue:
            (Xi, Xj) = queue.popleft()

            if revise(csp, Xi, Xj):
                if not csp.domains[Xi]:
                    return False
                for Xk in csp.neighbors[Xi] - {Xj}:
                    queue.append((Xk, Xi))

        return True

    def revise(csp, Xi, Xj) -> bool:
        revised = False

        for x in csp.domains[Xi]:
            if not any(csp.constraints[(Xi, Xj)](x, y) for y in csp.domains[Xj]):
                csp.domains[Xi].remove(x)
                revised = True

        return revised

    def lcv(var, assignment, csp):
        return sorted(csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment))

    def mrv(assignment, csp):
        return argmin_random_tie([v for v in csp.variables if v not in assignment],
                                 key=lambda var: num_legal_values(csp, var, assignment))
