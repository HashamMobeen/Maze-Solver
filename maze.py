"""
Maze Representation Module
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
