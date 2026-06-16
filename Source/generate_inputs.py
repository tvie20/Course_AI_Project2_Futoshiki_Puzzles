import os


def latin_square(N):
    """
    Tạo lời giải Latin square N x N.
    """
    return [[((i + j) % N) + 1 for j in range(N)] for i in range(N)]


def make_puzzle_from_solution(solution, clue_positions):
    """
    Từ lời giải đầy đủ, giữ lại một số ô clue, còn lại đổi thành 0.
    clue_positions dùng index bắt đầu từ 0.
    """
    N = len(solution)
    grid = [[0 for _ in range(N)] for _ in range(N)]

    for i, j in clue_positions:
        grid[i][j] = solution[i][j]

    return grid


def make_constraints(solution, horizontal_positions, vertical_positions):
    """
    Tạo constraints dựa trên lời giải có sẵn.
    Nếu left < right thì ghi 1.
    Nếu left > right thì ghi -1.
    Nếu không chọn constraint thì ghi 0.
    """
    N = len(solution)

    horizontal = [[0 for _ in range(N - 1)] for _ in range(N)]
    vertical = [[0 for _ in range(N)] for _ in range(N - 1)]

    for i, j in horizontal_positions:
        left = solution[i][j]
        right = solution[i][j + 1]

        if left < right:
            horizontal[i][j] = 1
        elif left > right:
            horizontal[i][j] = -1

    for i, j in vertical_positions:
        top = solution[i][j]
        bottom = solution[i + 1][j]

        if top < bottom:
            vertical[i][j] = 1
        elif top > bottom:
            vertical[i][j] = -1

    return horizontal, vertical


def write_input(path, grid, horizontal, vertical):
    """
    Ghi file input theo format đề bài.
    """
    N = len(grid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(N) + "\n")

        for row in grid:
            f.write(",".join(map(str, row)) + "\n")

        for row in horizontal:
            f.write(",".join(map(str, row)) + "\n")

        for row in vertical:
            f.write(",".join(map(str, row)) + "\n")


def generate_case(case_id, N, clue_positions, horizontal_positions, vertical_positions):
    solution = latin_square(N)
    grid = make_puzzle_from_solution(solution, clue_positions)
    horizontal, vertical = make_constraints(
        solution,
        horizontal_positions,
        vertical_positions
    )

    os.makedirs("Inputs", exist_ok=True)

    path = f"Inputs/input-{case_id:02d}.txt"
    write_input(path, grid, horizontal, vertical)

    print("Generated", path)


def main():
    # Case 01: 4x4
    generate_case(
        1,
        4,
        clue_positions=[
            (0, 1), (1, 3), (2, 0), (3, 2)
        ],
        horizontal_positions=[
            (0, 0), (0, 2), (2, 1), (3, 0)
        ],
        vertical_positions=[
            (0, 1), (1, 2), (2, 0)
        ]
    )

    # Case 02: 4x4
    generate_case(
        2,
        4,
        clue_positions=[
            (0, 0), (1, 2), (2, 3), (3, 1)
        ],
        horizontal_positions=[
            (0, 1), (1, 0), (2, 2), (3, 1)
        ],
        vertical_positions=[
            (0, 0), (1, 3), (2, 2)
        ]
    )

    # Case 03: 5x5
    generate_case(
        3,
        5,
        clue_positions=[
            (0, 0), (0, 3), (1, 1), (2, 4), (3, 2), (4, 0)
        ],
        horizontal_positions=[
            (0, 0), (0, 2), (1, 3), (2, 1), (3, 0), (4, 2)
        ],
        vertical_positions=[
            (0, 1), (1, 2), (2, 3), (3, 0), (0, 4)
        ]
    )

    # Case 04: 5x5
    generate_case(
        4,
        5,
        clue_positions=[
            (0, 2), (1, 4), (2, 1), (3, 3), (4, 0), (4, 4)
        ],
        horizontal_positions=[
            (0, 1), (1, 2), (2, 0), (2, 3), (3, 1), (4, 2)
        ],
        vertical_positions=[
            (0, 0), (0, 3), (1, 1), (2, 4), (3, 2)
        ]
    )

    # Case 05: 6x6
    generate_case(
        5,
        6,
        clue_positions=[
            (0, 0), (0, 4), (1, 2), (2, 5),
            (3, 1), (4, 3), (5, 0), (5, 5)
        ],
        horizontal_positions=[
            (0, 0), (0, 3), (1, 1), (2, 4),
            (3, 2), (4, 0), (5, 3)
        ],
        vertical_positions=[
            (0, 2), (1, 4), (2, 1), (3, 3),
            (4, 0), (0, 5)
        ]
    )

    # Case 06: 6x6
    generate_case(
        6,
        6,
        clue_positions=[
            (0, 1), (1, 3), (2, 0), (2, 5),
            (3, 2), (4, 4), (5, 1), (5, 5)
        ],
        horizontal_positions=[
            (0, 2), (1, 0), (1, 4), (2, 3),
            (3, 1), (4, 2), (5, 0)
        ],
        vertical_positions=[
            (0, 0), (1, 2), (2, 4), (3, 1),
            (4, 3), (0, 5)
        ]
    )

    # Case 07: 7x7
    generate_case(
        7,
        7,
        clue_positions=[
            (0, 0), (0, 5), (1, 2), (2, 6),
            (3, 3), (4, 1), (5, 4), (6, 0), (6, 6)
        ],
        horizontal_positions=[
            (0, 0), (0, 4), (1, 1), (2, 5),
            (3, 2), (4, 0), (5, 3), (6, 1)
        ],
        vertical_positions=[
            (0, 2), (1, 4), (2, 6), (3, 1),
            (4, 3), (5, 0), (0, 5)
        ]
    )

    # Case 08: 7x7
    generate_case(
        8,
        7,
        clue_positions=[
            (0, 3), (1, 0), (1, 5), (2, 2),
            (3, 6), (4, 1), (5, 4), (6, 0), (6, 5)
        ],
        horizontal_positions=[
            (0, 1), (1, 4), (2, 0), (2, 5),
            (3, 3), (4, 2), (5, 1), (6, 4)
        ],
        vertical_positions=[
            (0, 3), (1, 0), (2, 2), (3, 5),
            (4, 1), (5, 4), (0, 6)
        ]
    )

    # Case 09: 9x9
    generate_case(
        9,
        9,
        clue_positions=[
            (0, 0), (0, 4), (0, 8),
            (1, 2), (1, 6),
            (2, 1), (2, 5),
            (3, 3), (3, 7),
            (4, 0), (4, 4), (4, 8),
            (5, 1), (5, 5),
            (6, 2), (6, 6),
            (7, 3), (7, 7),
            (8, 0), (8, 4), (8, 8)
        ],
        horizontal_positions=[
            (0, 0), (0, 3), (0, 7),
            (1, 1), (1, 5),
            (2, 0), (2, 4),
            (3, 2), (3, 6),
            (4, 1), (4, 5),
            (5, 0), (5, 4),
            (6, 3), (6, 7),
            (7, 2), (7, 6),
            (8, 1), (8, 5)
        ],
        vertical_positions=[
            (0, 0), (0, 4), (0, 8),
            (1, 2), (1, 6),
            (2, 1), (2, 5),
            (3, 3), (3, 7),
            (4, 0), (4, 4),
            (5, 2), (5, 6),
            (6, 1), (6, 5),
            (7, 3), (7, 7)
        ]
    )

    # Case 10: 9x9
    generate_case(
        10,
        9,
        clue_positions=[
            (0, 2), (0, 6),
            (1, 0), (1, 4), (1, 8),
            (2, 3), (2, 7),
            (3, 1), (3, 5),
            (4, 0), (4, 4), (4, 8),
            (5, 2), (5, 6),
            (6, 1), (6, 5),
            (7, 0), (7, 4), (7, 8),
            (8, 2), (8, 6)
        ],
        horizontal_positions=[
            (0, 1), (0, 5),
            (1, 0), (1, 4), (1, 7),
            (2, 2), (2, 6),
            (3, 1), (3, 5),
            (4, 0), (4, 4), (4, 7),
            (5, 2), (5, 6),
            (6, 1), (6, 5),
            (7, 0), (7, 4), (7, 7),
            (8, 2), (8, 6)
        ],
        vertical_positions=[
            (0, 2), (0, 6),
            (1, 0), (1, 4), (1, 8),
            (2, 3), (2, 7),
            (3, 1), (3, 5),
            (4, 0), (4, 4), (4, 8),
            (5, 2), (5, 6),
            (6, 1), (6, 5),
            (7, 0), (7, 4), (7, 8)
        ]
    )


if __name__ == "__main__":
    main()