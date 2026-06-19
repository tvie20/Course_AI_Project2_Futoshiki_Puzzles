import time
import os

# Import từ module của atu
from futoshiki_io import read_input
from kb_generator import generate_ground_kb

# Import thuật toán của stinh
from inference import forward_chaining, backward_chaining, print_solution

def run_evaluation():
    # Tạo thư mục Outputs nếu chưa tồn tại
    os.makedirs("Outputs", exist_ok=True)

    print(f"{'Test Case':<15} | {'Kích thước':<10} | {'FC Time (s)':<15} | {'FC Solved':<10} | {'BC Time (s)':<15} | {'BC Solved':<10}")
    print("-" * 85)
    
    for i in range(1, 11):
        input_file = f"Inputs/input-{i:02d}.txt"
        output_file = f"Outputs/output-{i:02d}.txt"
        
        if not os.path.exists(input_file):
            continue
            
        try:
            puzzle = read_input(input_file)
            kb = generate_ground_kb(puzzle)
            N = kb["N"]
        except Exception as e:
            print(f"Lỗi đọc {input_file}: {e}")
            continue
            
        # 1. Chạy và đo thời gian Forward Chaining
        start_fc = time.time()
        is_solved_fc, result_domains = forward_chaining(kb)
        time_fc = time.time() - start_fc
        
        # 2. Chạy và đo thời gian Backward Chaining
        start_bc = time.time()
        is_solved_bc, assignment = backward_chaining(kb)
        time_bc = time.time() - start_bc
        
        # 3. Ghi nghiệm đạt chuẩn định dạng vào thư mục Outputs
        # Ưu tiên ghi nghiệm hoàn chỉnh từ Backward Chaining nếu giải được
        final_solution = assignment if is_solved_bc else result_domains
        with open(output_file, "w", encoding="utf-8") as f:
            print_solution(puzzle, final_solution, file_object=f)
            
        # In bảng thống kê ra màn hình console
        size_str = f"{N}x{N}"
        print(f"input-{i:02d}.txt  | {size_str:<10} | {time_fc:<15.5f} | {str(is_solved_fc):<10} | {time_bc:<15.5f} | {str(is_solved_bc):<10}")

if __name__ == "__main__":
    run_evaluation()