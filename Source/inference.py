import sys
import os

# Add the root directory to sys.path to allow imports from test
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test'))
from test_utils import BaseSolver, SearchLimitExceeded
from kb_generator import generate_ground_kb

class ForwardChainingSolver(BaseSolver):
    def solve(self, board, constraints):
        # 1. Start the adapter (build KB) BEFORE timing
        N = len(board)
        horizontal = [[0] * (N - 1) for _ in range(N)]
        vertical = [[0] * N for _ in range(N - 1)]
        
        for (r1, c1, op, r2, c2) in constraints:
            if r1 == r2 and c2 == c1 + 1:
                horizontal[r1][c1] = 1 if op == '<' else -1
            elif c1 == c2 and r2 == r1 + 1:
                vertical[r1][c1] = 1 if op == '<' else -1
                
        puzzle = {"N": N, "grid": board, "horizontal": horizontal, "vertical": vertical}
        kb = generate_ground_kb(puzzle)
        
        # 2. Start the timer now that KB is ready
        self.stats.start_timer()
        
        try:
            return self._run_algorithm(kb)
        except SearchLimitExceeded:
            return None

    def _run_algorithm(self, kb):
        N = kb["N"]
        domains = {cell: set(vals) for cell, vals in kb["domains"].items()}
        
        for constraint in kb["given_constraints"]:
            _, cell, val = constraint
            domains[cell] = {val}

        changed = True
        while changed:
            changed = False
            self.stats.check_limits()
            
            if any(len(d) == 0 for d in domains.values()):
                return False
                
            for i in range(1, N + 1):
                for j in range(1, N + 1):
                    cell = (i, j)
                    if len(domains[cell]) == 1:
                        val = list(domains[cell])[0]
                        
                        for c in range(1, N + 1):
                            if c != j and val in domains[(i, c)]:
                                domains[(i, c)].remove(val)
                                changed = True
                                self.stats.inferences += 1
                                
                        for r in range(1, N + 1):
                            if r != i and val in domains[(r, j)]:
                                domains[(r, j)].remove(val)
                                changed = True
                                self.stats.inferences += 1

            for constraint in kb["inequality_constraints"]:
                ctype, cell_A, cell_B = constraint
                dom_A = domains[cell_A]
                dom_B = domains[cell_B]
                
                if not dom_A or not dom_B:
                    return False

                if ctype == "less":
                    max_B = max(dom_B)
                    to_remove_A = {x for x in dom_A if x >= max_B}
                    if to_remove_A:
                        domains[cell_A] = dom_A - to_remove_A
                        changed = True
                        self.stats.inferences += len(to_remove_A)
                    
                    min_A = min(dom_A)
                    to_remove_B = {x for x in dom_B if x <= min_A}
                    if to_remove_B:
                        domains[cell_B] = dom_B - to_remove_B
                        changed = True
                        self.stats.inferences += len(to_remove_B)

                elif ctype == "greater":
                    min_B = min(dom_B)
                    to_remove_A = {x for x in dom_A if x <= min_B}
                    if to_remove_A:
                        domains[cell_A] = dom_A - to_remove_A
                        changed = True
                        self.stats.inferences += len(to_remove_A)
                    
                    max_A = max(dom_A)
                    to_remove_B = {x for x in dom_B if x >= max_A}
                    if to_remove_B:
                        domains[cell_B] = dom_B - to_remove_B
                        changed = True
                        self.stats.inferences += len(to_remove_B)

        is_solved = all(len(d) == 1 for d in domains.values())
        return is_solved


def is_consistent(assignment, cell, val, N, inequality_constraints):
    i, j = cell
    for c in range(1, N + 1):
        if (i, c) in assignment and assignment[(i, c)] == val:
            return False
            
    for r in range(1, N + 1):
        if (r, j) in assignment and assignment[(r, j)] == val:
            return False

    for constraint in inequality_constraints:
        ctype, cell_A, cell_B = constraint
        
        if cell_A in assignment and cell_B in assignment:
            if ctype == "less" and not (assignment[cell_A] < assignment[cell_B]): return False
            if ctype == "greater" and not (assignment[cell_A] > assignment[cell_B]): return False
        elif cell == cell_A and cell_B in assignment:
            if ctype == "less" and not (val < assignment[cell_B]): return False
            if ctype == "greater" and not (val > assignment[cell_B]): return False
        elif cell == cell_B and cell_A in assignment:
            if ctype == "less" and not (assignment[cell_A] < val): return False
            if ctype == "greater" and not (assignment[cell_A] > val): return False
    return True

class BackwardChainingSolver(BaseSolver):
    def solve(self, board, constraints):
        # 1. Start the adapter (build KB) BEFORE timing
        N = len(board)
        horizontal = [[0] * (N - 1) for _ in range(N)]
        vertical = [[0] * N for _ in range(N - 1)]
        
        for (r1, c1, op, r2, c2) in constraints:
            if r1 == r2 and c2 == c1 + 1:
                horizontal[r1][c1] = 1 if op == '<' else -1
            elif c1 == c2 and r2 == r1 + 1:
                vertical[r1][c1] = 1 if op == '<' else -1
                
        puzzle = {"N": N, "grid": board, "horizontal": horizontal, "vertical": vertical}
        kb = generate_ground_kb(puzzle)
        
        # 2. Start the timer now that KB is ready
        self.stats.start_timer()
        
        try:
            return self._run_algorithm(kb)
        except SearchLimitExceeded:
            return None

    def _run_algorithm(self, kb):
        N = kb["N"]
        inequality_constraints = kb["inequality_constraints"]
        
        assignment = {}
        for constraint in kb["given_constraints"]:
            _, cell, val = constraint
            assignment[cell] = val

        unassigned_cells = []
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if (i, j) not in assignment:
                    unassigned_cells.append((i, j))

        def backtrack(index):
            self.stats.check_limits()
            
            if index == len(unassigned_cells):
                return True
                
            cell = unassigned_cells[index]
            
            # Popping a subgoal
            self.stats.inferences += 1
            
            for val in kb["domains"][cell]:
                if is_consistent(assignment, cell, val, N, inequality_constraints):
                    assignment[cell] = val
                    
                    if backtrack(index + 1):
                        return True
                        
                    del assignment[cell]
                    
            return False

        if backtrack(0):
            return True
        return False