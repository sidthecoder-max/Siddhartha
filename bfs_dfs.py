"""
Uninformed Search Algorithms:
BFS and DFS implementation
Example: Missionaries and Cannibals Problem
"""

from collections import deque
import time


class State:
    def __init__(self, missionaries, cannibals, boat):
        self.m = missionaries
        self.c = cannibals
        self.boat = boat  # 1 = left, 0 = right

    def is_valid(self):
        """
        Check if state is valid
        """
        if self.m < 0 or self.c < 0 or self.m > 3 or self.c > 3:
            return False

        if (self.m > 0 and self.m < self.c):
            return False

        right_m = 3 - self.m
        right_c = 3 - self.c

        if (right_m > 0 and right_m < right_c):
            return False

        return True

    def is_goal(self):
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
    Generate possible next states
    """
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    successors = []

    for m, c in moves:
        if state.boat == 1:
            new_state = State(state.m - m, state.c - c, 0)
        else:
            new_state = State(state.m + m, state.c + c, 1)

        if new_state.is_valid():
            successors.append(new_state)

    return successors


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


if __name__ == "__main__":
    initial = State(3, 3, 1)

    print("\n===== BFS Search =====")
    bfs_path, bfs_nodes, bfs_time = bfs(initial)
    print("Solution Path:", bfs_path)
    print("Nodes Expanded:", bfs_nodes)
    print("Time Taken:", round(bfs_time, 6), "seconds")

    print("\n===== DFS Search =====")
    dfs_path, dfs_nodes, dfs_time = dfs(initial)
    print("Solution Path:", dfs_path)
    print("Nodes Expanded:", dfs_nodes)
    print("Time Taken:", round(dfs_time, 6), "seconds")

    print("\n===== Performance Comparison =====")
    print(f"BFS -> Nodes: {bfs_nodes}, Time: {round(bfs_time,6)} sec")
    print(f"DFS -> Nodes: {dfs_nodes}, Time: {round(dfs_time,6)} sec")