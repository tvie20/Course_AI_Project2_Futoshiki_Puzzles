from algo.solver_utils import find_first_empty_cell, is_valid

def backtrack_solve(board, constraints):
    """
    Grid-based backtracking algorithm with early pruning.
    """
    row, col = find_first_empty_cell(board)
    
    # Base case: Board is full (and we know it's valid due to early pruning)
    if row is None:
        return True
        
    N = len(board)
    for value in range(1, N + 1):
        # Early pruning: check constraints BEFORE assigning
        if is_valid(board, row, col, value, constraints):
            board[row][col] = value
            
            # Recursively solve
            if backtrack_solve(board, constraints):
                return True
                
            # Undo assignment if it leads to failure
            board[row][col] = 0
            
    return False
