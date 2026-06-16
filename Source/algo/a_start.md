
### 1. Heuristic 1: Remaining Unassigned Cells ($h_1$)

This is the most straightforward heuristic. It simply scans the board and counts how many cells still need a number. Because you must eventually fill every empty cell to reach the goal, this count is perfectly admissible (it never overestimates the cost to the goal).

```python
function heuristic_1_unassigned(board):
    count = 0
    N = length(board)
    
    for row from 0 to N - 1:
        for col from 0 to N - 1:
            if board[row][col] == 0:
                count = count + 1
                
    return count

```

---

### 2. Heuristic 2: Unfulfilled Inequality Chains ($h_2$)

This heuristic focuses specifically on the "hardest" parts of the board: the cells tied together by `<` or `>` signs. If an inequality constraint involves empty cells, those cells *must* be assigned to satisfy the board. By counting the unique empty cells involved in these constraints, we get an admissible lower bound of the moves required just to satisfy the inequality rules.

```python
function heuristic_2_chains(board, constraints):
    involved_empty_cells = Set()
    
    # Check every inequality constraint (< or >)
    for constraint in constraints:
        r1, c1, op, r2, c2 = constraint
        
        # If the left cell of the constraint is empty, it needs an assignment
        if board[r1][c1] == 0:
            involved_empty_cells.add((r1, c1))
            
        # If the right cell of the constraint is empty, it needs an assignment
        if board[r2][c2] == 0:
            involved_empty_cells.add((r2, c2))
            
    # The number of unique empty cells currently trapped in constraints
    return length(involved_empty_cells)

```

*Note: In a pure A* implementation, to ensure the heuristic remains as strong as possible, you will often use $h(s) = \max(h_1(s), h_2(s))$ because $h_1$ might be higher if there are many unassigned cells that don't have inequality constraints.*

---

### 3. Heuristic 3: AC-3 Informed Lower Bound ($h_3$)

This is the most powerful heuristic. It runs the Arc-Consistency 3 (AC-3) algorithm in the background to simulate the "domino effect" of the current board state. If AC-3 determines that any empty cell is left with zero valid options (an empty domain), the heuristic immediately flags the state as a dead end by returning infinity.

```python
function heuristic_3_ac3(board, current_domains, constraints):
    # 1. Clone domains so we don't accidentally modify the actual game state
    simulated_domains = deep_copy(current_domains)
    
    # 2. Run constraint propagation (AC-3)
    # This function narrows down the simulated_domains based on board rules
    apply_ac3_propagation(board, simulated_domains, constraints)
    
    # 3. Check for infeasibility (Dead Ends)
    N = length(board)
    for row from 0 to N - 1:
        for col from 0 to N - 1:
            if board[row][col] == 0:
                # If a cell has no valid numbers left to pick from
                if length(simulated_domains[row][col]) == 0:
                    return INFINITY  # Prune this branch immediately
                    
    # 4. If the board is feasible, return a base admissible cost
    # (Since it survived AC-3, we fall back to the basic empty cell count)
    return heuristic_1_unassigned(board)

```

