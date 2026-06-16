Here is the execution plan formatted as a direct, actionable prompt for your AI coding agent.

---

### **Implementation Plan: Instrumenting Search Algorithms for Performance Metrics**

**Objective:** Inject tracking counters into existing search algorithms to accurately measure `expansions` (nodes generated/visited) and `inferences` (logic deductions/domain prunings) for a Futoshiki CSP/SAT solver.

**Global Setup Instructions:**
For each algorithm class or function, initialize global tracking variables in the constructor or at the start of the execution context:

* `self.expansions = 0`
* `self.inferences = 0`

Implement the instrumentation based on the specific algorithm as detailed below:
# MUST SET MAX_expansions and MAX_inferences = 1.000.000 and LIMIT_TIME = 60 second
#### **1. Brute-Force Search**

* **Target Metric:** `expansions` (Total states generated).
* **Implementation Rule:** Place `self.expansions += 1` inside the core combination generation loop, or at the very beginning of the recursive state generation function. It must trigger every time a new grid configuration is fully or partially constructed.

#### **2. Backtracking**

* **Target Metric:** `expansions` (Nodes visited on the search tree).
* **Implementation Rule:** Place `self.expansions += 1` at the absolute first line inside the recursive `backtrack(state)` function. It must trigger exactly once per recursive call, representing a step down into a new branch.

#### **3. Forward Chaining / Forward Checking**

* **Target Metric:** `inferences` (Deductions made).
* **Implementation Rule (CSP Context):** Place `self.inferences += 1` inside the constraint propagation logic. Specifically, trigger it every time the algorithm successfully removes (prunes) a value from the domain of an unassigned variable.
* **Implementation Rule (Logic Rules Context):** Increment whenever a rule's premise is satisfied and a new fact is inferred.

#### **4. A* Search (All Heuristics: Empty Cells, Inequalities, AC-3)**

* **Target Metric:** `expansions` (Nodes expanded from the frontier).
* **Implementation Rule:** Place `self.expansions += 1` immediately after the `pop()` operation that removes the node with the lowest $f(n)$ from the priority queue (Open List).
* **Sub-Rule for Heuristic 4c (AC-3):** If AC-3 is utilized for heuristic calculation or preprocessing, track its logic separately. Initialize `self.ac3_inferences = 0` and place `self.ac3_inferences += 1` inside the core `while queue:` loop, triggering every time an arc is evaluated.

#### **5. Backward Chaining**

* **Target Metric:** `inferences` (Sub-goals evaluated).
* **Implementation Rule:** Place `self.inferences += 1` immediately after popping a sub-goal from the goal stack/queue, right before the algorithm checks the knowledge base to prove or disprove that sub-goal.

# Build the test function 
## Output
log to the console (and store in test_result.md file) it must contain 5 row include these 5 algorythm 
and contain 5 **Criteria** include **Correctness  | Run Time | Memory  | Inferences/Expansions . and this will be test using 10 tests in the @Inputs folders
