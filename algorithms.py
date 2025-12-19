"""
Pathfinding Algorithms Module
Member 2: Aoun Muhammad Azher
CMS ID: 509885
Implements BFS, DFS, and A* with exploration tracking
Enhanced with step-by-step visualization support
"""

from collections import deque
import heapq
import time

def reconstruct_path(parent, start, goal):
    """
    Rebuild path from goal to start using parent pointers
    Returns list of (row, col) tuples
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path


def bfs(maze):
    """
    Breadth-First Search using Queue (FIFO)
    Guarantees shortest path in unweighted graphs
    Time: O(V + E), Space: O(V)
    Returns: (path, nodes_explored, runtime, explored_cells)
    """
    start_time = time.perf_counter()
    
    if not maze.start or not maze.goal:
        return None, 0, 0.0, set()
    
    # Queue for BFS - FIFO data structure
    queue = deque([maze.start])
    visited = {maze.start}  # Set for O(1) lookup
    parent = {maze.start: None}
    nodes_explored = 0
    explored_cells = set()  # Track all cells we visited for visualization
    
    while queue:
        current = queue.popleft()  # FIFO: remove from front
        nodes_explored += 1
        explored_cells.add(current)  # Add to exploration set
        
        # Goal check
        if current == maze.goal:
            path = reconstruct_path(parent, maze.start, maze.goal)
            runtime = time.perf_counter() - start_time
            return path, nodes_explored, runtime, explored_cells
        
        # Explore all neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    # No path found
    runtime = time.perf_counter() - start_time
    return None, nodes_explored, runtime, explored_cells


def dfs(maze):
    """
    Depth-First Search using Stack (LIFO)
    Does not guarantee shortest path
    Time: O(V + E), Space: O(V)
    Returns: (path, nodes_explored, runtime, explored_cells)
    """
    start_time = time.perf_counter()
    
    if not maze.start or not maze.goal:
        return None, 0, 0.0, set()
    
    # Stack for DFS - LIFO data structure
    stack = [maze.start]
    visited = {maze.start}
    parent = {maze.start: None}
    nodes_explored = 0
    explored_cells = set()  # Track exploration
    
    while stack:
        current = stack.pop()  # LIFO: remove from back
        nodes_explored += 1
        explored_cells.add(current)
        
        # Goal check
        if current == maze.goal:
            path = reconstruct_path(parent, maze.start, maze.goal)
            runtime = time.perf_counter() - start_time
            return path, nodes_explored, runtime, explored_cells
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    # No path found
    runtime = time.perf_counter() - start_time
    return None, nodes_explored, runtime, explored_cells


def manhattan_distance(pos1, pos2):
    """
    Manhattan distance heuristic for A*
    Admissible: never overestimates actual distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def a_star(maze):
    """
    A* Search using Priority Queue (Min-Heap) with heuristic
    Often finds shortest path faster than BFS
    Time: O(E log V), Space: O(V)
    Returns: (path, nodes_explored, runtime, explored_cells)
    """
    start_time = time.perf_counter()
    
    if not maze.start or not maze.goal:
        return None, 0, 0.0, set()
    
    # Priority queue: (f_score, counter, position)
    counter = 0
    heap = [(0, counter, maze.start)]
    
    g_score = {maze.start: 0}
    parent = {maze.start: None}
    visited = set()
    nodes_explored = 0
    explored_cells = set()  # Track exploration
    
    while heap:
        current_f, _, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        
        visited.add(current)
        nodes_explored += 1
        explored_cells.add(current)
        
        # Goal check
        if current == maze.goal:
            path = reconstruct_path(parent, maze.start, maze.goal)
            runtime = time.perf_counter() - start_time
            return path, nodes_explored, runtime, explored_cells
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor in visited:
                continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h_score = manhattan_distance(neighbor, maze.goal)
                f_score = tentative_g + h_score
                parent[neighbor] = current
                
                counter += 1
                heapq.heappush(heap, (f_score, counter, neighbor))
    
    # No path found
    runtime = time.perf_counter() - start_time
    return None, nodes_explored, runtime, explored_cells


# ============================================================
# SORTING OPTIMIZED ALGORITHMS
# ============================================================

def dfs_optimized(maze):
    """
    DFS with Sorting Optimization
    
    OPTIMIZATION: Neighbors are sorted by distance to goal.
    The stack is ordered so that cells CLOSEST to goal are explored FIRST.
    This significantly reduces the number of nodes explored.
    
    Time: O(V + E), Space: O(V)
    Returns: (path, nodes_explored, runtime, explored_cells)
    """
    start_time = time.perf_counter()
    
    if not maze.start or not maze.goal:
        return None, 0, 0.0, set()
    
    stack = [maze.start]
    visited = {maze.start}
    parent = {maze.start: None}
    nodes_explored = 0
    explored_cells = set()
    
    while stack:
        current = stack.pop()
        nodes_explored += 1
        explored_cells.add(current)
        
        if current == maze.goal:
            path = reconstruct_path(parent, maze.start, maze.goal)
            runtime = time.perf_counter() - start_time
            return path, nodes_explored, runtime, explored_cells
        
        # Get neighbors and calculate distances to goal
        neighbors = maze.get_neighbors(current[0], current[1])
        neighbors_with_distance = []
        
        for neighbor in neighbors:
            if neighbor not in visited:
                # SORTING: Calculate Manhattan distance to goal
                distance = abs(neighbor[0] - maze.goal[0]) + abs(neighbor[1] - maze.goal[1])
                neighbors_with_distance.append((distance, neighbor))
        
        # SORTING: Sort by distance DESCENDING (furthest first)
        # Because stack pops from END, closest cells will be popped first!
        neighbors_with_distance.sort(key=lambda x: x[0], reverse=True)
        
        for _, neighbor in neighbors_with_distance:
            visited.add(neighbor)
            parent[neighbor] = current
            stack.append(neighbor)
    
    runtime = time.perf_counter() - start_time
    return None, nodes_explored, runtime, explored_cells


def bfs_bidirectional(maze):
    """
    Bi-directional BFS - Searches from BOTH start AND goal simultaneously
    
    OPTIMIZATION: By searching from both ends and meeting in the middle,
    we explore roughly half the nodes compared to standard BFS.
    
    Time: O(V + E), Space: O(V)
    Returns: (path, nodes_explored, runtime, explored_cells)
    """
    start_time = time.perf_counter()
    
    if not maze.start or not maze.goal:
        return None, 0, 0.0, set()
    
    # Forward search (from start)
    forward_queue = deque([maze.start])
    forward_visited = {maze.start}
    forward_parent = {maze.start: None}
    
    # Backward search (from goal)
    backward_queue = deque([maze.goal])
    backward_visited = {maze.goal}
    backward_parent = {maze.goal: None}
    
    nodes_explored = 0
    explored_cells = set()
    meeting_point = None
    
    while forward_queue and backward_queue:
        # Expand forward search (one step)
        if forward_queue:
            current = forward_queue.popleft()
            nodes_explored += 1
            explored_cells.add(current)
            
            # Check if forward search met backward search
            if current in backward_visited:
                meeting_point = current
                break
            
            for neighbor in maze.get_neighbors(current[0], current[1]):
                if neighbor not in forward_visited:
                    forward_visited.add(neighbor)
                    forward_parent[neighbor] = current
                    forward_queue.append(neighbor)
                    
                    # Also check if this neighbor is in backward search
                    if neighbor in backward_visited:
                        meeting_point = neighbor
                        break
            
            if meeting_point:
                break
        
        # Expand backward search (one step)
        if backward_queue and not meeting_point:
            current = backward_queue.popleft()
            nodes_explored += 1
            explored_cells.add(current)
            
            # Check if backward search met forward search
            if current in forward_visited:
                meeting_point = current
                break
            
            for neighbor in maze.get_neighbors(current[0], current[1]):
                if neighbor not in backward_visited:
                    backward_visited.add(neighbor)
                    backward_parent[neighbor] = current
                    backward_queue.append(neighbor)
                    
                    # Also check if this neighbor is in forward search
                    if neighbor in forward_visited:
                        meeting_point = neighbor
                        break
            
            if meeting_point:
                break
    
    if meeting_point is None:
        runtime = time.perf_counter() - start_time
        return None, nodes_explored, runtime, explored_cells
    
    # Reconstruct path: start → meeting_point → goal
    # Part 1: Forward path (start to meeting point)
    path_forward = []
    current = meeting_point
    while current is not None:
        path_forward.append(current)
        current = forward_parent.get(current)
    path_forward.reverse()
    
    # Part 2: Backward path (meeting point to goal)
    path_backward = []
    current = backward_parent.get(meeting_point)  # Skip meeting point
    while current is not None:
        path_backward.append(current)
        current = backward_parent.get(current)
    
    full_path = path_forward + path_backward
    runtime = time.perf_counter() - start_time
    return full_path, nodes_explored, runtime, explored_cells


# ============================================================
# ANIMATED VERSIONS - Generator Functions for Step-by-Step UI
# ============================================================

def bfs_animated(maze):
    """
    BFS with step-by-step visualization
    Yields: (current_cell, explored_set, path_so_far, is_goal_reached)
    """
    if not maze.start or not maze.goal:
        return
    
    queue = deque([maze.start])
    visited = {maze.start}
    parent = {maze.start: None}
    explored_cells = set()
    
    while queue:
        current = queue.popleft()
        explored_cells.add(current)
        
        # Yield current state for visualization
        current_path = reconstruct_path(parent, maze.start, current)
        yield (current, explored_cells.copy(), current_path, False)
        
        # Check if goal reached
        if current == maze.goal:
            final_path = reconstruct_path(parent, maze.start, maze.goal)
            yield (current, explored_cells.copy(), final_path, True)
            return
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    # No path found
    yield (None, explored_cells.copy(), [], False)


def dfs_animated(maze):
    """
    DFS with step-by-step visualization
    Yields: (current_cell, explored_set, path_so_far, is_goal_reached)
    """
    if not maze.start or not maze.goal:
        return
    
    stack = [maze.start]
    visited = {maze.start}
    parent = {maze.start: None}
    explored_cells = set()
    
    while stack:
        current = stack.pop()
        explored_cells.add(current)
        
        # Yield current state for visualization
        current_path = reconstruct_path(parent, maze.start, current)
        yield (current, explored_cells.copy(), current_path, False)
        
        # Check if goal reached
        if current == maze.goal:
            final_path = reconstruct_path(parent, maze.start, maze.goal)
            yield (current, explored_cells.copy(), final_path, True)
            return
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    # No path found
    yield (None, explored_cells.copy(), [], False)


def a_star_animated(maze):
    """
    A* with step-by-step visualization
    Yields: (current_cell, explored_set, path_so_far, is_goal_reached)
    """
    if not maze.start or not maze.goal:
        return
    
    counter = 0
    heap = [(0, counter, maze.start)]
    g_score = {maze.start: 0}
    parent = {maze.start: None}
    visited = set()
    explored_cells = set()
    
    while heap:
        current_f, _, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        
        visited.add(current)
        explored_cells.add(current)
        
        # Yield current state for visualization
        current_path = reconstruct_path(parent, maze.start, current)
        yield (current, explored_cells.copy(), current_path, False)
        
        # Check if goal reached
        if current == maze.goal:
            final_path = reconstruct_path(parent, maze.start, maze.goal)
            yield (current, explored_cells.copy(), final_path, True)
            return
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor in visited:
                continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h_score = manhattan_distance(neighbor, maze.goal)
                f_score = tentative_g + h_score
                parent[neighbor] = current
                
                counter += 1
                heapq.heappush(heap, (f_score, counter, neighbor))
    
    # No path found
    yield (None, explored_cells.copy(), [], False)


# ============================================================
# ANIMATED VERSIONS OF OPTIMIZED ALGORITHMS
# ============================================================

def dfs_optimized_animated(maze):
    """
    DFS Optimized with step-by-step visualization
    
    SORTING OPTIMIZATION: Explores neighbors closest to goal first
    Yields: (current_cell, explored_set, path_so_far, is_goal_reached)
    """
    if not maze.start or not maze.goal:
        return
    
    stack = [maze.start]
    visited = {maze.start}
    parent = {maze.start: None}
    explored_cells = set()
    
    while stack:
        current = stack.pop()
        explored_cells.add(current)
        
        # Yield current state for visualization
        current_path = reconstruct_path(parent, maze.start, current)
        yield (current, explored_cells.copy(), current_path, False)
        
        if current == maze.goal:
            final_path = reconstruct_path(parent, maze.start, maze.goal)
            yield (current, explored_cells.copy(), final_path, True)
            return
        
        # Get neighbors with distances
        neighbors = maze.get_neighbors(current[0], current[1])
        neighbors_with_distance = []
        
        for neighbor in neighbors:
            if neighbor not in visited:
                distance = abs(neighbor[0] - maze.goal[0]) + abs(neighbor[1] - maze.goal[1])
                neighbors_with_distance.append((distance, neighbor))
        
        # SORTING: Descending order (closest popped first from stack)
        neighbors_with_distance.sort(key=lambda x: x[0], reverse=True)
        
        for _, neighbor in neighbors_with_distance:
            visited.add(neighbor)
            parent[neighbor] = current
            stack.append(neighbor)
    
    yield (None, explored_cells.copy(), [], False)


def bfs_bidirectional_animated(maze):
    """
    Bi-directional BFS with step-by-step visualization
    
    OPTIMIZATION: Searches from both start and goal, meeting in middle
    Yields: (current_cell, explored_set, path_so_far, is_goal_reached)
    """
    if not maze.start or not maze.goal:
        return
    
    # Forward search
    forward_queue = deque([maze.start])
    forward_visited = {maze.start}
    forward_parent = {maze.start: None}
    
    # Backward search
    backward_queue = deque([maze.goal])
    backward_visited = {maze.goal}
    backward_parent = {maze.goal: None}
    
    explored_cells = set()
    meeting_point = None
    is_forward_turn = True  # Alternate between forward and backward
    
    while forward_queue or backward_queue:
        if is_forward_turn and forward_queue:
            current = forward_queue.popleft()
            explored_cells.add(current)
            
            # Yield current state
            yield (current, explored_cells.copy(), [], False)
            
            if current in backward_visited:
                meeting_point = current
                break
            
            for neighbor in maze.get_neighbors(current[0], current[1]):
                if neighbor not in forward_visited:
                    forward_visited.add(neighbor)
                    forward_parent[neighbor] = current
                    forward_queue.append(neighbor)
                    
                    if neighbor in backward_visited:
                        meeting_point = neighbor
                        break
            
            if meeting_point:
                break
                
        elif not is_forward_turn and backward_queue:
            current = backward_queue.popleft()
            explored_cells.add(current)
            
            # Yield current state
            yield (current, explored_cells.copy(), [], False)
            
            if current in forward_visited:
                meeting_point = current
                break
            
            for neighbor in maze.get_neighbors(current[0], current[1]):
                if neighbor not in backward_visited:
                    backward_visited.add(neighbor)
                    backward_parent[neighbor] = current
                    backward_queue.append(neighbor)
                    
                    if neighbor in forward_visited:
                        meeting_point = neighbor
                        break
            
            if meeting_point:
                break
        
        is_forward_turn = not is_forward_turn  # Alternate
    
    if meeting_point is None:
        yield (None, explored_cells.copy(), [], False)
        return
    
    # Reconstruct full path
    path_forward = []
    current = meeting_point
    while current is not None:
        path_forward.append(current)
        current = forward_parent.get(current)
    path_forward.reverse()
    
    path_backward = []
    current = backward_parent.get(meeting_point)
    while current is not None:
        path_backward.append(current)
        current = backward_parent.get(current)
    
    full_path = path_forward + path_backward
    yield (meeting_point, explored_cells.copy(), full_path, True)
