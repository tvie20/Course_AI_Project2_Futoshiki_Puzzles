import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from io import StringIO

from futoshiki_io import read_input, validate_puzzle
from kb_generator import generate_ground_kb, generate_cnf, write_dimacs_cnf
from inference import backward_chaining, forward_chaining, print_solution
from algo.A_star import AStarSolver
from algo.brute_force import BruteForceSolver
from algo.backtracking import BacktrackingSolver
from algo.solver_utils import parse_and_convert


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "Inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Outputs")
CNF_DIR = os.path.join(BASE_DIR, "CNF")

# Grid drawing constants
CELL_SIZE = 36
GAP_SIZE = 16
PADDING = 14

ALGO_OPTIONS = [
    "Forward Chaining",
    "Backward Chaining",
    "Brute-Force",
    "Backtracking",
    "A* (H1 - Unassigned)",
    "A* (H2 - Chains)",
    "A* (H3 - AC3)",
]


class FutoshikiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Futoshiki Project 2 - Logic Solver GUI")
        self.root.geometry("1150x820")

        self.current_puzzle = None
        self.current_file = None

        # Step visualizer state
        self.step_trace = []
        self._current_step = 0
        self._autoplay_job = None

        self.create_widgets()

    # ── Widget construction ──────────────────────────────────────────────────

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Futoshiki Puzzle - Data, KB, CNF & Solver",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=8)

        # ── Row 0: Action buttons ────────────────────────────────────────────
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=3)

        tk.Button(button_frame, text="Open Input File", width=18, command=self.open_input_file).grid(
            row=0, column=0, padx=5, pady=2
        )
        tk.Button(button_frame, text="Generate KB/CNF", width=18, command=self.generate_kb_cnf).grid(
            row=0, column=1, padx=5, pady=2
        )
        self.btn_solve = tk.Button(
            button_frame, text="Solve", width=18, command=self.solve_puzzle
        )
        self.btn_solve.grid(row=0, column=2, padx=5, pady=2)
        tk.Button(button_frame, text="Export CNF", width=18, command=self.export_cnf).grid(
            row=0, column=3, padx=5, pady=2
        )
        tk.Button(button_frame, text="Clear", width=18, command=self.clear_output).grid(
            row=0, column=4, padx=5, pady=2
        )

        # ── Row 1: Algorithm & configuration ────────────────────────────────
        tk.Label(button_frame, text="Algorithm:", font=("Arial", 10)).grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )
        self.algo_var = tk.StringVar(value="Backward Chaining")
        self.algo_combo = ttk.Combobox(
            button_frame,
            textvariable=self.algo_var,
            values=ALGO_OPTIONS,
            state="readonly",
            width=22,
        )
        self.algo_combo.grid(row=1, column=1, padx=5, pady=4, sticky="w")
        self.algo_combo.bind("<<ComboboxSelected>>", self._on_algo_changed)

        tk.Label(button_frame, text="Timeout (s):", font=("Arial", 10)).grid(
            row=1, column=2, padx=5, pady=4, sticky="e"
        )
        self.timeout_var = tk.IntVar(value=180)
        ttk.Spinbox(
            button_frame, from_=1, to=3600, textvariable=self.timeout_var, width=10
        ).grid(row=1, column=3, padx=5, pady=4, sticky="w")

        tk.Label(button_frame, text="Max Inf/Exp:", font=("Arial", 10)).grid(
            row=1, column=4, padx=5, pady=4, sticky="e"
        )
        self.max_exp_var = tk.IntVar(value=1000000)
        ttk.Spinbox(
            button_frame, from_=1, to=1000000, textvariable=self.max_exp_var, width=12
        ).grid(row=1, column=5, padx=5, pady=4, sticky="w")

        # ── Status bar ───────────────────────────────────────────────────────
        status_frame = tk.Frame(self.root, relief="sunken", bd=1)
        status_frame.pack(fill="x", padx=10, pady=(0, 3))

        self.status_label = tk.Label(
            status_frame, text="Status: Idle", font=("Arial", 10), fg="#333333", anchor="w"
        )
        self.status_label.pack(side="left", padx=12)

        tk.Label(status_frame, text="|", fg="#aaaaaa").pack(side="left")

        self.runtime_label = tk.Label(
            status_frame, text="Runtime: —", font=("Arial", 10), fg="#333333", anchor="w"
        )
        self.runtime_label.pack(side="left", padx=12)

        tk.Label(status_frame, text="|", fg="#aaaaaa").pack(side="left")

        self.expand_label = tk.Label(
            status_frame, text="Inferences/Expansions: —", font=("Arial", 10), fg="#333333", anchor="w"
        )
        self.expand_label.pack(side="left", padx=12)

        # ── File label ───────────────────────────────────────────────────────
        self.file_label = tk.Label(self.root, text="No file selected", font=("Arial", 10))
        self.file_label.pack(pady=3)

        # ── Puzzle grid canvas ───────────────────────────────────────────────
        grid_frame = tk.LabelFrame(self.root, text="Puzzle Grid", font=("Arial", 10))
        grid_frame.pack(padx=10, pady=(0, 3), fill="x")

        self.grid_canvas = tk.Canvas(
            grid_frame, height=1, bg="white", bd=0, highlightthickness=0
        )
        self.grid_canvas.pack(fill="x", padx=5, pady=5)

        # ── Step Visualizer ──────────────────────────────────────────────────
        self.step_visualizer_frame = tk.LabelFrame(self.root, text="Step Visualizer", font=("Arial", 10))
        self.step_visualizer_frame.pack(padx=10, pady=(0, 3), fill="x")

        self.step_label = tk.Label(
            self.step_visualizer_frame,
            text="No trace loaded.",
            font=("Consolas", 10),
            anchor="w",
        )
        self.step_label.pack(fill="x", padx=10, pady=4)

        slider_nav = tk.Frame(self.step_visualizer_frame)
        slider_nav.pack(fill="x", padx=10, pady=(0, 6))

        self.step_slider = ttk.Scale(
            slider_nav, from_=0, to=0, orient="horizontal", command=self._on_slider_moved
        )
        self.step_slider.pack(side="left", fill="x", expand=True, padx=(0, 8))

        tk.Button(slider_nav, text="◀ Prev", width=8, command=self._step_prev).pack(
            side="left", padx=2
        )
        tk.Button(slider_nav, text="▶ Next", width=8, command=self._step_next).pack(
            side="left", padx=2
        )
        self.autoplay_btn = tk.Button(
            slider_nav, text="▶▶ Auto", width=8, command=self._step_autoplay_toggle
        )
        self.autoplay_btn.pack(side="left", padx=2)

        # ── Text log area ────────────────────────────────────────────────────
        log_frame = tk.LabelFrame(self.root, text="Output Log", font=("Arial", 10))
        log_frame.pack(expand=True, fill="both", padx=10, pady=(0, 8))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            log_frame,
            wrap="none",
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
        )
        self.text_area.pack(expand=True, fill="both", padx=4, pady=4)
        scrollbar.config(command=self.text_area.yview)

    # ── Algorithm selector callback ──────────────────────────────────────────

    def _on_algo_changed(self, event=None):
        self._stop_autoplay()

    # ── Step visualizer helpers ──────────────────────────────────────────────

    def _load_step_trace(self, steps):
        """Populate visualizer with a new step list."""
        self.step_trace = steps
        self._current_step = 0
        self._stop_autoplay()
        if steps:
            self.step_slider.config(to=max(0, len(steps) - 1))
            self.step_slider.set(0)
            self._update_step_display(0)
        else:
            self.step_label.config(text="No steps recorded (puzzle may have been solved immediately).")

    def _update_step_display(self, idx):
        idx = int(idx)
        if not self.step_trace:
            return
        idx = max(0, min(idx, len(self.step_trace) - 1))
        self._current_step = idx
        s = self.step_trace[idx]
        
        # Extract assignment for drawing
        if "assignment" in s:
            assignment = s["assignment"]
        elif "board" in s:
            board = s["board"]
            N = len(board)
            assignment = {
                (i + 1, j + 1): board[i][j]
                for i in range(N) for j in range(N) if board[i][j] != 0
            }
        else:
            assignment = {}
            
        self.draw_grid(self.current_puzzle, solution=assignment)

        # Build label text
        text = f"Step {idx + 1} / {len(self.step_trace)}"
        if "cell" in s:
            text += f"  |  Last Action: {s['cell']}"
            
        if "h" in s:
            text += f"  |  g = {s['g']}   h = {s['h']}   f = {s['f']}"
            
        self.step_label.config(text=text)

    def _on_slider_moved(self, val):
        self._update_step_display(int(float(val)))

    def _step_prev(self):
        if self._current_step > 0:
            self._update_step_display(self._current_step - 1)
            self.step_slider.set(self._current_step)

    def _step_next(self):
        if self._current_step < len(self.step_trace) - 1:
            self._update_step_display(self._current_step + 1)
            self.step_slider.set(self._current_step)

    def _step_autoplay_toggle(self):
        if self._autoplay_job is not None:
            self._stop_autoplay()
        else:
            self.autoplay_btn.config(text="⏹ Stop")
            self._autoplay_step()

    def _autoplay_step(self):
        if self._current_step >= len(self.step_trace) - 1:
            self._stop_autoplay()
            return
        self._step_next()
        # Max 5s total -> interval = 5000 / num_steps
        interval = max(1, 5000 // max(1, len(self.step_trace)))
        self._autoplay_job = self.root.after(interval, self._autoplay_step)

    def _stop_autoplay(self):
        if self._autoplay_job is not None:
            self.root.after_cancel(self._autoplay_job)
            self._autoplay_job = None
        self.autoplay_btn.config(text="▶▶ Auto")

    # ── File / grid / KB helpers ─────────────────────────────────────────────

    def open_input_file(self):
        path = filedialog.askopenfilename(
            initialdir=INPUT_DIR,
            title="Select input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            puzzle = read_input(path)
            validate_puzzle(puzzle)
            self.current_puzzle = puzzle
            self.current_file = path
            self.file_label.config(text=f"Selected file: {path}")
            self.clear_output()
            self.write_line("Input file loaded successfully.")
            self.write_line("")
            self.display_puzzle(puzzle)
            self.draw_grid(puzzle)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_puzzle(self, puzzle):
        """Print the puzzle to the text log (dots for empty cells)."""
        N = puzzle["N"]
        grid = puzzle["grid"]
        horizontal = puzzle["horizontal"]
        vertical = puzzle["vertical"]

        self.write_line(f"N = {N}")
        self.write_line("")
        self.write_line("Puzzle:")

        for i in range(N):
            row_text = ""
            for j in range(N):
                value = grid[i][j]
                cell = "." if value == 0 else str(value)
                row_text += f" {cell} "
                if j < N - 1:
                    sign = horizontal[i][j]
                    row_text += "<" if sign == 1 else (">" if sign == -1 else " ")
            self.write_line(row_text)

            if i < N - 1:
                vtext = ""
                for j in range(N):
                    sign = vertical[i][j]
                    vtext += " ^ " if sign == 1 else (" v " if sign == -1 else "   ")
                    if j < N - 1:
                        vtext += " "
                self.write_line(vtext)

    def draw_grid(self, puzzle, solution=None):
        """
        Draw the Futoshiki grid on self.grid_canvas.
        solution: dict {(i,j) 1-indexed -> value} (optional).
        """
        self.grid_canvas.delete("all")
        N = puzzle["N"]
        grid = puzzle["grid"]
        horizontal = puzzle["horizontal"]
        vertical = puzzle["vertical"]

        step = CELL_SIZE + GAP_SIZE
        total_w = PADDING * 2 + N * CELL_SIZE + (N - 1) * GAP_SIZE + 4
        total_h = PADDING * 2 + N * CELL_SIZE + (N - 1) * GAP_SIZE + 4
        self.grid_canvas.config(width=total_w, height=total_h)

        for i in range(N):
            for j in range(N):
                x = PADDING + j * step
                y = PADDING + i * step
                x2 = x + CELL_SIZE
                y2 = y + CELL_SIZE

                given = grid[i][j]
                solved_val = None
                if solution is not None:
                    solved_val = solution.get((i + 1, j + 1))

                self.grid_canvas.create_rectangle(
                    x, y, x2, y2, fill="white", outline="#555555", width=2
                )

                if given != 0:
                    self.grid_canvas.create_text(
                        x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                        text=str(given),
                        font=("Arial", int(CELL_SIZE * 0.38), "bold"),
                        fill="red",
                    )
                elif solved_val is not None:
                    self.grid_canvas.create_text(
                        x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                        text=str(solved_val),
                        font=("Arial", int(CELL_SIZE * 0.38), "bold"),
                        fill="black",
                    )

                if j < N - 1:
                    sign = horizontal[i][j]
                    sym = "<" if sign == 1 else (">" if sign == -1 else "")
                    if sym:
                        self.grid_canvas.create_text(
                            x2 + GAP_SIZE // 2, y + CELL_SIZE // 2,
                            text=sym, font=("Arial", 13, "bold"), fill="red",
                        )

                if i < N - 1:
                    sign = vertical[i][j]
                    sym = "^" if sign == 1 else ("v" if sign == -1 else "")
                    if sym:
                        self.grid_canvas.create_text(
                            x + CELL_SIZE // 2, y2 + GAP_SIZE // 2,
                            text=sym, font=("Arial", 13, "bold"), fill="red",
                        )

    def generate_kb_cnf(self):
        if self.current_puzzle is None:
            messagebox.showwarning("Warning", "Please open an input file first.")
            return
        try:
            kb = generate_ground_kb(self.current_puzzle)
            clauses = generate_cnf(self.current_puzzle)

            self.write_line("")
            self.write_line("========== KB/CNF SUMMARY ==========")
            self.write_line(f"N: {kb['N']}")
            self.write_line(f"Number of domains: {len(kb['domains'])}")
            self.write_line(f"Number of row constraints: {len(kb['row_constraints'])}")
            self.write_line(f"Number of column constraints: {len(kb['column_constraints'])}")
            self.write_line(f"Number of inequality constraints: {len(kb['inequality_constraints'])}")
            self.write_line(f"Number of given constraints: {len(kb['given_constraints'])}")
            self.write_line(f"Number of facts: {len(kb['facts'])}")
            self.write_line(f"Number of CNF clauses: {len(clauses)}")
            self.write_line("====================================")
            self.write_line("")
            self.write_line("First 10 facts:")
            for fact in kb["facts"][:10]:
                self.write_line(str(fact))
            self.write_line("")
            self.write_line("First 10 CNF clauses:")
            for clause in clauses[:10]:
                self.write_line(str(clause))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _log_kb_summary(self, puzzle):
        """Write a compact KB/CNF header to the log (used by chaining algos)."""
        try:
            kb = generate_ground_kb(puzzle)
            clauses = generate_cnf(puzzle)
            self.write_line("")
            self.write_line("--- KB/CNF Summary ---")
            self.write_line(
                f"N={kb['N']}  Facts={len(kb['facts'])}  "
                f"CNF clauses={len(clauses)}  "
                f"Inequality constraints={len(kb['inequality_constraints'])}"
            )
            self.write_line("----------------------")
        except Exception:
            pass

    # ── Solver helpers ───────────────────────────────────────────────────────

    def _build_board_and_constraints(self, puzzle):
        """Convert puzzle dict to a mutable 0-indexed board + constraint list."""
        board = [row[:] for row in puzzle["grid"]]
        constraints = parse_and_convert(puzzle)
        return board, constraints

    # ── Main solve entry point ───────────────────────────────────────────────

    def solve_puzzle(self):
        if self.current_puzzle is None:
            messagebox.showwarning("Warning", "Please open an input file first.")
            return

        algo = self.algo_var.get()
        try:
            timeout = int(self.timeout_var.get())
            max_exp = int(self.max_exp_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Timeout or Max Inf/Exp value.")
            return

        # Lock UI
        self.btn_solve.config(state="disabled")
        self.status_label.config(text="Status: Running…", fg="blue")
        self.runtime_label.config(text="Runtime: —")
        self.expand_label.config(text="Inferences/Expansions: —")
        self.write_line("")
        self.write_line(f"========== SOLVING  ({algo}) ==========")

        # Run in background thread to keep UI responsive
        t = threading.Thread(
            target=self._run_solver,
            args=(self.current_puzzle, algo, timeout, max_exp),
            daemon=True,
        )
        t.start()

    def _run_solver(self, puzzle, algo, timeout, max_exp):
        """Worker thread: run the selected algorithm and post result to main thread."""
        result = {
            "algo": algo,
            "success": False,
            "assignment": None,
            "board": None,
            "domains": None,
            "runtime": 0.0,
            "expansions": 0,
            "inferences": 0,
            "limit_msg": None,
            "error": None,
            "steps": [],
        }

        try:
            # ── KB-based (chaining) algorithms ───────────────────────────────
            if algo == "Forward Chaining":
                kb = generate_ground_kb(puzzle)
                t0 = time.perf_counter()
                is_solved, domains, steps = forward_chaining(kb, record_steps=True)
                result["runtime"] = time.perf_counter() - t0
                result["success"] = bool(is_solved)
                result["domains"] = domains
                result["steps"] = steps

            elif algo == "Backward Chaining":
                kb = generate_ground_kb(puzzle)
                t0 = time.perf_counter()
                is_solved, assignment, steps = backward_chaining(kb, record_steps=True)
                result["runtime"] = time.perf_counter() - t0
                result["success"] = bool(is_solved)
                result["assignment"] = assignment
                result["steps"] = steps

            # ── Board-based algorithms ────────────────────────────────────────
            else:
                board, constraints = self._build_board_and_constraints(puzzle)

                if algo == "Brute-Force":
                    solver = BruteForceSolver(
                        time_limit=timeout,
                        max_expansions=max_exp,
                        max_inferences=max_exp,
                        record_steps=True
                    )
                elif algo == "Backtracking":
                    solver = BacktrackingSolver(
                        time_limit=timeout,
                        max_expansions=max_exp,
                        max_inferences=max_exp,
                        record_steps=True
                    )
                else:
                    # A* variants
                    heuristic = "h1"
                    if "H2" in algo:
                        heuristic = "h2"
                    elif "H3" in algo:
                        heuristic = "h3"
                    solver = AStarSolver(
                        time_limit=timeout,
                        max_expansions=max_exp,
                        max_inferences=max_exp,
                        heuristic_choice=heuristic,
                        record_steps=True,
                    )

                res = solver.solve(board, constraints)
                result["runtime"] = solver.stats.get_run_time()
                result["expansions"] = solver.stats.expansions
                result["inferences"] = solver.stats.inferences
                result["board"] = board
                result["steps"] = getattr(solver, "steps", [])

                if res is True:
                    result["success"] = True
                elif res is None:
                    result["limit_msg"] = (
                        "Search limit reached (timeout or max expansions/inferences)."
                    )

        except Exception as exc:
            result["error"] = str(exc)

        # Hand back to Tk main thread
        self.root.after(0, self._on_solve_done, result, puzzle)

    def _on_solve_done(self, result, puzzle):
        """Called on the main thread after the solver thread finishes."""
        # Re-enable solve button
        self.btn_solve.config(state="normal")

        algo = result["algo"]
        runtime = result["runtime"]
        expansions = result["expansions"]
        inferences = result["inferences"]

        # Update status bar
        self.runtime_label.config(text=f"Runtime: {runtime:.4f}s")
        if algo in ("Forward Chaining", "Backward Chaining"):
            self.expand_label.config(text="Inferences/Expansions: N/A (KB-based)")
        else:
            self.expand_label.config(
                text=f"Expansions: {expansions}   |   Inferences: {inferences}"
            )

        # ── Error ────────────────────────────────────────────────────────────
        if result["error"]:
            self.status_label.config(text="Status: Error", fg="red")
            self.write_line(f"[ERROR] {result['error']}")
            messagebox.showerror("Error", result["error"])
            return

        # ── Limit reached ────────────────────────────────────────────────────
        if result["limit_msg"]:
            self.status_label.config(text="Status: Limit reached", fg="#cc6600")
            self.write_line(f"[LIMIT] {result['limit_msg']}")
            self.write_line(f"Runtime: {runtime:.4f}s")
            messagebox.showwarning("Limit Reached", result["limit_msg"])
            return

        # ── No solution ──────────────────────────────────────────────────────
        if not result["success"]:
            self.status_label.config(text="Status: No solution found", fg="red")
            self.write_line("No solution found.")
            messagebox.showwarning("Result", "No solution found.")
            return

        # ── Solved ──────────────────────────────────────────────────────────
        self.status_label.config(text="Status: Solved ✓", fg="green")
        self.write_line(f"Runtime: {runtime:.4f}s")
        N = puzzle["N"]

        # ── Step Visualizer Processing ───────────────────────────────────────
        steps = result.get("steps", [])
        if len(steps) > 10000:
            self.write_line(f"Trace too large to visualize ({len(steps)} steps > 10000). Visualization disabled.")
            messagebox.showwarning("Large Trace", f"The solver recorded {len(steps)} steps, which is too large to visualize.\nThe visualizer will be disabled for this run.")
            self._load_step_trace([])
        else:
            self._load_step_trace(steps)
            self.write_line(f"Recorded {len(steps)} steps for visualization.")

        if algo == "Forward Chaining":
            domains = result["domains"]
            # Extract singleton values for grid display
            assignment = {
                cell: next(iter(vals))
                for cell, vals in domains.items()
                if len(vals) == 1
            }
            self.draw_grid(puzzle, solution=assignment)
            self._log_kb_summary(puzzle)
            # Log full domain table
            self.write_line("")
            self.write_line("Final domain state (cell: remaining values):")
            for i in range(1, N + 1):
                for j in range(1, N + 1):
                    vals = sorted(domains.get((i, j), set()))
                    self.write_line(f"  ({i},{j}): {vals}")

        elif algo == "Backward Chaining":
            assignment = result["assignment"]
            self.draw_grid(puzzle, solution=assignment)
            self._log_kb_summary(puzzle)
            buffer = StringIO()
            print_solution(puzzle, assignment, file_object=buffer)
            self.write_line("")
            self.write_line("Solution:")
            self.write_text(buffer.getvalue())
            self._save_solution(puzzle, assignment)

        else:
            # Board-based solvers (Brute-Force, Backtracking, A*)
            board = result["board"]
            assignment = {
                (i + 1, j + 1): board[i][j]
                for i in range(N)
                for j in range(N)
                if board[i][j] != 0
            }
            self.draw_grid(puzzle, solution=assignment)
            buffer = StringIO()
            print_solution(puzzle, assignment, file_object=buffer)
            self.write_line("")
            self.write_line("Solution:")
            self.write_text(buffer.getvalue())
            self._save_solution(puzzle, assignment)

            self.write_line("")
            self.write_line("Solution:")
            self.write_text(buffer.getvalue())
            self._save_solution(puzzle, assignment)

        self.write_line(f"Solved successfully with {algo}.")
        messagebox.showinfo("Success", f"Solved with {algo} in {runtime:.4f}s")

    def _save_solution(self, puzzle, assignment):
        """Write the solution text to the Outputs directory."""
        try:
            buffer = StringIO()
            print_solution(puzzle, assignment, file_object=buffer)
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = self.get_output_path()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(buffer.getvalue())
            self.write_line(f"Saved solution to: {output_path}")
        except Exception as exc:
            self.write_line(f"[Warning] Could not save solution: {exc}")

    # ── Export / paths ───────────────────────────────────────────────────────

    def export_cnf(self):
        if self.current_puzzle is None:
            messagebox.showwarning("Warning", "Please open an input file first.")
            return
        try:
            os.makedirs(CNF_DIR, exist_ok=True)
            if self.current_file:
                base_name = os.path.basename(self.current_file)
                name_without_ext = os.path.splitext(base_name)[0]
                output_path = os.path.join(CNF_DIR, name_without_ext + ".cnf")
            else:
                output_path = os.path.join(CNF_DIR, "output.cnf")
            write_dimacs_cnf(self.current_puzzle, output_path)
            self.write_line("")
            self.write_line(f"CNF exported to: {output_path}")
            messagebox.showinfo("Success", f"CNF exported to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_output_path(self):
        """Map Inputs/input-XX.txt → Outputs/output-XX.txt."""
        if self.current_file:
            base_name = os.path.basename(self.current_file)
            name_without_ext = os.path.splitext(base_name)[0]
            if name_without_ext.startswith("input"):
                output_name = name_without_ext.replace("input", "output", 1) + ".txt"
            else:
                output_name = name_without_ext + "_solution.txt"
            return os.path.join(OUTPUT_DIR, output_name)
        return os.path.join(OUTPUT_DIR, "output.txt")

    # ── Utility ──────────────────────────────────────────────────────────────

    def clear_output(self):
        self.text_area.delete("1.0", tk.END)
        self.grid_canvas.delete("all")
        self.grid_canvas.config(width=1, height=1)

    def write_line(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)

    def write_text(self, text):
        self.text_area.insert(tk.END, text)
        if not text.endswith("\n"):
            self.text_area.insert(tk.END, "\n")
        self.text_area.see(tk.END)


def main():
    root = tk.Tk()
    app = FutoshikiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()