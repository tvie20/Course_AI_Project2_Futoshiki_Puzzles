import os

def parse_and_convert(puzzle):
    """
    Takes the puzzle dictionary and converts the horizontal and vertical 
    constraints into a single list of tuples: (row1, col1, operator, row2, col2).
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]
    
    constraints = []
    
    for i in range(N):
        for j in range(N - 1):
            if horizontal[i][j] == 1:
                # cell(i, j) < cell(i, j+1)
                constraints.append((i, j, '<', i, j+1))
            elif horizontal[i][j] == -1:
                # cell(i, j) > cell(i, j+1)
                constraints.append((i, j, '>', i, j+1))
                
    for i in range(N - 1):
        for j in range(N):
            if vertical[i][j] == 1:
                # cell(i, j) < cell(i+1, j)
                constraints.append((i, j, '<', i+1, j))
            elif vertical[i][j] == -1:
                # cell(i, j) > cell(i+1, j)
                constraints.append((i, j, '>', i+1, j))
                
    return constraints

def is_valid(board, row, col, value, constraints):
    """
    Universal constraint checker for the grid.
    """
    N = len(board)
    
    # 1. Row Check
    for c in range(N):
        if board[row][c] == value:
            return False
            
    # 2. Column Check
    for r in range(N):
        if board[r][col] == value:
            return False
            
    # 3. Inequality Check
    for constraint in constraints:
        r1, c1, op, r2, c2 = constraint
        
        if (r1, c1) == (row, col):
            neighbor_val = board[r2][c2]
            if neighbor_val != 0:
                if op == '<' and not (value < neighbor_val): return False
                if op == '>' and not (value > neighbor_val): return False
                
        if (r2, c2) == (row, col):
            neighbor_val = board[r1][c1]
            if neighbor_val != 0:
                if op == '<' and not (neighbor_val < value): return False
                if op == '>' and not (neighbor_val > value): return False
                
    return True

def find_first_empty_cell(board):
    """
    Finds the first empty cell (0) in the board.
    """
    N = len(board)
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                return r, c
    return None, None

def format_grid(puzzle, grid):
    """
    Formats the grid with inequalities as a string.
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]
    
    lines = []
    for i in range(N):
        # Format row
        row_str = ""
        for j in range(N):
            row_str += str(grid[i][j])
            if j < N - 1:
                h = horizontal[i][j]
                if h == 1:
                    row_str += " < "
                elif h == -1:
                    row_str += " > "
                else:
                    row_str += "   "
        lines.append(row_str.rstrip())
        
        # Format vertical constraints below the row
        if i < N - 1:
            vert_str = ""
            has_vert = False
            for j in range(N):
                v = vertical[i][j]
                if v == 1:
                    vert_str += "^"
                    has_vert = True
                elif v == -1:
                    vert_str += "v"
                    has_vert = True
                else:
                    vert_str += " "
                
                if j < N - 1:
                    vert_str += "   "
            if has_vert:
                lines.append(vert_str.rstrip())
                
    return "\n".join(lines)
