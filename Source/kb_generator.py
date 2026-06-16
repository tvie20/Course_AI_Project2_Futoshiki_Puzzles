def generate_less_facts(N):
    """
    Sinh facts Less(v1, v2) cho mọi v1 < v2.
    Ví dụ N = 4:
    Less(1,2), Less(1,3), Less(1,4), Less(2,3), ...
    """
    facts = []

    for v1 in range(1, N + 1):
        for v2 in range(1, N + 1):
            if v1 < v2:
                facts.append(("Less", v1, v2))

    return facts


def generate_given_facts(puzzle):
    """
    Sinh Given(i, j, v) từ các ô đã cho sẵn.
    Dùng index bắt đầu từ 1 theo đề bài.
    """
    N = puzzle["N"]
    grid = puzzle["grid"]

    facts = []

    for i in range(N):
        for j in range(N):
            value = grid[i][j]
            if value != 0:
                facts.append(("Given", i + 1, j + 1, value))

    return facts


def generate_horizontal_facts(puzzle):
    """
    Sinh LessH(i,j) hoặc GreaterH(i,j).
    horizontal[i][j] là ràng buộc giữa ô (i,j) và (i,j+1).
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]

    facts = []

    for i in range(N):
        for j in range(N - 1):
            sign = horizontal[i][j]

            if sign == 1:
                facts.append(("LessH", i + 1, j + 1))
            elif sign == -1:
                facts.append(("GreaterH", i + 1, j + 1))

    return facts


def generate_vertical_facts(puzzle):
    """
    Sinh LessV(i,j) hoặc GreaterV(i,j).
    vertical[i][j] là ràng buộc giữa ô (i,j) và (i+1,j).
    """
    N = puzzle["N"]
    vertical = puzzle["vertical"]

    facts = []

    for i in range(N - 1):
        for j in range(N):
            sign = vertical[i][j]

            if sign == 1:
                facts.append(("LessV", i + 1, j + 1))
            elif sign == -1:
                facts.append(("GreaterV", i + 1, j + 1))

    return facts


def generate_facts(puzzle):
    """
    Sinh toàn bộ facts ban đầu từ puzzle.
    """
    N = puzzle["N"]

    facts = []

    facts.extend(generate_less_facts(N))
    facts.extend(generate_given_facts(puzzle))
    facts.extend(generate_horizontal_facts(puzzle))
    facts.extend(generate_vertical_facts(puzzle))

    return facts
def generate_domains(N):
    """
    Mỗi ô ban đầu có domain là {1, 2, ..., N}.
    """
    domains = {}

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            domains[(i, j)] = set(range(1, N + 1))

    return domains


def generate_row_constraints(N):
    """
    Mỗi hàng là all-different.
    """
    constraints = []

    for i in range(1, N + 1):
        constraints.append(("row_all_diff", i))

    return constraints


def generate_column_constraints(N):
    """
    Mỗi cột là all-different.
    """
    constraints = []

    for j in range(1, N + 1):
        constraints.append(("col_all_diff", j))

    return constraints


def generate_inequality_constraints(puzzle):
    """
    Sinh constraint dạng dễ dùng cho solver:
    ("less", (i1,j1), (i2,j2))
    nghĩa là cell1 < cell2.
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]

    constraints = []

    # Ràng buộc ngang
    for i in range(N):
        for j in range(N - 1):
            sign = horizontal[i][j]

            left_cell = (i + 1, j + 1)
            right_cell = (i + 1, j + 2)

            if sign == 1:
                constraints.append(("less", left_cell, right_cell))
            elif sign == -1:
                constraints.append(("greater", left_cell, right_cell))

    # Ràng buộc dọc
    for i in range(N - 1):
        for j in range(N):
            sign = vertical[i][j]

            top_cell = (i + 1, j + 1)
            bottom_cell = (i + 2, j + 1)

            if sign == 1:
                constraints.append(("less", top_cell, bottom_cell))
            elif sign == -1:
                constraints.append(("greater", top_cell, bottom_cell))

    return constraints


def generate_given_constraints(puzzle):
    """
    Sinh constraint cho các ô đã cho sẵn.
    """
    N = puzzle["N"]
    grid = puzzle["grid"]

    constraints = []

    for i in range(N):
        for j in range(N):
            value = grid[i][j]
            if value != 0:
                constraints.append(("given", (i + 1, j + 1), value))

    return constraints


def generate_ground_kb(puzzle):
    """
    Sinh KB dạng structured data.
    """
    N = puzzle["N"]

    kb = {
        "N": N,
        "domains": generate_domains(N),
        "row_constraints": generate_row_constraints(N),
        "column_constraints": generate_column_constraints(N),
        "inequality_constraints": generate_inequality_constraints(puzzle),
        "given_constraints": generate_given_constraints(puzzle),
        "facts": generate_facts(puzzle),
        "cnf": generate_cnf(puzzle)
    }

    return kb
def var_id(i, j, v, N):
    """
    Mã hóa Val(i,j,v) thành một số nguyên duy nhất.
    i, j, v bắt đầu từ 1.

    Ví dụ N = 4:
    Val(1,1,1) -> 1
    Val(1,1,2) -> 2
    ...
    """
    return (i - 1) * N * N + (j - 1) * N + v


def decode_var(var, N):
    """
    Giải mã số nguyên về lại Val(i,j,v).
    """
    var = abs(var)
    var -= 1

    i = var // (N * N) + 1
    remainder = var % (N * N)

    j = remainder // N + 1
    v = remainder % N + 1

    return i, j, v


def generate_cell_at_least_one_clauses(N):
    """
    Mỗi ô có ít nhất một giá trị:
    Val(i,j,1) OR Val(i,j,2) OR ... OR Val(i,j,N)
    """
    clauses = []

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            clause = []
            for v in range(1, N + 1):
                clause.append(var_id(i, j, v, N))
            clauses.append(clause)

    return clauses


def generate_cell_at_most_one_clauses(N):
    """
    Mỗi ô có nhiều nhất một giá trị:
    NOT Val(i,j,v1) OR NOT Val(i,j,v2)
    """
    clauses = []

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for v1 in range(1, N + 1):
                for v2 in range(v1 + 1, N + 1):
                    clauses.append([
                        -var_id(i, j, v1, N),
                        -var_id(i, j, v2, N)
                    ])

    return clauses


def generate_row_uniqueness_clauses(N):
    """
    Mỗi hàng không được có hai ô cùng giá trị.
    """
    clauses = []

    for i in range(1, N + 1):
        for v in range(1, N + 1):
            for j1 in range(1, N + 1):
                for j2 in range(j1 + 1, N + 1):
                    clauses.append([
                        -var_id(i, j1, v, N),
                        -var_id(i, j2, v, N)
                    ])

    return clauses


def generate_column_uniqueness_clauses(N):
    """
    Mỗi cột không được có hai ô cùng giá trị.
    """
    clauses = []

    for j in range(1, N + 1):
        for v in range(1, N + 1):
            for i1 in range(1, N + 1):
                for i2 in range(i1 + 1, N + 1):
                    clauses.append([
                        -var_id(i1, j, v, N),
                        -var_id(i2, j, v, N)
                    ])

    return clauses


def generate_given_clauses(puzzle):
    """
    Ô cho sẵn Given(i,j,v) thì ép Val(i,j,v) đúng.
    """
    N = puzzle["N"]
    grid = puzzle["grid"]

    clauses = []

    for i in range(N):
        for j in range(N):
            value = grid[i][j]
            if value != 0:
                clauses.append([var_id(i + 1, j + 1, value, N)])

    return clauses


def generate_inequality_clauses(puzzle):
    """
    Sinh clause cho các ràng buộc bất đẳng thức.

    Nếu A < B:
        loại mọi cặp vA >= vB
        nghĩa là: NOT Val(A,vA) OR NOT Val(B,vB)

    Nếu A > B:
        loại mọi cặp vA <= vB
    """
    N = puzzle["N"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]

    clauses = []

    # Ràng buộc ngang
    for i in range(N):
        for j in range(N - 1):
            sign = horizontal[i][j]

            cell1_i = i + 1
            cell1_j = j + 1
            cell2_i = i + 1
            cell2_j = j + 2

            if sign == 1:
                # cell1 < cell2
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 >= v2:
                            clauses.append([
                                -var_id(cell1_i, cell1_j, v1, N),
                                -var_id(cell2_i, cell2_j, v2, N)
                            ])

            elif sign == -1:
                # cell1 > cell2
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 <= v2:
                            clauses.append([
                                -var_id(cell1_i, cell1_j, v1, N),
                                -var_id(cell2_i, cell2_j, v2, N)
                            ])

    # Ràng buộc dọc
    for i in range(N - 1):
        for j in range(N):
            sign = vertical[i][j]

            cell1_i = i + 1
            cell1_j = j + 1
            cell2_i = i + 2
            cell2_j = j + 1

            if sign == 1:
                # cell1 < cell2
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 >= v2:
                            clauses.append([
                                -var_id(cell1_i, cell1_j, v1, N),
                                -var_id(cell2_i, cell2_j, v2, N)
                            ])

            elif sign == -1:
                # cell1 > cell2
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 <= v2:
                            clauses.append([
                                -var_id(cell1_i, cell1_j, v1, N),
                                -var_id(cell2_i, cell2_j, v2, N)
                            ])

    return clauses


def generate_cnf(puzzle):
    """
    Sinh toàn bộ CNF cho puzzle.

    CNF là list các clause.
    Mỗi clause là list[int].
    Số dương nghĩa là Val(i,j,v).
    Số âm nghĩa là NOT Val(i,j,v).
    """
    N = puzzle["N"]

    clauses = []

    clauses.extend(generate_cell_at_least_one_clauses(N))
    clauses.extend(generate_cell_at_most_one_clauses(N))
    clauses.extend(generate_row_uniqueness_clauses(N))
    clauses.extend(generate_column_uniqueness_clauses(N))
    clauses.extend(generate_given_clauses(puzzle))
    clauses.extend(generate_inequality_clauses(puzzle))

    return clauses
def num_variables(N):
    """
    Số biến CNF.
    Vì mỗi biến tương ứng Val(i,j,v),
    với i,j,v thuộc {1..N}, nên có N^3 biến.
    """
    return N * N * N


def write_dimacs_cnf(puzzle, output_path):
    """
    Ghi CNF ra file theo chuẩn DIMACS.

    Format:
    p cnf <number_of_variables> <number_of_clauses>
    literal literal ... 0
    literal literal ... 0
    """
    N = puzzle["N"]
    clauses = generate_cnf(puzzle)
    variables = num_variables(N)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"p cnf {variables} {len(clauses)}\n")

        for clause in clauses:
            line = " ".join(map(str, clause)) + " 0\n"
            f.write(line)

    return output_path