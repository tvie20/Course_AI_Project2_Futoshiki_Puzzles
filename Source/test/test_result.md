# Futoshiki Algorithm Test Results

Limits: 180.0 seconds, 1000000 expansions, 1000000 inferences

## Average Results (Over 10 tests)

| Algorithm | Correctness | Avg Run Time (s) | Avg Heuristic Time (s) | Avg Memory | Avg Expansions | Avg Inferences |
|---|---|---|---|---|---|---|
| Brute-Force | 0% | 21.0550 | 0.0000 | 9.77 KB | 1000001 | 0 |
| Backtracking | 100% | 0.4359 | 0.0000 | 1.14 KB | 4799 | 0 |
| A* Search (h1) | 100% | 0.4323 | 0.0449 | 21.59 KB | 5254 | 0 |
| A* Search (h2) | 70% | 52.3421 | 6.4872 | 151.08 MB | 275941 | 0 |
| A* Search (h3) | 100% | 0.1649 | 0.1615 | 26.64 KB | 33 | 8510 |
| Forward Chaining | 40% | 0.0054 | 0.0000 | 548.44 KB | 0 | 141 |
| Backward Chaining | 100% | 0.4002 | 0.0000 | 525.14 KB | 0 | 4798 |

## Detailed Results

| Test | Algorithm | Correctness | Run Time (s) | Heuristic Time (s) | Memory | Expansions | Inferences |
|---|---|---|---|---|---|---|---|
| Input-01 | Brute-Force | Limit Exceeded | 9.3553 | 0.0000 | 3.97 KB | 1000001 | 0 |
| Input-01 | Backtracking | Yes | 0.0003 | 0.0000 | 0.48 KB | 14 | 0 |
| Input-01 | A* Search (h1) | Yes | 0.0008 | 0.0001 | 3.35 KB | 14 | 0 |
| Input-01 | A* Search (h2) | Yes | 0.0008 | 0.0001 | 1.89 KB | 18 | 0 |
| Input-01 | A* Search (h3) | Yes | 0.0102 | 0.0095 | 4.66 KB | 13 | 333 |
| Input-01 | Forward Chaining | Yes | 0.0010 | 0.0000 | 63.10 KB | 0 | 36 |
| Input-01 | Backward Chaining | Yes | 0.0004 | 0.0000 | 54.03 KB | 0 | 13 |
| Input-02 | Brute-Force | Limit Exceeded | 13.4292 | 0.0000 | 4.02 KB | 1000001 | 0 |
| Input-02 | Backtracking | Yes | 0.0003 | 0.0000 | 0.54 KB | 13 | 0 |
| Input-02 | A* Search (h1) | Yes | 0.0005 | 0.0001 | 2.49 KB | 13 | 0 |
| Input-02 | A* Search (h2) | Yes | 0.0006 | 0.0001 | 2.05 KB | 17 | 0 |
| Input-02 | A* Search (h3) | Yes | 0.0091 | 0.0085 | 4.66 KB | 13 | 349 |
| Input-02 | Forward Chaining | Yes | 0.0014 | 0.0000 | 60.01 KB | 0 | 36 |
| Input-02 | Backward Chaining | Yes | 0.0003 | 0.0000 | 53.55 KB | 0 | 12 |
| Input-03 | Brute-Force | Limit Exceeded | 16.0672 | 0.0000 | 6.22 KB | 1000001 | 0 |
| Input-03 | Backtracking | Yes | 0.0006 | 0.0000 | 0.70 KB | 23 | 0 |
| Input-03 | A* Search (h1) | Yes | 0.0014 | 0.0002 | 3.82 KB | 24 | 0 |
| Input-03 | A* Search (h2) | Yes | 0.0029 | 0.0003 | 2.83 KB | 62 | 0 |
| Input-03 | A* Search (h3) | Yes | 0.0293 | 0.0281 | 15.50 KB | 20 | 1080 |
| Input-03 | Forward Chaining | Yes | 0.0041 | 0.0000 | 159.89 KB | 0 | 76 |
| Input-03 | Backward Chaining | Yes | 0.0007 | 0.0000 | 149.62 KB | 0 | 22 |
| Input-04 | Brute-Force | Limit Exceeded | 16.1275 | 0.0000 | 6.22 KB | 1000001 | 0 |
| Input-04 | Backtracking | Yes | 0.0006 | 0.0000 | 0.70 KB | 24 | 0 |
| Input-04 | A* Search (h1) | Yes | 0.0014 | 0.0002 | 5.89 KB | 24 | 0 |
| Input-04 | A* Search (h2) | Yes | 0.0042 | 0.0005 | 7.66 KB | 91 | 0 |
| Input-04 | A* Search (h3) | Yes | 0.0215 | 0.0205 | 15.75 KB | 20 | 1247 |
| Input-04 | Forward Chaining | Yes | 0.0035 | 0.0000 | 158.00 KB | 0 | 76 |
| Input-04 | Backward Chaining | Yes | 0.0006 | 0.0000 | 149.62 KB | 0 | 23 |
| Input-05 | Brute-Force | Limit Exceeded | 19.6064 | 0.0000 | 8.75 KB | 1000001 | 0 |
| Input-05 | Backtracking | Yes | 0.0027 | 0.0000 | 0.98 KB | 120 | 0 |
| Input-05 | A* Search (h1) | Yes | 0.0052 | 0.0006 | 10.49 KB | 117 | 0 |
| Input-05 | A* Search (h2) | Yes | 0.0945 | 0.0091 | 290.08 KB | 1926 | 0 |
| Input-05 | A* Search (h3) | Yes | 0.0840 | 0.0815 | 23.27 KB | 29 | 3714 |
| Input-05 | Forward Chaining | No | 0.0019 | 0.0000 | 311.25 KB | 0 | 102 |
| Input-05 | Backward Chaining | Yes | 0.0044 | 0.0000 | 298.35 KB | 0 | 119 |
| Input-06 | Brute-Force | Limit Exceeded | 19.6483 | 0.0000 | 8.75 KB | 1000001 | 0 |
| Input-06 | Backtracking | Yes | 0.0028 | 0.0000 | 0.98 KB | 90 | 0 |
| Input-06 | A* Search (h1) | Yes | 0.0060 | 0.0007 | 16.21 KB | 90 | 0 |
| Input-06 | A* Search (h2) | Yes | 0.0306 | 0.0036 | 34.73 KB | 535 | 0 |
| Input-06 | A* Search (h3) | Yes | 0.0704 | 0.0682 | 23.11 KB | 29 | 3664 |
| Input-06 | Forward Chaining | No | 0.0029 | 0.0000 | 311.25 KB | 0 | 90 |
| Input-06 | Backward Chaining | Yes | 0.0030 | 0.0000 | 298.16 KB | 0 | 89 |
| Input-07 | Brute-Force | Limit Exceeded | 24.0146 | 0.0000 | 12.12 KB | 1000001 | 0 |
| Input-07 | Backtracking | Yes | 0.3086 | 0.0000 | 1.39 KB | 7583 | 0 |
| Input-07 | A* Search (h1) | Yes | 0.4895 | 0.0513 | 27.17 KB | 7598 | 0 |
| Input-07 | A* Search (h2) | Limit Exceeded | 115.6098 | 7.2727 | 215.95 MB | 1000001 | 0 |
| Input-07 | A* Search (h3) | Yes | 0.1374 | 0.1337 | 34.55 KB | 41 | 9084 |
| Input-07 | Forward Chaining | No | 0.0038 | 0.0000 | 573.12 KB | 0 | 140 |
| Input-07 | Backward Chaining | Yes | 0.4200 | 0.0000 | 550.45 KB | 0 | 7582 |
| Input-08 | Brute-Force | Limit Exceeded | 24.1983 | 0.0000 | 12.12 KB | 1000001 | 0 |
| Input-08 | Backtracking | Yes | 0.1001 | 0.0000 | 1.45 KB | 1975 | 0 |
| Input-08 | A* Search (h1) | Yes | 0.1254 | 0.0135 | 30.05 KB | 1978 | 0 |
| Input-08 | A* Search (h2) | Yes | 37.3055 | 2.7264 | 41.63 MB | 378969 | 0 |
| Input-08 | A* Search (h3) | Yes | 0.1630 | 0.1591 | 34.20 KB | 41 | 8874 |
| Input-08 | Forward Chaining | No | 0.0059 | 0.0000 | 573.48 KB | 0 | 145 |
| Input-08 | Backward Chaining | Yes | 0.1170 | 0.0000 | 548.23 KB | 0 | 1974 |
| Input-09 | Brute-Force | Limit Exceeded | 33.9907 | 0.0000 | 17.75 KB | 1000001 | 0 |
| Input-09 | Backtracking | Yes | 3.6563 | 0.0000 | 2.07 KB | 35419 | 0 |
| Input-09 | A* Search (h1) | Yes | 3.4504 | 0.3578 | 48.84 KB | 39957 | 0 |
| Input-09 | A* Search (h2) | Limit Exceeded | 185.6616 | 31.1593 | 693.35 MB | 634954 | 0 |
| Input-09 | A* Search (h3) | Yes | 0.5018 | 0.4937 | 53.12 KB | 62 | 28502 |
| Input-09 | Forward Chaining | No | 0.0141 | 0.0000 | 1.59 MB | 0 | 373 |
| Input-09 | Backward Chaining | Yes | 3.1986 | 0.0000 | 1.52 MB | 0 | 35418 |
| Input-10 | Brute-Force | Limit Exceeded | 34.1122 | 0.0000 | 17.75 KB | 1000001 | 0 |
| Input-10 | Backtracking | Yes | 0.2868 | 0.0000 | 2.07 KB | 2725 | 0 |
| Input-10 | A* Search (h1) | Yes | 0.2428 | 0.0248 | 67.59 KB | 2725 | 0 |
| Input-10 | A* Search (h2) | Limit Exceeded | 184.7102 | 23.6996 | 559.51 MB | 742833 | 0 |
| Input-10 | A* Search (h3) | Yes | 0.6220 | 0.6126 | 57.53 KB | 61 | 28254 |
| Input-10 | Forward Chaining | No | 0.0152 | 0.0000 | 1.61 MB | 0 | 337 |
| Input-10 | Backward Chaining | Yes | 0.2568 | 0.0000 | 1.55 MB | 0 | 2724 |
