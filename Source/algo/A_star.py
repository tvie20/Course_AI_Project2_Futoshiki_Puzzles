import heapq
import copy
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

def apply_ac3_propagation(board, domains, constraints):
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
                    # Col constraints
                    for r2 in range(N):
                        if r != r2 and val in domains[r2][c]:
                            domains[r2][c].remove(val)
                            changed = True
                            
        # Inequality constraints
        for constraint in constraints:
            r1, c1, op, r2, c2 = constraint
            
            if op == '<':
                if domains[r2][c2]:
                    max_d2 = max(domains[r2][c2])
                    to_remove = [v1 for v1 in domains[r1][c1] if not (v1 < max_d2)]
                    for v1 in to_remove:
                        domains[r1][c1].remove(v1)
                        changed = True
                        
                if domains[r1][c1]:
                    min_d1 = min(domains[r1][c1])
                    to_remove = [v2 for v2 in domains[r2][c2] if not (v2 > min_d1)]
                    for v2 in to_remove:
                        domains[r2][c2].remove(v2)
                        changed = True
                        
            elif op == '>':
                if domains[r2][c2]:
                    min_d2 = min(domains[r2][c2])
                    to_remove = [v1 for v1 in domains[r1][c1] if not (v1 > min_d2)]
                    for v1 in to_remove:
                        domains[r1][c1].remove(v1)
                        changed = True
                        
                if domains[r1][c1]:
                    max_d1 = max(domains[r1][c1])
                    to_remove = [v2 for v2 in domains[r2][c2] if not (v2 < max_d1)]
                    for v2 in to_remove:
                        domains[r2][c2].remove(v2)
                        changed = True

def heuristic_3_ac3(board, constraints):
    domains = get_initial_domains(board)
    apply_ac3_propagation(board, domains, constraints)
    
    for r in range(len(board)):
        for c in range(len(board)):
            if len(domains[r][c]) == 0:
                return float('inf') # Dead end
                
    return heuristic_1_unassigned(board)

def calculate_heuristic(board, constraints, heuristic_choice):
    if heuristic_choice == 'h1':
        return heuristic_1_unassigned(board)
    elif heuristic_choice == 'h2':
        return heuristic_2_chains(board, constraints)
    elif heuristic_choice == 'h3':
        return heuristic_3_ac3(board, constraints)
    return heuristic_1_unassigned(board)

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

def a_star_solve(initial_board, constraints, heuristic_choice='h1'):
    priority_queue = []
    
    h_start = calculate_heuristic(initial_board, constraints, heuristic_choice)
    if h_start == float('inf'):
        return False
        
    heapq.heappush(priority_queue, State(h_start, 0, initial_board))
    
    while priority_queue:
        current_state = heapq.heappop(priority_queue)
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
            
        N = len(current_board)
        
        # Generate successors
        for value in range(1, N + 1):
            if is_valid(current_board, row, col, value, constraints):
                new_board = [r[:] for r in current_board]
                new_board[row][col] = value
                
                new_g = g + 1
                new_h = calculate_heuristic(new_board, constraints, heuristic_choice)
                
                if new_h != float('inf'):
                    new_f = new_g + new_h
                    heapq.heappush(priority_queue, State(new_f, new_g, new_board))
                    
    return False
