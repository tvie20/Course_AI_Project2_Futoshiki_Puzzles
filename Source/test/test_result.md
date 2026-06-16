# Futoshiki Algorithm Test Results

Limits: 60 seconds, 1,000,000 expansions/inferences

## Average Results (Over 10 tests)

| Algorithm | Correctness | Avg Run Time (s) | Avg Memory | Avg Inferences/Expansions |
|---|---|---|---|---|
| Brute-Force | 0% | 19.2670 | 9.77 KB | 1000001 |
| Backtracking | 100% | 0.2358 | 1.12 KB | 4799 |
| A* Search (h1) | 100% | 0.3789 | 21.59 KB | 5254 |
| Forward Chaining | 40% | 0.0050 | 543.91 KB | 141 |
| Backward Chaining | 100% | 0.2083 | 524.33 KB | 4798 |

## Detailed Results

| Test | Algorithm | Correctness | Run Time (s) | Memory | Inferences/Expansions |
|---|---|---|---|---|---|
| Input-01 | Brute-Force | Limit Exceeded | 11.9182 | 3.97 KB | 1000001 |
| Input-01 | Backtracking | Yes | 0.0004 | 0.48 KB | 14 |
| Input-01 | A* Search (h1) | Yes | 0.0006 | 3.28 KB | 14 |
| Input-01 | Forward Chaining | Yes | 0.0010 | 64.59 KB | 36 |
| Input-01 | Backward Chaining | Yes | 0.0006 | 54.15 KB | 13 |
| Input-02 | Brute-Force | Limit Exceeded | 11.7508 | 4.02 KB | 1000001 |
| Input-02 | Backtracking | Yes | 0.0005 | 0.54 KB | 13 |
| Input-02 | A* Search (h1) | Yes | 0.0005 | 2.55 KB | 13 |
| Input-02 | Forward Chaining | Yes | 0.0008 | 60.40 KB | 36 |
| Input-02 | Backward Chaining | Yes | 0.0003 | 53.55 KB | 12 |
| Input-03 | Brute-Force | Limit Exceeded | 14.4222 | 6.22 KB | 1000001 |
| Input-03 | Backtracking | Yes | 0.0005 | 0.70 KB | 23 |
| Input-03 | A* Search (h1) | Yes | 0.0010 | 3.82 KB | 24 |
| Input-03 | Forward Chaining | Yes | 0.0032 | 159.89 KB | 76 |
| Input-03 | Backward Chaining | Yes | 0.0010 | 149.62 KB | 22 |
| Input-04 | Brute-Force | Limit Exceeded | 14.3122 | 6.22 KB | 1000001 |
| Input-04 | Backtracking | Yes | 0.0005 | 0.70 KB | 24 |
| Input-04 | A* Search (h1) | Yes | 0.0011 | 5.89 KB | 24 |
| Input-04 | Forward Chaining | Yes | 0.0048 | 159.04 KB | 76 |
| Input-04 | Backward Chaining | Yes | 0.0006 | 149.62 KB | 23 |
| Input-05 | Brute-Force | Limit Exceeded | 17.7087 | 8.75 KB | 1000001 |
| Input-05 | Backtracking | Yes | 0.0032 | 0.98 KB | 120 |
| Input-05 | A* Search (h1) | Yes | 0.0071 | 10.49 KB | 117 |
| Input-05 | Forward Chaining | No | 0.0022 | 308.74 KB | 102 |
| Input-05 | Backward Chaining | Yes | 0.0053 | 298.35 KB | 119 |
| Input-06 | Brute-Force | Limit Exceeded | 17.6379 | 8.75 KB | 1000001 |
| Input-06 | Backtracking | Yes | 0.0038 | 0.98 KB | 90 |
| Input-06 | A* Search (h1) | Yes | 0.0049 | 16.21 KB | 90 |
| Input-06 | Forward Chaining | No | 0.0045 | 309.23 KB | 90 |
| Input-06 | Backward Chaining | Yes | 0.0033 | 298.16 KB | 89 |
| Input-07 | Brute-Force | Limit Exceeded | 21.7606 | 12.12 KB | 1000001 |
| Input-07 | Backtracking | Yes | 0.2657 | 1.39 KB | 7583 |
| Input-07 | A* Search (h1) | Yes | 0.4503 | 27.17 KB | 7598 |
| Input-07 | Forward Chaining | No | 0.0034 | 563.52 KB | 140 |
| Input-07 | Backward Chaining | Yes | 0.2314 | 548.22 KB | 7582 |
| Input-08 | Brute-Force | Limit Exceeded | 21.7575 | 12.12 KB | 1000001 |
| Input-08 | Backtracking | Yes | 0.0889 | 1.39 KB | 1975 |
| Input-08 | A* Search (h1) | Yes | 0.1114 | 30.05 KB | 1978 |
| Input-08 | Forward Chaining | No | 0.0040 | 563.98 KB | 145 |
| Input-08 | Backward Chaining | Yes | 0.0659 | 546.01 KB | 1974 |
| Input-09 | Brute-Force | Limit Exceeded | 30.8665 | 17.75 KB | 1000001 |
| Input-09 | Backtracking | Yes | 1.8299 | 2.02 KB | 35419 |
| Input-09 | A* Search (h1) | Yes | 2.9998 | 48.84 KB | 39957 |
| Input-09 | Forward Chaining | No | 0.0128 | 1.57 MB | 373 |
| Input-09 | Backward Chaining | Yes | 1.6329 | 1.52 MB | 35418 |
| Input-10 | Brute-Force | Limit Exceeded | 30.5357 | 17.75 KB | 1000001 |
| Input-10 | Backtracking | Yes | 0.1652 | 2.02 KB | 2725 |
| Input-10 | A* Search (h1) | Yes | 0.2123 | 67.59 KB | 2725 |
| Input-10 | Forward Chaining | No | 0.0136 | 1.60 MB | 337 |
| Input-10 | Backward Chaining | Yes | 0.1414 | 1.55 MB | 2724 |
