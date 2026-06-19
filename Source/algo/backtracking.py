from algo.solver_utils import find_first_empty_cell, is_valid
import sys
import os

# Add the test directory directly to sys.path to avoid clash with stdlib 'test'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test'))
from test_utils import BaseSolver, SearchLimitExceeded

class BacktrackingSolver(BaseSolver):
    def _run_algorithm(self, board, constraints):
        self.stats.expansions += 1
        self.stats.check_limits()
        
        row, col = find_first_empty_cell(board)
        
        # Base case: Board is full (and we know it's valid due to early pruning)
        if row is None:
            return True
            
        N = len(board)
        for value in range(1, N + 1):
            # Early pruning: check constraints BEFORE assigning
            if is_valid(board, row, col, value, constraints):
                board[row][col] = value
                
                if self.record_steps:
                    self.steps.append({
                        "step": self.stats.expansions,
                        "board": [r[:] for r in board]
                    })
                
                # Recursively solve
                if self._run_algorithm(board, constraints):
                    return True
                    
                # Undo assignment if it leads to failure
                board[row][col] = 0
                
        return False
