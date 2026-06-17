import os
import tkinter as tk
from tkinter import filedialog, messagebox
from io import StringIO

from futoshiki_io import read_input, validate_puzzle
from kb_generator import generate_ground_kb, generate_cnf, write_dimacs_cnf
from inference import backward_chaining, print_solution


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "Inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Outputs")
CNF_DIR = os.path.join(BASE_DIR, "CNF")


class FutoshikiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Futoshiki Project 2 - Logic Solver GUI")
        self.root.geometry("1050x700")

        self.current_puzzle = None
        self.current_file = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Futoshiki Puzzle - Data, KB, CNF & Solver",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        btn_open = tk.Button(
            button_frame,
            text="Open Input File",
            width=18,
            command=self.open_input_file
        )
        btn_open.grid(row=0, column=0, padx=5)

        btn_kb = tk.Button(
            button_frame,
            text="Generate KB/CNF",
            width=18,
            command=self.generate_kb_cnf
        )
        btn_kb.grid(row=0, column=1, padx=5)

        btn_solve = tk.Button(
            button_frame,
            text="Solve",
            width=18,
            command=self.solve_puzzle
        )
        btn_solve.grid(row=0, column=2, padx=5)

        btn_export = tk.Button(
            button_frame,
            text="Export CNF",
            width=18,
            command=self.export_cnf
        )
        btn_export.grid(row=0, column=3, padx=5)

        btn_clear = tk.Button(
            button_frame,
            text="Clear",
            width=18,
            command=self.clear_output
        )
        btn_clear.grid(row=0, column=4, padx=5)

        self.file_label = tk.Label(
            self.root,
            text="No file selected",
            font=("Arial", 10)
        )
        self.file_label.pack(pady=5)

        self.text_area = tk.Text(
            self.root,
            wrap="none",
            font=("Consolas", 11)
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

    def open_input_file(self):
        path = filedialog.askopenfilename(
            initialdir=INPUT_DIR,
            title="Select input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
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

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_puzzle(self, puzzle):
        """
        Hiển thị đề bài ban đầu.
        Dấu . là ô trống.
        Dấu ^ nghĩa là top < bottom.
        Dấu v nghĩa là top > bottom.
        """
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

                    if sign == 1:
                        row_text += "<"
                    elif sign == -1:
                        row_text += ">"
                    else:
                        row_text += " "

            self.write_line(row_text)

            if i < N - 1:
                vertical_text = ""

                for j in range(N):
                    sign = vertical[i][j]

                    # Theo đề: 1 = top < bottom, -1 = top > bottom.
                    # Khi hiển thị dọc: ^ = top < bottom, v = top > bottom.
                    if sign == 1:
                        vertical_text += " ^ "
                    elif sign == -1:
                        vertical_text += " v "
                    else:
                        vertical_text += "   "

                    if j < N - 1:
                        vertical_text += " "

                self.write_line(vertical_text)

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

    def solve_puzzle(self):
        if self.current_puzzle is None:
            messagebox.showwarning("Warning", "Please open an input file first.")
            return

        try:
            kb = generate_ground_kb(self.current_puzzle)

            self.write_line("")
            self.write_line("========== SOLVING ==========")

            is_solved, assignment = backward_chaining(kb)

            if not is_solved:
                self.write_line("No solution found.")
                messagebox.showwarning("Result", "No solution found.")
                return

            buffer = StringIO()
            print_solution(self.current_puzzle, assignment, file_object=buffer)
            solution_text = buffer.getvalue()

            self.write_line("Solution:")
            self.write_text(solution_text)
            self.write_line("Solution generated successfully.")

            os.makedirs(OUTPUT_DIR, exist_ok=True)

            output_path = self.get_output_path()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(solution_text)

            self.write_line(f"Saved solution to: {output_path}")
            messagebox.showinfo("Success", f"Solved and saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

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
        """
        Nếu mở Inputs/input-01.txt thì lưu thành Outputs/output-01.txt.
        """
        if self.current_file:
            base_name = os.path.basename(self.current_file)
            name_without_ext = os.path.splitext(base_name)[0]

            if name_without_ext.startswith("input"):
                output_name = name_without_ext.replace("input", "output", 1) + ".txt"
            else:
                output_name = name_without_ext + "_solution.txt"

            return os.path.join(OUTPUT_DIR, output_name)

        return os.path.join(OUTPUT_DIR, "output.txt")

    def clear_output(self):
        self.text_area.delete("1.0", tk.END)

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