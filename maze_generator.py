"""
Maze Generation Module
Provides algorithms to generate random and structured mazes
"""

import random


def generate_random_maze(rows, cols, wall_density=0.3):
    """
    Generate a random maze with specified wall density
    
    Args:
        rows: Number of rows
        cols: Number of columns
        wall_density: Percentage of walls (0.0 to 1.0)
    
    Returns:
        2D grid with walls (#), paths (.), start (S), and goal (G)
    """
    # Create empty grid
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Add border walls
    for r in range(rows):
        grid[r][0] = '#'
        grid[r][cols - 1] = '#'
    for c in range(cols):
        grid[0][c] = '#'
        grid[rows - 1][c] = '#'
    
    # Add random walls inside
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if random.random() < wall_density:
                grid[r][c] = '#'
    
    # Place start and goal
    # Start in top-left area
    grid[1][1] = 'S'
    
    # Goal in bottom-right area
    grid[rows - 2][cols - 2] = 'G'
    
    return grid


def generate_recursive_backtracking(rows, cols):
    """
    Generate maze using recursive backtracking algorithm
    Creates a perfect maze (no loops, single solution path)
    
    Args:
        rows: Number of rows (should be odd)
        cols: Number of columns (should be odd)
    
    Returns:
        2D grid with maze structure
    """
    # Ensure odd dimensions for proper maze structure
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1
    
    # Start with all walls
    grid = [['#' for _ in range(cols)] for _ in range(rows)]
    
    # Carve passages
    def carve_passages(r, c):
        """Recursive function to carve paths"""
        grid[r][c] = '.'
        
        # Define directions: up, down, left, right
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            
            # Check if new position is valid and unvisited
            if (1 <= new_r < rows - 1 and 
                1 <= new_c < cols - 1 and 
                grid[new_r][new_c] == '#'):
                
                # Carve through the wall between cells
                grid[r + dr // 2][c + dc // 2] = '.'
                carve_passages(new_r, new_c)
    
    # Start carving from position (1, 1)
    carve_passages(1, 1)
    
    # Place start and goal
    grid[1][1] = 'S'
    
    # Find a good goal position (far from start)
    # Try bottom-right area
    for r in range(rows - 2, 0, -1):
        for c in range(cols - 2, 0, -1):
            if grid[r][c] == '.':
                grid[r][c] = 'G'
                return grid
    
    # Fallback: place goal at any open space
    for r in range(rows - 2, 0, -1):
        for c in range(cols - 2, 0, -1):
            if grid[r][c] == '.':
                grid[r][c] = 'G'
                break
    
    return grid


def grid_to_string(grid):
    """Convert 2D grid to string format for Maze class"""
    return '\n'.join([''.join(row) for row in grid])


def generate_empty_maze(rows, cols):
    """
    Generate an empty maze (no walls except borders)
    Useful for custom maze editing
    
    Args:
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        2D grid with only border walls
    """
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Add border walls
    for r in range(rows):
        grid[r][0] = '#'
        grid[r][cols - 1] = '#'
    for c in range(cols):
        grid[0][c] = '#'
        grid[rows - 1][c] = '#'
    
    # Place start and goal
    grid[1][1] = 'S'
    grid[rows - 2][cols - 2] = 'G'
    
    return grid

