import heapq
import sys
import os

# Add the test directory directly to sys.path to avoid clash with stdlib 'test'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test'))
from test_utils import BaseSolver, SearchLimitExceeded
from algo.solver_utils import find_first_empty_cell, is_valid

def heuristic_1_unassigned(board):
    count = 0
    for row in board:
        for val in row:
            if val == 0:
                count += 1
    return count

def heuristic_2_chains(board, constraints):
    involved = set()
    for constraint in constraints:
        r1, c1, op, r2, c2 = constraint
        if board[r1][c1] == 0:
            involved.add((r1, c1))
        if board[r2][c2] == 0:
            involved.add((r2, c2))
    return len(involved)

def get_initial_domains(board):
    N = len(board)
    domains = [[set() for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                domains[r][c] = set(range(1, N + 1))
            else:
                domains[r][c] = {board[r][c]}
    return domains

def apply_ac3_propagation(board, domains, constraints, stats=None):
    N = len(board)
    changed = True
    while changed:
        changed = False
        
        for r in range(N):
            for c in range(N):
                if len(domains[r][c]) == 1:
                    val = next(iter(domains[r][c]))
                    # Row constraints
                    for c2 in range(N):
                        if c != c2 and val in domains[r][c2]:
                            domains[r][c2].remove(val)
                            changed = True
                            if stats: stats.inferences += 1
                    # Col constraints
                    for r2 in range(N):
                        if r != r2 and val in domains[r2][c]:
                            domains[r2][c].remove(val)
                            changed = True
                            if stats: stats.inferences += 1
                            
        # Inequality constraints
        for constraint in constraints:
            if stats: stats.check_limits()
            r1, c1, op, r2, c2 = constraint
            
            if op == '<':
                if domains[r2][c2]:
                    max_d2 = max(domains[r2][c2])
                    to_remove = [v1 for v1 in domains[r1][c1] if not (v1 < max_d2)]
                    for v1 in to_remove:
                        domains[r1][c1].remove(v1)
                        changed = True
                        if stats: stats.inferences += 1
                        
                if domains[r1][c1]:
                    min_d1 = min(domains[r1][c1])
                    to_remove = [v2 for v2 in domains[r2][c2] if not (v2 > min_d1)]
                    for v2 in to_remove:
                        domains[r2][c2].remove(v2)
                        changed = True
                        if stats: stats.inferences += 1
                        
            elif op == '>':
                if domains[r2][c2]:
                    min_d2 = min(domains[r2][c2])
                    to_remove = [v1 for v1 in domains[r1][c1] if not (v1 > min_d2)]
                    for v1 in to_remove:
                        domains[r1][c1].remove(v1)
                        changed = True
                        if stats: stats.inferences += 1
                        
                if domains[r1][c1]:
                    max_d1 = max(domains[r1][c1])
                    to_remove = [v2 for v2 in domains[r2][c2] if not (v2 < max_d1)]
                    for v2 in to_remove:
                        domains[r2][c2].remove(v2)
                        changed = True
                        if stats: stats.inferences += 1

def heuristic_3_ac3(board, constraints, stats=None):
    domains = get_initial_domains(board)
    apply_ac3_propagation(board, domains, constraints, stats)
    
    for r in range(len(board)):
        for c in range(len(board)):
            if len(domains[r][c]) == 0:
                return float('inf') # Dead end
                
    return heuristic_1_unassigned(board)

def calculate_heuristic(board, constraints, heuristic_choice, stats=None):
    import time
    start_time = time.perf_counter()
    
    if heuristic_choice == 'h1':
        res = heuristic_1_unassigned(board)
    elif heuristic_choice == 'h2':
        res = heuristic_2_chains(board, constraints)
    elif heuristic_choice == 'h3':
        res = heuristic_3_ac3(board, constraints, stats)
    else:
        res = heuristic_1_unassigned(board)
        
    if stats:
        stats.heuristic_time += time.perf_counter() - start_time
        
    return res

class State:
    def __init__(self, f, g, board):
        self.f = f
        self.g = g
        self.board = board
        
    def __lt__(self, other):
        # Tie-break on g (prefer deeper nodes if f is same to act like DFS/Greedy)
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

class AStarSolver(BaseSolver):
    def __init__(self, time_limit=60.0, max_expansions=1000000, max_inferences=1000000, heuristic_choice='h1', record_steps=False):
        super().__init__(time_limit, max_expansions, max_inferences)
        self.heuristic_choice = heuristic_choice
        self.record_steps = record_steps
        self.steps = []  # populated when record_steps=True

    def _run_algorithm(self, initial_board, constraints):
        priority_queue = []
        self.steps = []  # reset on each run
        
        h_start = calculate_heuristic(initial_board, constraints, self.heuristic_choice, self.stats)
        if h_start == float('inf'):
            return False
            
        heapq.heappush(priority_queue, State(h_start, 0, initial_board))
        
        while priority_queue:
            self.stats.check_limits()
            
            current_state = heapq.heappop(priority_queue)
            self.stats.expansions += 1
            
            f = current_state.f
            g = current_state.g
            current_board = current_state.board
            
            row, col = find_first_empty_cell(current_board)
            
            # Base Case: Board is full
            if row is None:
                # Copy solution back to initial_board
                for r in range(len(current_board)):
                    for c in range(len(current_board)):
                        initial_board[r][c] = current_board[r][c]
                return True
            
            # Record step metadata (array-based, no yield/callbacks)
            if self.record_steps:
                self.steps.append({
                    "step": self.stats.expansions,
                    "cell": (row, col),       # 0-indexed
                    "g": g,
                    "h": f - g,               # h = f - g
                    "f": f,
                    "board": [r[:] for r in current_board],  # snapshot
                })
                
            N = len(current_board)
            
            # Generate successors
            for value in range(1, N + 1):
                if is_valid(current_board, row, col, value, constraints):
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = value
                    
                    new_g = g + 1
                    new_h = calculate_heuristic(new_board, constraints, self.heuristic_choice, self.stats)
                    
                    if new_h != float('inf'):
                        new_f = new_g + new_h
                        heapq.heappush(priority_queue, State(new_f, new_g, new_board))
                        
        return False
