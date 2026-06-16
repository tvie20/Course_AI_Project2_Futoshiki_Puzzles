from algo.solver_utils import find_first_empty_cell, is_valid

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

def brute_force_solve(board, constraints):
    """
    Naive grid-based brute force algorithm.
    """
    row, col = find_first_empty_cell(board)
    
    # Base case: Board is full
    if row is None:
        return is_board_valid(board, constraints)
        
    N = len(board)
    for value in range(1, N + 1):
        board[row][col] = value
        
        # Recursively solve without prior checking
        if brute_force_solve(board, constraints):
            return True
            
        # Undo assignment if it leads to failure
        board[row][col] = 0
        
    return False
