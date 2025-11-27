# ----------------------------------------------------------
# Deadlock Detection Logic Module
# Contributor: Himanth (Backend Developer)
# Description:
#   This module implements:
#     ✔ Cycle detection in Wait-For Graph (WFG)
#     ✔ Banker's Algorithm for safety state detection
# ----------------------------------------------------------


try:
    import numpy as np
except Exception:
    np = None


class DeadlockDetector:

    def detect_deadlock_wfg(self, graph):
        visited = set()

        # DFS-based cycle detection:
        # If any cycle is found in the Wait-For Graph → deadlock exists
        def dfs(node, stack):
            if node in stack:
                return True
            stack.add(node)
            visited.add(node)
            for neigh in graph.get(node, []):
                if dfs(neigh, stack):
                    return True
            stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node, set()):
                    return True
        return False

    def bankers_algorithm(self, alloc, max_matrix, avail):
        # Provide a numpy-free fallback so the server can run without
        # heavy numeric packages installed.

        if np is not None:
            alloc = np.array(alloc)
            max_matrix = np.array(max_matrix)
            n = len(alloc)
            m = len(avail)
            need = max_matrix - alloc
            work = np.array(avail).copy()
            finish = [False] * n

            safe_seq = []
            while len(safe_seq) < n:
                progress = False
                for i in range(n):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                        work = work + alloc[i]
                        finish[i] = True
                        safe_seq.append(i)
                        progress = True
                if not progress:
                    return False, []
            return True, safe_seq

        else:
            # Pure-Python fallback version of Banker's Algorithm
            # Used when numpy is not available on the system
            n = len(alloc)
            m = len(avail)
            need = [[max_matrix[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
            work = list(avail)
            finish = [False] * n

            safe_seq = []
            while len(safe_seq) < n:
                progress = False
                for i in range(n):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                        work = [work[j] + alloc[i][j] for j in range(m)]
                        finish[i] = True
                        safe_seq.append(i)
                        progress = True
                if not progress:
                    return False, []
            return True, safe_seq
