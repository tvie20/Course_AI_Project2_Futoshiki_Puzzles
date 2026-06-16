def forward_chaining(kb):
    """
    Thuật toán Forward Chaining (Lan truyền ràng buộc) cho Futoshiki.
    Input: kb (Knowledge Base sinh từ kb_generator.py)
    Output: (is_solved, result_domains)
        - is_solved: True nếu bảng đã được giải hoàn toàn, False nếu bế tắc/mâu thuẫn.
        - result_domains: Dict chứa domain cuối cùng của các ô.
    """
    N = kb["N"]
    # Khởi tạo bản sao của domains để không làm hỏng KB gốc
    domains = {cell: set(vals) for cell, vals in kb["domains"].items()}
    
    # 1. Áp dụng các luật Given (Điền giá trị cho các ô đã biết)
    for constraint in kb["given_constraints"]:
        _, cell, val = constraint
        domains[cell] = {val}

    changed = True
    while changed:
        changed = False
        
        # Kiểm tra mâu thuẫn: Có ô nào bị rỗng tập giá trị không?
        if any(len(d) == 0 for d in domains.values()):
            return False, domains

        # 2. Luật duy nhất trên Hàng và Cột (All-Different)
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                cell = (i, j)
                if len(domains[cell]) == 1:
                    val = list(domains[cell])[0]
                    
                    # Rút gọn trên cùng hàng
                    for c in range(1, N + 1):
                        if c != j and val in domains[(i, c)]:
                            domains[(i, c)].remove(val)
                            changed = True
                            
                    # Rút gọn trên cùng cột
                    for r in range(1, N + 1):
                        if r != i and val in domains[(r, j)]:
                            domains[(r, j)].remove(val)
                            changed = True

        # 3. Luật Bất đẳng thức (Inequality Constraints)
        for constraint in kb["inequality_constraints"]:
            ctype, cell_A, cell_B = constraint
            dom_A = domains[cell_A]
            dom_B = domains[cell_B]
            
            if not dom_A or not dom_B:
                return False, domains

            if ctype == "less":  # cell_A < cell_B
                # A phải nhỏ hơn GTLN của B
                max_B = max(dom_B)
                to_remove_A = {x for x in dom_A if x >= max_B}
                if to_remove_A:
                    domains[cell_A] = dom_A - to_remove_A
                    changed = True
                
                # B phải lớn hơn GTNN của A
                min_A = min(dom_A)
                to_remove_B = {x for x in dom_B if x <= min_A}
                if to_remove_B:
                    domains[cell_B] = dom_B - to_remove_B
                    changed = True

            elif ctype == "greater":  # cell_A > cell_B
                # A phải lớn hơn GTNN của B
                min_B = min(dom_B)
                to_remove_A = {x for x in dom_A if x <= min_B}
                if to_remove_A:
                    domains[cell_A] = dom_A - to_remove_A
                    changed = True
                
                # B phải nhỏ hơn GTLN của A
                max_A = max(dom_A)
                to_remove_B = {x for x in dom_B if x >= max_A}
                if to_remove_B:
                    domains[cell_B] = dom_B - to_remove_B
                    changed = True

    # Kiểm tra xem tất cả các ô đã chỉ còn 1 giá trị duy nhất chưa
    is_solved = all(len(d) == 1 for d in domains.values())
    return is_solved, domains

def is_consistent(assignment, cell, val, N, inequality_constraints):
    """
    Hàm kiểm tra tính hợp lệ của một phép gán (SLD Resolution check).
    """
    i, j = cell
    
    # Kiểm tra đụng độ trên hàng
    for c in range(1, N + 1):
        if (i, c) in assignment and assignment[(i, c)] == val:
            return False
            
    # Kiểm tra đụng độ trên cột
    for r in range(1, N + 1):
        if (r, j) in assignment and assignment[(r, j)] == val:
            return False

    # Kiểm tra ràng buộc bất đẳng thức
    for constraint in inequality_constraints:
        ctype, cell_A, cell_B = constraint
        
        # Nếu cả 2 ô đều đã được gán giá trị
        if cell_A in assignment and cell_B in assignment:
            if ctype == "less" and not (assignment[cell_A] < assignment[cell_B]):
                return False
            if ctype == "greater" and not (assignment[cell_A] > assignment[cell_B]):
                return False
                
        # Nếu đang gán giá trị cho 1 trong 2 ô
        elif cell == cell_A and cell_B in assignment:
            if ctype == "less" and not (val < assignment[cell_B]): return False
            if ctype == "greater" and not (val > assignment[cell_B]): return False
        elif cell == cell_B and cell_A in assignment:
            if ctype == "less" and not (assignment[cell_A] < val): return False
            if ctype == "greater" and not (assignment[cell_A] > val): return False

    return True

def backward_chaining(kb):
    """
    Thuật toán Backward Chaining bằng Backtracking.
    Input: kb (Knowledge Base)
    Output: (is_solved, assignment)
    """
    N = kb["N"]
    inequality_constraints = kb["inequality_constraints"]
    
    # 1. Khởi tạo trạng thái ban đầu từ luật Given
    assignment = {}
    for constraint in kb["given_constraints"]:
        _, cell, val = constraint
        assignment[cell] = val

    # Lập danh sách các ô còn trống cần chứng minh
    unassigned_cells = []
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if (i, j) not in assignment:
                unassigned_cells.append((i, j))

    # 2. Khối đệ quy suy diễn lùi
    def backtrack(index):
        # Base case: Đã chứng minh và điền xong toàn bộ bảng
        if index == len(unassigned_cells):
            return True
            
        cell = unassigned_cells[index]
        
        # Thay vì thử từ 1->N, chỉ thử các giá trị trong domain hợp lệ 
        # (Nếu kết hợp với FC, KB["domains"] lúc này sẽ cực kỳ nhỏ)
        for val in kb["domains"][cell]:
            if is_consistent(assignment, cell, val, N, inequality_constraints):
                assignment[cell] = val  # Giả định giá trị
                
                if backtrack(index + 1): # Lùi lại chứng minh ô tiếp theo
                    return True
                    
                del assignment[cell]    # Quay lui (Backtrack) nếu sai hướng
                
        return False # Bế tắc

    # 3. Kích hoạt truy vấn
    if backtrack(0):
        return True, assignment
    return False, {}

def print_solution(puzzle, result_dict, file_object=None):
    """
    In lưới kết quả N x N kèm theo đầy đủ các dấu bất đẳng thức ra màn hình hoặc ghi vào file.
    - puzzle: Dict chứa dữ liệu gốc của test case (để lấy thông tin ràng buộc)
    - result_dict: Dict chứa kết quả sau khi giải (domains hoặc assignment)
    - file_object: Nếu truyền vào một file đã mở, kết quả sẽ được ghi vào file đó thay vì console.
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]
    
    # Chuyển đổi dữ liệu kết quả về dạng ma trận số nguyên đơn thuần
    grid_vals = [[0 for _ in range(N)] for _ in range(N)]
    for (i, j), val in result_dict.items():
        if isinstance(val, set):
            grid_vals[i-1][j-1] = list(val)[0] if len(val) == 1 else 0
        elif isinstance(val, int):
            grid_vals[i-1][j-1] = val

    # Hàm bổ trợ để xuất chuỗi ra đúng đích (file hoặc console)
    def output_line(text):
        if file_object:
            file_object.write(text + "\n")
        else:
            print(text)

    # Tiến hành dựng và in từng hàng
    for r in range(N):
        # 1. Dựng hàng chứa các ô số và ràng buộc ngang
        cell_line = ""
        for c in range(N):
            val_str = str(grid_vals[r][c]) if grid_vals[r][c] != 0 else "?"
            cell_line += val_str
            
            # Nếu chưa phải ô cuối cùng của hàng, xét ràng buộc ngang tiếp theo
            if c < N - 1:
                sign = horizontal[r][c]
                if sign == 1:
                    cell_line += " < "
                elif sign == -1:
                    cell_line += " > "
                else:
                    cell_line += "   " # Khoảng trắng căn lề
        output_line(cell_line)
        
        # 2. Dựng hàng chứa các ràng buộc dọc nằm xen kẽ (nếu chưa tới hàng cuối)
        if r < N - 1:
            vert_line = ""
            for c in range(N):
                sign = vertical[r][c]
                if sign == 1:
                    vert_line += "^"
                elif sign == -1:
                    vert_line += "v"
                else:
                    vert_line += " "
                
                # Thêm khoảng trắng bù vào vị trí tương ứng với ràng buộc ngang phía trên
                if c < N - 1:
                    vert_line += "   "
            output_line(vert_line)