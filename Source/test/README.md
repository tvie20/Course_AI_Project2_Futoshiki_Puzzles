# Hướng dẫn sử dụng Test Suite (Futoshiki AI Lab)

Bộ test này tự động đánh giá các thuật toán (bao gồm 3 biến thể Heuristic của A*) trên 10 file input có sẵn và xuất kết quả ra file `test_result.md`.

## Lệnh Chạy Cấu Hình Mặc Định

Để chạy bộ test với **giới hạn thời gian 180s** và **giới hạn duyệt 1.000.000 (expansions/inferences)**:

```bash
cd Source/test
python run_tests.py
```

## Lệnh Chạy Cấu Hình Tuỳ Chỉnh (Tuỳ Chọn)

Bạn có thể thay đổi các hệ số thời gian (time_limit) hoặc số lần duyệt tối đa (max_expansions, max_inferences) cực kỳ linh hoạt thông qua CLI, ví dụ:

```bash
# Đổi giới hạn thời gian lên 300s (5 phút) và giới hạn duyệt lên 5 triệu
python run_tests.py --time-limit 300 --max-expansions 5000000 --max-inferences 5000000
```

## Xem Trợ Giúp Các Cờ (Flags)

Nếu bạn cần xem giải thích về các cờ CLI, hãy gọi:
```bash
python run_tests.py --help
```

## Kết quả đầu ra

Sau khi chạy, kết quả sẽ tự động được ghi/đè vào file `Source/test/test_result.md` dưới định dạng Markdown tiêu chuẩn. 
File kết quả cung cấp 2 bảng:
1. **Average Results**: Tính tỷ lệ Correctness và lấy trung bình các chỉ số Run Time, Heuristic Time, Expansions, Inferences trên 10 test của từng thuật toán.
2. **Detailed Results**: Lưu trữ chi tiết thông số từng test của từng thuật toán. 
*(Thuật toán nào không yêu cầu expansion hoặc inference sẽ được đánh dấu 0 ở cột tương ứng).*
