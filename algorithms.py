"""
Pathfinding Algorithms Module
<<<<<<< HEAD
Member 2: [Your Name]
=======
Member 2: Aoun Muhammad Azher
CMS ID: 509885
>>>>>>> fa7c126c5b4a8418e51529d5af9da68c18835938
Implements BFS, DFS, and A* with exploration tracking
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
