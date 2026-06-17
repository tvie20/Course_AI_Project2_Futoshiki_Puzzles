import sys
import os
import tracemalloc
import time
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from futoshiki_io import read_input
from algo.brute_force import BruteForceSolver
from algo.backtracking import BacktrackingSolver
from algo.A_star import AStarSolver
from inference import ForwardChainingSolver, BackwardChainingSolver

def format_memory(bytes_size):
    kb = bytes_size / 1024
    if kb < 1024:
        return f"{kb:.2f} KB"
    mb = kb / 1024
    return f"{mb:.2f} MB"

def run_all_tests(time_limit=180.0, max_expansions=1000000, max_inferences=1000000):
    solvers = {
        "Brute-Force": BruteForceSolver,
        "Backtracking": BacktrackingSolver,
        "A* Search (h1)": lambda **kwargs: AStarSolver(heuristic_choice='h1', **kwargs),
        "A* Search (h2)": lambda **kwargs: AStarSolver(heuristic_choice='h2', **kwargs),
        "A* Search (h3)": lambda **kwargs: AStarSolver(heuristic_choice='h3', **kwargs),
        "Forward Chaining": ForwardChainingSolver,
        "Backward Chaining": BackwardChainingSolver
    }

    # Data structures for results
    # detailed_results: list of dicts for every run
    detailed_results = []
    
    # aggregated_results: { solver_name: {"correct": 0, "time": 0.0, "heuristic_time": 0.0, "memory": 0, "expansions": 0, "inferences": 0, "count": 0} }
    aggregated_results = {name: {"correct": 0, "time": 0.0, "heuristic_time": 0.0, "memory": 0, "expansions": 0, "inferences": 0, "count": 0} for name in solvers}

    print("Starting Test Suite...")
    for i in range(1, 11):
        input_file = f"../Inputs/input-{i:02d}.txt"
        if not os.path.exists(os.path.join(os.path.dirname(__file__), input_file)):
            print(f"Skipping {input_file} - Not found")
            continue
            
        print(f"\n--- Running Test {i:02d} ---")
        
        for name, solver_class in solvers.items():
            # Fresh read to avoid mutating the same board
            board_data = read_input(os.path.join(os.path.dirname(__file__), input_file))
            board = board_data["grid"]
            
            from algo.solver_utils import parse_and_convert
            constraints = parse_and_convert(board_data)

            solver = solver_class(time_limit=time_limit, max_expansions=max_expansions, max_inferences=max_inferences)
            
            # Start memory tracking
            tracemalloc.start()
            
            try:
                result = solver.solve(board, constraints)
            except Exception as e:
                result = None
                print(f"  {name}: Exception - {e}")
                
            # Get memory tracking results
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Collect metrics
            run_time = solver.stats.get_run_time()
            memory_used = peak
            
            correctness = "Yes" if result is True else ("Limit Exceeded" if result is None else "No")
            heuristic_time = solver.stats.heuristic_time
            
            print(f"  {name}: Correct={correctness}, Time={run_time:.4f}s (H_Time: {heuristic_time:.4f}s), Mem={format_memory(memory_used)}, Exp={solver.stats.expansions}, Inf={solver.stats.inferences}")

            detailed_results.append({
                "Test": f"Input-{i:02d}",
                "Algorithm": name,
                "Correctness": correctness,
                "Run Time (s)": f"{run_time:.4f}",
                "Heuristic Time (s)": f"{heuristic_time:.4f}",
                "Memory": format_memory(memory_used),
                "Expansions": solver.stats.expansions,
                "Inferences": solver.stats.inferences
            })

            # Aggregate
            aggregated_results[name]["count"] += 1
            if result is True:
                aggregated_results[name]["correct"] += 1
            aggregated_results[name]["time"] += run_time
            aggregated_results[name]["heuristic_time"] += heuristic_time
            aggregated_results[name]["memory"] += memory_used
            aggregated_results[name]["expansions"] += solver.stats.expansions
            aggregated_results[name]["inferences"] += solver.stats.inferences

    # Generate Markdown File
    output_md = os.path.join(os.path.dirname(__file__), "test_result.md")
    with open(output_md, "w") as f:
        f.write("# Futoshiki Algorithm Test Results\n\n")
        f.write(f"Limits: {time_limit} seconds, {max_expansions} expansions, {max_inferences} inferences\n\n")
        
        f.write("## Average Results (Over 10 tests)\n\n")
        f.write("| Algorithm | Correctness | Avg Run Time (s) | Avg Heuristic Time (s) | Avg Memory | Avg Expansions | Avg Inferences |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for name, stats in aggregated_results.items():
            count = stats["count"]
            if count == 0: continue
            
            pct_correct = (stats["correct"] / count) * 100
            avg_time = stats["time"] / count
            avg_htime = stats["heuristic_time"] / count
            avg_mem = stats["memory"] / count
            avg_exp = stats["expansions"] / count
            avg_inf = stats["inferences"] / count
            
            f.write(f"| {name} | {pct_correct:.0f}% | {avg_time:.4f} | {avg_htime:.4f} | {format_memory(avg_mem)} | {avg_exp:.0f} | {avg_inf:.0f} |\n")
            
        f.write("\n## Detailed Results\n\n")
        f.write("| Test | Algorithm | Correctness | Run Time (s) | Heuristic Time (s) | Memory | Expansions | Inferences |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for res in detailed_results:
            f.write(f"| {res['Test']} | {res['Algorithm']} | {res['Correctness']} | {res['Run Time (s)']} | {res['Heuristic Time (s)']} | {res['Memory']} | {res['Expansions']} | {res['Inferences']} |\n")

    print(f"\nResults successfully written to {output_md}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Futoshiki Algorithm Tests")
    parser.add_argument("--time-limit", type=float, default=180.0, help="Time limit in seconds for each algorithm run (default: 180.0)")
    parser.add_argument("--max-expansions", type=int, default=1000000, help="Maximum number of state expansions allowed (default: 1000000)")
    parser.add_argument("--max-inferences", type=int, default=1000000, help="Maximum number of inferences allowed (default: 1000000)")
    
    args = parser.parse_args()
    
    run_all_tests(
        time_limit=args.time_limit,
        max_expansions=args.max_expansions,
        max_inferences=args.max_inferences
    )
