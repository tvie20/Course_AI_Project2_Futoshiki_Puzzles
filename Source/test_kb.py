from futoshiki_io import read_input, validate_puzzle
from kb_generator import generate_ground_kb, generate_cnf


def main():
    """
    Test toàn bộ 10 input:
    - Đọc input
    - Kiểm tra format input
    - Sinh ground KB
    - Sinh CNF
    - In số facts và số clauses
    """

    for index in range(1, 11):
        path = f"Inputs/input-{index:02d}.txt"

        puzzle = read_input(path)
        validate_puzzle(puzzle)

        kb = generate_ground_kb(puzzle)
        clauses = generate_cnf(puzzle)

        print(path)
        print("N:", puzzle["N"])
        print("Facts:", len(kb["facts"]))
        print("CNF clauses:", len(clauses))
        print("-" * 40)


if __name__ == "__main__":
    main()
