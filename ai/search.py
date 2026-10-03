from collections import deque
import heapq


# ============================================================
# GET NEIGHBORS
# ============================================================

def get_neighbors(position, game_map):

    row, col = position

    rows = len(game_map)
    cols = len(game_map[0])

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    neighbors = []

    for row_change, col_change in directions:

        new_row = row + row_change
        new_col = col + col_change

        if new_row < 0 or new_row >= rows:
            continue

        if new_col < 0 or new_col >= cols:
            continue

        if game_map[new_row][new_col] == 1:
            continue

        neighbors.append((new_row, new_col))

    return neighbors


# ============================================================
# RECONSTRUCT PATH
# ============================================================

def reconstruct_path(parent, start, goal):

    path = []

    current = goal

    while current is not None:

        path.append(current)

        if current == start:
            break

        current = parent.get(current)

    path.reverse()

    if len(path) == 0 or path[0] != start:
        return []

    return path


# ============================================================
# BREADTH-FIRST SEARCH
# ============================================================

def bfs(game_map, start, goal):

    queue = deque()

    queue.append(start)

    visited = set()

    visited.add(start)

    parent = {
        start: None
    }

    explored = []

    while queue:

        current = queue.popleft()

        explored.append(current)

        if current == goal:

            path = reconstruct_path(
                parent,
                start,
                goal
            )

            return path, explored

        for neighbor in get_neighbors(
            current,
            game_map
        ):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    return [], explored


# ============================================================
# DEPTH-FIRST SEARCH
# ============================================================

def dfs(game_map, start, goal):

    stack = []

    stack.append(start)

    visited = set()

    visited.add(start)

    parent = {
        start: None
    }

    explored = []

    while stack:

        current = stack.pop()

        explored.append(current)

        if current == goal:

            path = reconstruct_path(
                parent,
                start,
                goal
            )

            return path, explored

        for neighbor in get_neighbors(
            current,
            game_map
        ):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                stack.append(neighbor)

    return [], explored


# ============================================================
# MANHATTAN DISTANCE
# ============================================================

def heuristic(position, goal):

    row1, col1 = position
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


# ============================================================
# A* SEARCH
# ============================================================

def astar(game_map, start, goal):

    # Priority queue
    open_list = []

    # Starting node
    heapq.heappush(
        open_list,
        (0, start)
    )

    # Cost from start
    g_cost = {
        start: 0
    }

    # Parent information
    parent = {
        start: None
    }

    # Keep track of explored cells
    explored = []

    visited = set()

    while open_list:

        current_priority, current = heapq.heappop(
            open_list
        )

        if current in visited:
            continue

        visited.add(current)

        explored.append(current)

        # Goal reached
        if current == goal:

            path = reconstruct_path(
                parent,
                start,
                goal
            )

            return path, explored

        # Check neighboring cells
        for neighbor in get_neighbors(
            current,
            game_map
        ):

            new_g_cost = g_cost[current] + 1

            if (
                neighbor not in g_cost
                or new_g_cost < g_cost[neighbor]
            ):

                g_cost[neighbor] = new_g_cost

                h_cost = heuristic(
                    neighbor,
                    goal
                )

                f_cost = new_g_cost + h_cost

                parent[neighbor] = current

                heapq.heappush(
                    open_list,
                    (f_cost, neighbor)
                )

    return [], explored


# ============================================================
# TEST A*
# ============================================================

if __name__ == "__main__":

    test_map = [

        [0, 0, 0, 0, 1],

        [0, 1, 0, 0, 1],

        [0, 1, 0, 0, 0],

        [0, 0, 0, 1, 0],

        [1, 1, 0, 0, 0]
    ]

    start = (0, 0)

    goal = (4, 4)


    # --------------------------------------------------------
    # BFS
    # --------------------------------------------------------

    bfs_path, bfs_explored = bfs(
        test_map,
        start,
        goal
    )

    print("========== BFS ==========")

    print("Path:")
    print(bfs_path)

    print("Cells explored:")
    print(len(bfs_explored))


    # --------------------------------------------------------
    # DFS
    # --------------------------------------------------------

    dfs_path, dfs_explored = dfs(
        test_map,
        start,
        goal
    )

    print("\n========== DFS ==========")

    print("Path:")
    print(dfs_path)

    print("Cells explored:")
    print(len(dfs_explored))


    # --------------------------------------------------------
    # A*
    # --------------------------------------------------------

    astar_path, astar_explored = astar(
        test_map,
        start,
        goal
    )

    print("\n========== A* ==========")

    print("Path:")
    print(astar_path)

    print("Cells explored:")
    print(len(astar_explored))