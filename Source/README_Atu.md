# Module Data & KB - Atu

## 1. Chạy môi trường

Máy của Atu chạy bằng Python 3.9:

```bash
py -3.9 test_kb.py
```

Nếu máy khác nhận lệnh `python`, có thể chạy:

```bash
python test_kb.py
```

---

## 2. Cấu trúc input

Các input nằm trong thư mục:

```text
Inputs/
```

Bao gồm:

```text
input-01.txt
input-02.txt
...
input-10.txt
```

Kích thước test case:

```text
input-01.txt: 4x4
input-02.txt: 4x4
input-03.txt: 5x5
input-04.txt: 5x5
input-05.txt: 6x6
input-06.txt: 6x6
input-07.txt: 7x7
input-08.txt: 7x7
input-09.txt: 9x9
input-10.txt: 9x9
```

Format mỗi input:

```text
N
N dòng grid
N dòng horizontal constraints
N-1 dòng vertical constraints
```

Quy ước:

```text
0  = ô trống hoặc không có ràng buộc
1  = dấu <
-1 = dấu >
```

---

## 3. Đọc input

```python
from futoshiki_io import read_input

puzzle = read_input("Inputs/input-01.txt")

N = puzzle["N"]
grid = puzzle["grid"]
horizontal = puzzle["horizontal"]
vertical = puzzle["vertical"]
```

---

## 4. Kiểm tra input

```python
from futoshiki_io import validate_puzzle

validate_puzzle(puzzle)
```

Nếu input sai format, hàm sẽ báo lỗi.

---

## 5. Sinh facts

```python
from kb_generator import generate_facts

facts = generate_facts(puzzle)
```

Facts có dạng tuple:

```python
("Less", v1, v2)
("Given", i, j, v)
("LessH", i, j)
("GreaterH", i, j)
("LessV", i, j)
("GreaterV", i, j)
```

Ví dụ:

```python
("Given", 1, 2, 2)
("LessH", 1, 1)
```

---

## 6. Sinh ground KB

```python
from kb_generator import generate_ground_kb

kb = generate_ground_kb(puzzle)
```

KB trả về dictionary gồm:

```python
kb["N"]
kb["domains"]
kb["row_constraints"]
kb["column_constraints"]
kb["inequality_constraints"]
kb["given_constraints"]
kb["facts"]
kb["cnf"]
```

Trong đó:

```python
kb["domains"][(i, j)] = {1, 2, ..., N}
```

Ràng buộc bất đẳng thức có dạng:

```python
("less", (i1, j1), (i2, j2))
("greater", (i1, j1), (i2, j2))
```

Ví dụ:

```python
("less", (1, 1), (1, 2))
```

nghĩa là ô `(1,1) < (1,2)`.

---

## 7. Sinh CNF

```python
from kb_generator import generate_cnf

clauses = generate_cnf(puzzle)
```

CNF là list các clause. Mỗi clause là list số nguyên.

Ví dụ:

```python
[1, 2, 3, 4]
[-1, -2]
```

Số dương biểu diễn literal `Val(i,j,v)`. Số âm biểu diễn literal `¬Val(i,j,v)`.

---

## 8. Mã hóa biến CNF

```python
from kb_generator import var_id, decode_var

x = var_id(1, 1, 2, 4)
print(x)

print(decode_var(x, 4))
```

Công thức:

```text
Val(i,j,v) -> var_id(i,j,v,N)
```

Ví dụ với N = 4:

```text
Val(1,1,1) -> 1
Val(1,1,2) -> 2
Val(1,1,3) -> 3
Val(1,1,4) -> 4
```

---

## 9. Cách chạy test toàn bộ 10 input

```bash
py -3.9 test_kb.py
```

Kết quả hiện tại:

```text
Inputs/input-01.txt
N: 4
Facts: 17
CNF clauses: 378
----------------------------------------
Inputs/input-02.txt
N: 4
Facts: 17
CNF clauses: 378
----------------------------------------
Inputs/input-03.txt
N: 5
Facts: 27
CNF clauses: 946
----------------------------------------
Inputs/input-04.txt
N: 5
Facts: 27
CNF clauses: 946
----------------------------------------
Inputs/input-05.txt
N: 6
Facts: 36
CNF clauses: 1937
----------------------------------------
Inputs/input-06.txt
N: 6
Facts: 36
CNF clauses: 1937
----------------------------------------
Inputs/input-07.txt
N: 7
Facts: 45
CNF clauses: 3565
----------------------------------------
Inputs/input-08.txt
N: 7
Facts: 45
CNF clauses: 3565
----------------------------------------
Inputs/input-09.txt
N: 9
Facts: 93
CNF clauses: 10470
----------------------------------------
Inputs/input-10.txt
N: 9
Facts: 97
CNF clauses: 10650
----------------------------------------
```

---

## 10. Cách các thành viên khác gọi module

```python
from futoshiki_io import read_input, validate_puzzle
from kb_generator import generate_ground_kb, generate_cnf

puzzle = read_input("Inputs/input-01.txt")
validate_puzzle(puzzle)

kb = generate_ground_kb(puzzle)
clauses = generate_cnf(puzzle)

N = kb["N"]
domains = kb["domains"]
row_constraints = kb["row_constraints"]
column_constraints = kb["column_constraints"]
inequality_constraints = kb["inequality_constraints"]
given_constraints = kb["given_constraints"]
facts = kb["facts"]
cnf = kb["cnf"]
```

---

## 11. Ghi chú cho nhóm

- Index trong module bắt đầu từ 1.
- Ô được biểu diễn dạng `(i, j)`.
- Ràng buộc nhỏ hơn biểu diễn dạng `("less", cell1, cell2)`.
- Ràng buộc lớn hơn biểu diễn dạng `("greater", cell1, cell2)`.
- CNF dùng biến nguyên, mã hóa từ `Val(i,j,v)` bằng hàm `var_id(i,j,v,N)`.

---

## 12. Xuất CNF ra file DIMACS

Module có hỗ trợ xuất CNF ra file `.cnf` theo chuẩn DIMACS.

Chạy lệnh:

```bash
py -3.9 export_cnf.py
```

Kết quả sẽ được lưu trong thư mục:

```text
CNF/
```

Bao gồm:

```text
input-01.cnf
input-02.cnf
...
input-10.cnf
```

Ví dụ dòng đầu của `CNF/input-01.cnf`:

```text
p cnf 64 378
```

Ý nghĩa:

```text
64  = số biến CNF, vì input-01 là 4x4 nên có 4 × 4 × 4 biến
378 = số clauses
```

Mỗi dòng clause kết thúc bằng số `0`, theo đúng format DIMACS.

Ví dụ:

```text
1 2 3 4 0
-1 -2 0
```

Trong đó:

- Số dương biểu diễn literal `Val(i,j,v)`.
- Số âm biểu diễn literal phủ định `¬Val(i,j,v)`.
- Số `0` kết thúc một clause.

---

## 13. GUI

Module có giao diện đơn giản bằng tkinter.

Chạy GUI:

```bash
py -3.9 gui.py
```

Chức năng hiện có:

- Chọn file input.
- Hiển thị puzzle cùng dấu bất đẳng thức.
- Sinh ground KB và CNF.
- Hiển thị số facts, số constraints, số CNF clauses.
- Xuất CNF ra file `.cnf`.

Lưu ý: GUI hiện tại phục vụ phần Data & KB của Atu. Nút solve sẽ được tích hợp sau khi nhóm hoàn thiện solver.
