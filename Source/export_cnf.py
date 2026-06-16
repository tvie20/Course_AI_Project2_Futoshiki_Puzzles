from futoshiki_io import read_input, validate_puzzle
from kb_generator import write_dimacs_cnf


def main():
    for index in range(1, 11):
        input_path = f"Inputs/input-{index:02d}.txt"
        output_path = f"CNF/input-{index:02d}.cnf"

        puzzle = read_input(input_path)
        validate_puzzle(puzzle)

        write_dimacs_cnf(puzzle, output_path)

        print(f"Exported {output_path}")


if __name__ == "__main__":
    main()