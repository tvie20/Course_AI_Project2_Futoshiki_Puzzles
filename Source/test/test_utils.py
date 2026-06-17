import time

class SearchLimitExceeded(Exception):
    """Exception raised when a search algorithm exceeds time or expansion limits."""
    pass

class SearchStats:
    def __init__(self, time_limit=180.0, max_expansions=1000000, max_inferences=1000000):
        self.expansions = 0
        self.inferences = 0
        self.heuristic_time = 0.0
        self.time_limit = time_limit
        self.max_expansions = max_expansions
        self.max_inferences = max_inferences
        self.start_time = None

    def start_timer(self):
        self.start_time = time.perf_counter()

    def get_run_time(self):
        if self.start_time is None:
            return 0.0
        return time.perf_counter() - self.start_time

    def check_limits(self):
        if self.expansions > self.max_expansions:
            raise SearchLimitExceeded("Max expansions limit reached")
        if self.inferences > self.max_inferences:
            raise SearchLimitExceeded("Max inferences limit reached")
        if self.start_time is not None and self.get_run_time() > self.time_limit:
            raise SearchLimitExceeded("Time limit reached")

class BaseSolver:
    def __init__(self, time_limit=60.0, max_expansions=1000000, max_inferences=1000000):
        self.stats = SearchStats(time_limit, max_expansions, max_inferences)
        
    def solve(self, board, constraints):
        self.stats.start_timer()
        try:
            return self._run_algorithm(board, constraints)
        except SearchLimitExceeded:
            return None

    def _run_algorithm(self, board, constraints):
        raise NotImplementedError("Subclasses must implement _run_algorithm")
