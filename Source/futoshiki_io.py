def parse_line(line):
    """
    Chuyển một dòng dạng '0,2,0,0' thành list số nguyên [0, 2, 0, 0].
    """
    return [int(x.strip()) for x in line.strip().split(",")]


def read_input(path):
    """
    Đọc file input Futoshiki.

    Trả về dictionary:
    {
        "N": N,
        "grid": grid,
        "horizontal": horizontal_constraints,
        "vertical": vertical_constraints
    }
    """

    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Bỏ qua dòng trống
            if not line:
                continue

            # Bỏ qua comment nếu có
            if line.startswith("#"):
                continue

            lines.append(line)

    if len(lines) == 0:
        raise ValueError("Input file rỗng.")

    N = int(lines[0])

    expected_lines = 1 + N + N + (N - 1)
    if len(lines) != expected_lines:
        raise ValueError(
            f"File input sai số dòng. Cần {expected_lines} dòng dữ liệu, nhưng có {len(lines)} dòng."
        )

    # Đọc grid
    grid = []
    index = 1
    for _ in range(N):
        row = parse_line(lines[index])
        if len(row) != N:
            raise ValueError("Một dòng grid không đủ N phần tử.")
        grid.append(row)
        index += 1

    # Đọc ràng buộc ngang: N dòng, mỗi dòng N-1 phần tử
    horizontal = []
    for _ in range(N):
        row = parse_line(lines[index])
        if len(row) != N - 1:
            raise ValueError("Một dòng horizontal constraints không đủ N-1 phần tử.")
        horizontal.append(row)
        index += 1

    # Đọc ràng buộc dọc: N-1 dòng, mỗi dòng N phần tử
    vertical = []
    for _ in range(N - 1):
        row = parse_line(lines[index])
        if len(row) != N:
            raise ValueError("Một dòng vertical constraints không đủ N phần tử.")
        vertical.append(row)
        index += 1

    return {
        "N": N,
        "grid": grid,
        "horizontal": horizontal,
        "vertical": vertical
    }


def print_puzzle(puzzle):
    """
    In nhanh puzzle ra màn hình để kiểm tra.
    """
    N = puzzle["N"]
    grid = puzzle["grid"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]

    print("N =", N)
    print("Grid:")
    for row in grid:
        print(row)

    print("Horizontal constraints:")
    for row in horizontal:
        print(row)

    print("Vertical constraints:")
    for row in vertical:
        print(row)
def validate_puzzle(puzzle):
    """
    Kiểm tra puzzle có đúng format không.
    """
    N = puzzle["N"]
    grid = puzzle["grid"]
    horizontal = puzzle["horizontal"]
    vertical = puzzle["vertical"]

    if len(grid) != N:
        raise ValueError("Grid phải có đúng N dòng.")

    for row in grid:
        if len(row) != N:
            raise ValueError("Mỗi dòng grid phải có đúng N phần tử.")

        for value in row:
            if value < 0 or value > N:
                raise ValueError("Giá trị trong grid phải nằm trong khoảng 0..N.")

    if len(horizontal) != N:
        raise ValueError("Horizontal constraints phải có đúng N dòng.")

    for row in horizontal:
        if len(row) != N - 1:
            raise ValueError("Mỗi dòng horizontal phải có đúng N-1 phần tử.")

        for value in row:
            if value not in [-1, 0, 1]:
                raise ValueError("Horizontal chỉ được chứa -1, 0, 1.")

    if len(vertical) != N - 1:
        raise ValueError("Vertical constraints phải có đúng N-1 dòng.")

    for row in vertical:
        if len(row) != N:
            raise ValueError("Mỗi dòng vertical phải có đúng N phần tử.")

        for value in row:
            if value not in [-1, 0, 1]:
                raise ValueError("Vertical chỉ được chứa -1, 0, 1.")

    return True