from algo.solver_utils import find_first_empty_cell, is_valid
import sys
import os

# Add the test directory directly to sys.path to avoid clash with stdlib 'test'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test'))
from test_utils import BaseSolver, SearchLimitExceeded

def is_board_valid(board, constraints):
    """
    Full validation of a completely filled board.
    """
    N = len(board)
    
    # Check all rows and columns
    for i in range(N):
        row_set = set()
        col_set = set()
        for j in range(N):
            if board[i][j] == 0:
                return False
            row_set.add(board[i][j])
            
            if board[j][i] == 0:
                return False
            col_set.add(board[j][i])
            
        if len(row_set) != N or len(col_set) != N:
            return False
            
    # Check all constraints
    for constraint in constraints:
        r1, c1, op, r2, c2 = constraint
        val1 = board[r1][c1]
        val2 = board[r2][c2]
        
        if val1 == 0 or val2 == 0:
            return False
            
        if op == '<' and not (val1 < val2):
            return False
        if op == '>' and not (val1 > val2):
            return False
            
    return True

class BruteForceSolver(BaseSolver):
    def _run_algorithm(self, board, constraints):
        self.stats.expansions += 1
        self.stats.check_limits()
        
        row, col = find_first_empty_cell(board)
        
        # Base case: Board is full
        if row is None:
            return is_board_valid(board, constraints)
            
        N = len(board)
        for value in range(1, N + 1):
            board[row][col] = value
            
            if self.record_steps:
                self.steps.append({
                    "step": self.stats.expansions,
                    "board": [r[:] for r in board]
                })
            
            # Recursively solve without prior checking
            if self._run_algorithm(board, constraints):
                return True
                
            # Undo assignment if it leads to failure
            board[row][col] = 0
            
        return False
