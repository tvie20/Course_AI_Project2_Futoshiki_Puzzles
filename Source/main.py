import argparse
import os
import time
import sys

# Add current directory to path if needed for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from futoshiki_io import read_input
from algo.solver_utils import parse_and_convert, format_grid
from algo.brute_force import brute_force_solve
from algo.backtracking import backtrack_solve
from algo.A_star import a_star_solve

def main():
    parser = argparse.ArgumentParser(description="Futoshiki Grid Solver CLI")
    parser.add_argument("algorithm", choices=['brute_force', 'backtracking', 'a_star'], help="Solver algorithm to use")
    parser.add_argument("input_file", help="Path to the input file (e.g. Inputs/input-01.txt)")
    parser.add_argument("--heuristic", choices=['h1', 'h2', 'h3'], default='h1', help="Heuristic function for A* (default: h1)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        return
        
    print(f"Processing file: {args.input_file}")
    print(f"Algorithm: {args.algorithm}")
    print("-" * 30)
    
    # Đọc puzzle từ file txt
    puzzle = read_input(args.input_file)
    
    # Convert constraints into list of tuples
    constraints = parse_and_convert(puzzle)
    
    # Copy grid so we can modify it directly
    board = [row[:] for row in puzzle["grid"]]
    
    # Đo thời gian & chạy thuật toán
    start_time = time.time()
    
    if args.algorithm == 'brute_force':
        success = brute_force_solve(board, constraints)
    elif args.algorithm == 'backtracking':
        success = backtrack_solve(board, constraints)
    elif args.algorithm == 'a_star':
        success = a_star_solve(board, constraints, heuristic_choice=args.heuristic)
        
    end_time = time.time()
    exec_time = end_time - start_time
    
    print(f"Execution time: {exec_time:.4f} seconds")
    print("-" * 30)
    
    if success:
        output_str = format_grid(puzzle, board)
        print("Resulting Grid:")
        print(output_str)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
