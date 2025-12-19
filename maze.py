"""Maze Representation Module
Member 1: Husnain Shakil
Handles maze data structure and validation
"""
import numpy as np

class Maze:
    def __init__(self):
        """Initialize empty maze with 2D array structure"""
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None
    
    def load_from_string(self, maze_string):
        """
        Load maze from multi-line string
        Format: # = wall, . = path, S = start, G = goal
        """
        lines = maze_string.strip().split('\n')
        self.grid = [list(line) for line in lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self._find_start_goal()
    
    def load_from_file(self, filename):
        """Load maze from text file"""
        with open(filename, 'r') as f:
            maze_string = f.read()
        self.load_from_string(maze_string)
    
    def _find_start_goal(self):
        """Scan grid to locate start and goal positions"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)
    
    def is_valid(self, row, col):
        """
        Check if cell is within bounds and walkable
        Used by pathfinding algorithms to validate neighbors
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] != '#'
        return False
    
    def get_neighbors(self, row, col):
        """
        Return valid neighboring cells (up, down, left, right)
        Graph edges in the maze representation
        """
        neighbors = []
        # Four cardinal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def export_for_matplotlib(self):
        """
        Export maze data for matplotlib chart generation
        Returns numeric grid for visualization
        """
        visual_grid = np.zeros((self.rows, self.cols))
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '#':
                    visual_grid[r][c] = 1
                elif self.grid[r][c] == 'S':
                    visual_grid[r][c] = 2
                elif self.grid[r][c] == 'G':
                    visual_grid[r][c] = 3
        
        return visual_grid
    
    def set_cell(self, row, col, value):
        """
        Set a cell value (for interactive editing)
        
        Args:
            row: Row index
            col: Column index
            value: '#' (wall), '.' (path), 'S' (start), 'G' (goal)
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            old_value = self.grid[row][col]
            self.grid[row][col] = value
            
            # Update start/goal references
            if value == 'S':
                # Clear old start if exists
                if self.start and self.start != (row, col):
                    old_r, old_c = self.start
                    if self.grid[old_r][old_c] == 'S':
                        self.grid[old_r][old_c] = '.'
                self.start = (row, col)
            elif value == 'G':
                # Clear old goal if exists
                if self.goal and self.goal != (row, col):
                    old_r, old_c = self.goal
                    if self.grid[old_r][old_c] == 'G':
                        self.grid[old_r][old_c] = '.'
                self.goal = (row, col)
            elif old_value == 'S':
                self.start = None
            elif old_value == 'G':
                self.goal = None
    
    def get_cell(self, row, col):
        """Get cell value at position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    
    def clear(self):
        """Clear all walls (keep borders, start, goal)"""
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if self.grid[r][c] not in ['S', 'G']:
                    self.grid[r][c] = '.'
    
    def to_string(self):
        """Export maze as string"""
        return '\n'.join([''.join(row) for row in self.grid])
    
    def get_neighbors_sorted(self, row, col, goal):
        """
        Return valid neighboring cells sorted by distance to goal (closest first)
        
        SORTING OPTIMIZATION: By exploring cells closer to the goal first,
        algorithms can find the path faster with fewer explored nodes.
        
        Args:
            row: Current row position
            col: Current column position
            goal: Tuple (goal_row, goal_col) - the target position
        
        Returns:
            List of (row, col) tuples sorted by Manhattan distance to goal
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid(new_row, new_col):
                # Calculate Manhattan distance to goal
                distance = abs(new_row - goal[0]) + abs(new_col - goal[1])
                neighbors.append((distance, (new_row, new_col)))
        
        # SORTING: Sort by distance (ascending - closest first)
        neighbors.sort(key=lambda x: x[0])
        
        # Return just the positions (without distances)
        return [pos for _, pos in neighbors]