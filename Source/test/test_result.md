# Futoshiki Algorithm Test Results

Limits: 180.0 seconds, 1000000 expansions, 1000000 inferences

## Average Results (Over 10 tests)

| Algorithm | Correctness | Avg Run Time (s) | Avg Memory | Avg Inferences/Expansions |
|---|---|---|---|---|
| Brute-Force | 0% | 13.1590 | 9.77 KB | 1000001 |
| Backtracking | 100% | 0.1710 | 1.12 KB | 4799 |
| A* Search (h1) | 100% | 0.2782 | 21.59 KB | 5254 |
| Forward Chaining | 40% | 0.0039 | 543.77 KB | 141 |
| Backward Chaining | 100% | 0.1535 | 524.31 KB | 4798 |

## Detailed Results

| Test | Algorithm | Correctness | Run Time (s) | Memory | Inferences/Expansions |
|---|---|---|---|---|---|
| Input-01 | Brute-Force | Limit Exceeded | 7.4114 | 3.97 KB | 1000001 |
| Input-01 | Backtracking | Yes | 0.0002 | 0.48 KB | 14 |
| Input-01 | A* Search (h1) | Yes | 0.0005 | 3.28 KB | 14 |
| Input-01 | Forward Chaining | Yes | 0.0010 | 63.29 KB | 36 |
| Input-01 | Backward Chaining | Yes | 0.0005 | 54.05 KB | 13 |
| Input-02 | Brute-Force | Limit Exceeded | 7.9321 | 4.02 KB | 1000001 |
| Input-02 | Backtracking | Yes | 0.0003 | 0.54 KB | 13 |
| Input-02 | A* Search (h1) | Yes | 0.0005 | 2.55 KB | 13 |
| Input-02 | Forward Chaining | Yes | 0.0005 | 60.34 KB | 36 |
| Input-02 | Backward Chaining | Yes | 0.0002 | 53.55 KB | 12 |
| Input-03 | Brute-Force | Limit Exceeded | 10.2116 | 6.22 KB | 1000001 |
| Input-03 | Backtracking | Yes | 0.0004 | 0.70 KB | 23 |
| Input-03 | A* Search (h1) | Yes | 0.0011 | 3.82 KB | 24 |
| Input-03 | Forward Chaining | Yes | 0.0026 | 159.89 KB | 76 |
| Input-03 | Backward Chaining | Yes | 0.0003 | 149.62 KB | 22 |
| Input-04 | Brute-Force | Limit Exceeded | 9.8297 | 6.22 KB | 1000001 |
| Input-04 | Backtracking | Yes | 0.0006 | 0.70 KB | 24 |
| Input-04 | A* Search (h1) | Yes | 0.0010 | 5.89 KB | 24 |
| Input-04 | Forward Chaining | Yes | 0.0014 | 159.04 KB | 76 |
| Input-04 | Backward Chaining | Yes | 0.0005 | 149.62 KB | 23 |
| Input-05 | Brute-Force | Limit Exceeded | 11.4824 | 8.75 KB | 1000001 |
| Input-05 | Backtracking | Yes | 0.0022 | 0.98 KB | 120 |
| Input-05 | A* Search (h1) | Yes | 0.0046 | 10.49 KB | 117 |
| Input-05 | Forward Chaining | No | 0.0027 | 308.74 KB | 102 |
| Input-05 | Backward Chaining | Yes | 0.0035 | 298.30 KB | 119 |
| Input-06 | Brute-Force | Limit Exceeded | 11.9046 | 8.75 KB | 1000001 |
| Input-06 | Backtracking | Yes | 0.0024 | 0.98 KB | 90 |
| Input-06 | A* Search (h1) | Yes | 0.0043 | 16.21 KB | 90 |
| Input-06 | Forward Chaining | No | 0.0014 | 309.23 KB | 90 |
| Input-06 | Backward Chaining | Yes | 0.0024 | 298.16 KB | 89 |
| Input-07 | Brute-Force | Limit Exceeded | 14.6475 | 12.12 KB | 1000001 |
| Input-07 | Backtracking | Yes | 0.2184 | 1.39 KB | 7583 |
| Input-07 | A* Search (h1) | Yes | 0.3094 | 27.17 KB | 7598 |
| Input-07 | Forward Chaining | No | 0.0031 | 563.52 KB | 140 |
| Input-07 | Backward Chaining | Yes | 0.1683 | 548.22 KB | 7582 |
| Input-08 | Brute-Force | Limit Exceeded | 15.3679 | 12.12 KB | 1000001 |
| Input-08 | Backtracking | Yes | 0.0538 | 1.39 KB | 1975 |
| Input-08 | A* Search (h1) | Yes | 0.0802 | 30.05 KB | 1978 |
| Input-08 | Forward Chaining | No | 0.0048 | 563.98 KB | 145 |
| Input-08 | Backward Chaining | Yes | 0.0529 | 546.01 KB | 1974 |
| Input-09 | Brute-Force | Limit Exceeded | 21.4582 | 17.75 KB | 1000001 |
| Input-09 | Backtracking | Yes | 1.3287 | 2.02 KB | 35419 |
| Input-09 | A* Search (h1) | Yes | 2.2296 | 48.84 KB | 39957 |
| Input-09 | Forward Chaining | No | 0.0107 | 1.57 MB | 373 |
| Input-09 | Backward Chaining | Yes | 1.1990 | 1.52 MB | 35418 |
| Input-10 | Brute-Force | Limit Exceeded | 21.3445 | 17.75 KB | 1000001 |
| Input-10 | Backtracking | Yes | 0.1029 | 2.02 KB | 2725 |
| Input-10 | A* Search (h1) | Yes | 0.1506 | 67.59 KB | 2725 |
| Input-10 | Forward Chaining | No | 0.0106 | 1.60 MB | 337 |
| Input-10 | Backward Chaining | Yes | 0.1078 | 1.55 MB | 2724 |
