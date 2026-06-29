import heapq
import sys
import os

# Add the test directory directly to sys.path to avoid clash with stdlib 'test'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test'))
from test_utils import BaseSolver, SearchLimitExceeded
from algo.solver_utils import find_first_empty_cell, is_valid

def heuristic_1_unassigned(board):
    # Đơn giản nhất: Đếm số lượng ô còn đang nhận giá trị 0. Ít ô trống nghĩa là gần đích hơn.
    count = 0
    for row in board:
        for val in row:
            if val == 0:
                count += 1
    return count

def heuristic_2_chains(board, constraints):
    # Đếm số lượng ô trống đang tham gia trực tiếp vào các ràng buộc bất đẳng thức (<, >).
    # Giúp A* ưu tiên xử lý các khu vực có ràng buộc chặt chẽ trước.
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
    # Giả lập chạy một vòng AC3 (thuật toán loại bỏ các giá trị mâu thuẫn) trên bảng hiện tại.
    domains = get_initial_domains(board)
    apply_ac3_propagation(board, domains, constraints, stats)
    
    unassigned_count = 0
    for r in range(len(board)):
        for c in range(len(board)):
            if len(domains[r][c]) == 0:
                return float('inf') # Nếu có ô bị rỗng miền -> Trạng thái chết (Dead end)
            elif len(domains[r][c]) > 1:
                unassigned_count += 1 # Đếm số ô chưa chắc chắn
                
    return unassigned_count

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

def find_mrv_degree_cell(board, constraints):
    # Hàm chọn ô trống ưu tiên theo chiến lược MRV (Minimum Remaining Values)
    # Kết hợp với Degree heuristic (chọn ô có nhiều ràng buộc với các ô trống khác nhất).
    # Giúp hạn chế đẻ ra nhiều nhánh con và phát hiện bế tắc sớm.
    N = len(board)
    best_cell = (None, None)
    min_mrv = float('inf')  # mrv: số lượng giá trị hợp lệ có thể điền (càng ít càng tốt)
    max_degree = -1         # degree: số lượng ràng buộc với ô rỗng khác (càng nhiều càng tốt)
    
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                mrv = 0
                for v in range(1, N + 1):
                    if is_valid(board, r, c, v, constraints):
                        mrv += 1
                
                degree = 0
                for i in range(N):
                    if i != c and board[r][i] == 0: degree += 1
                    if i != r and board[i][c] == 0: degree += 1
                for const in constraints:
                    r1, c1, op, r2, c2 = const
                    if (r1, c1) == (r, c) and board[r2][c2] == 0: degree += 1
                    if (r2, c2) == (r, c) and board[r1][c1] == 0: degree += 1
                
                if mrv < min_mrv:
                    min_mrv = mrv
                    max_degree = degree
                    best_cell = (r, c)
                elif mrv == min_mrv:
                    if degree > max_degree:
                        max_degree = degree
                        best_cell = (r, c)
                        
    return best_cell
class AStarSolver(BaseSolver):
    """
    Thuật toán tìm kiếm A* (A-Star Search).
    Luôn mở rộng trạng thái tốt nhất dựa trên hàm đánh giá f(n) = g(n) + h(n).
    - g(n): Số ô đã điền (độ sâu của cây tìm kiếm).
    - h(n): Hàm heuristic (h1, h2, h3) đánh giá số bước còn lại.
    Dùng Priority Queue để luôn pop ra trạng thái có f(n) nhỏ nhất.
    """
    def __init__(self, time_limit=60.0, max_expansions=1000000, max_inferences=1000000, heuristic_choice='h1', record_steps=False):
        super().__init__(time_limit, max_expansions, max_inferences)
        self.heuristic_choice = heuristic_choice
        self.record_steps = record_steps
        self.steps = []  # populated when record_steps=True

    def _run_algorithm(self, initial_board, constraints):
        priority_queue = []
        node_id_counter = 0
        self.steps = []  # reset on each run
        
        h_start = calculate_heuristic(initial_board, constraints, self.heuristic_choice, self.stats)
        if h_start == float('inf'):
            return False
            
        # Cho trạng thái ban đầu vào Priority Queue. (f, -g, id, board)
        heapq.heappush(priority_queue, (h_start, 0, node_id_counter, initial_board))
        
        while priority_queue:
            self.stats.check_limits()
            
            # Bốc trạng thái có điểm f (f_score) nhỏ nhất ra khỏi hàng đợi
            f, neg_g, _, current_board = heapq.heappop(priority_queue)
            g = -neg_g
            self.stats.expansions += 1
            
            # Tìm ô trống có MRV nhỏ nhất (ít lựa chọn nhất) để duyệt tiếp
            row, col = find_mrv_degree_cell(current_board, constraints)
            
            # Base Case: Board is full (Bảng đã kín, mục tiêu đạt được)
            if row is None:
                if self.record_steps:
                    self.steps.append({
                        "step": self.stats.expansions,
                        "cell": "Done",
                        "g": g,
                        "h": 0,
                        "f": f,
                        "board": [r[:] for r in current_board],
                    })
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
            
            # Generate successors (Sinh các trạng thái con)
            for value in range(1, N + 1):
                if is_valid(current_board, row, col, value, constraints):
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = value
                    
                    new_g = g + 1
                    new_h = calculate_heuristic(new_board, constraints, self.heuristic_choice, self.stats)
                    
                    # Nếu heuristic không báo Dead end (khác vô cực)
                    if new_h != float('inf'):
                        new_f = new_g + new_h
                        node_id_counter += 1
                        # Đẩy trạng thái con mới vào hàng đợi ưu tiên
                        heapq.heappush(priority_queue, (new_f, -new_g, node_id_counter, new_board))
                        
        return False
