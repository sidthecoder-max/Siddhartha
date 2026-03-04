"""
Missionaries and Cannibals Problem
----------------------------------

Problem:
- 3 Missionaries and 3 Cannibals on left bank
- One boat (capacity = 2)
- Cannibals must never outnumber missionaries on either bank
- Goal: Move everyone safely to right bank

This file implements:
- State representation
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Performance comparison
"""

from collections import deque
import time


class State:
    def __init__(self, missionaries, cannibals, boat):
        """
        missionaries: number of missionaries on left bank
        cannibals: number of cannibals on left bank
        boat: 1 if boat on left bank, 0 if on right bank
        """
        self.m = missionaries
        self.c = cannibals
        self.boat = boat

    def is_valid(self):
        """
        Check if state satisfies problem constraints
        """
        # Bounds check
        if self.m < 0 or self.c < 0 or self.m > 3 or self.c > 3:
            return False

        # Left bank safety
        if self.m > 0 and self.m < self.c:
            return False

        # Right bank safety
        right_m = 3 - self.m
        right_c = 3 - self.c

        if right_m > 0 and right_m < right_c:
            return False

        return True

    def is_goal(self):
        """
        Goal state: all on right bank
        """
        return self.m == 0 and self.c == 0 and self.boat == 0

    def __eq__(self, other):
        return (self.m, self.c, self.boat) == (other.m, other.c, other.boat)

    def __hash__(self):
        return hash((self.m, self.c, self.boat))

    def __repr__(self):
        side = "Left" if self.boat == 1 else "Right"
        return f"(M={self.m}, C={self.c}, Boat={side})"


def get_successors(state):
    """
    Generate all possible legal next states
    """
    moves = [
        (1, 0),  # 1 missionary
        (2, 0),  # 2 missionaries
        (0, 1),  # 1 cannibal
        (0, 2),  # 2 cannibals
        (1, 1)   # 1 missionary & 1 cannibal
    ]

    successors = []

    for m, c in moves:
        if state.boat == 1:  # Boat on left -> move to right
            new_state = State(state.m - m, state.c - c, 0)
        else:  # Boat on right -> move to left
            new_state = State(state.m + m, state.c + c, 1)

        if new_state.is_valid():
            successors.append(new_state)

    return successors


# -----------------------------
# Breadth-First Search (BFS)
# -----------------------------
def bfs(initial_state):
    start_time = time.time()

    queue = deque([(initial_state, [])])
    visited = set()
    nodes_expanded = 0

    while queue:
        state, path = queue.popleft()
        nodes_expanded += 1

        if state.is_goal():
            end_time = time.time()
            return path + [state], nodes_expanded, end_time - start_time

        visited.add(state)

        for successor in get_successors(state):
            if successor not in visited:
                queue.append((successor, path + [state]))

    return None, nodes_expanded, 0


# -----------------------------
# Depth-First Search (DFS)
# -----------------------------
def dfs(initial_state):
    start_time = time.time()

    stack = [(initial_state, [])]
    visited = set()
    nodes_expanded = 0

    while stack:
        state, path = stack.pop()
        nodes_expanded += 1

        if state.is_goal():
            end_time = time.time()
            return path + [state], nodes_expanded, end_time - start_time

        if state not in visited:
            visited.add(state)

            for successor in get_successors(state):
                stack.append((successor, path + [state]))

    return None, nodes_expanded, 0


def print_solution(path):
    """
    Nicely print solution steps
    """
    print("\nSolution Steps:\n")
    for step, state in enumerate(path):
        print(f"Step {step}: {state}")


if __name__ == "__main__":

    initial_state = State(3, 3, 1)

    print("===== Missionaries and Cannibals Problem =====\n")

    # BFS Execution
    print("Running BFS...\n")
    bfs_path, bfs_nodes, bfs_time = bfs(initial_state)

    if bfs_path:
        print_solution(bfs_path)
        print("\nBFS Performance:")
        print("Nodes Expanded:", bfs_nodes)
        print("Time Taken:", round(bfs_time, 6), "seconds")
    else:
        print("No solution found using BFS.")

    print("\n--------------------------------------------\n")

    # DFS Execution
    print("Running DFS...\n")
    dfs_path, dfs_nodes, dfs_time = dfs(initial_state)

    if dfs_path:
        print_solution(dfs_path)
        print("\nDFS Performance:")
        print("Nodes Expanded:", dfs_nodes)
        print("Time Taken:", round(dfs_time, 6), "seconds")
    else:
        print("No solution found using DFS.")

    print("\n============================================\n")
    print("Performance Comparison:")
    print(f"BFS -> Nodes: {bfs_nodes}, Time: {round(bfs_time, 6)} sec")
    print(f"DFS -> Nodes: {dfs_nodes}, Time: {round(dfs_time, 6)} sec")