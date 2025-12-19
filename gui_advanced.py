"""
ADVANCED MAZE PATHFINDER - Enhanced UI
Features:
- Animated step-by-step visualization
- Interactive maze editing
- Maze generation (random, recursive backtracking)
- Speed control slider
- Dark mode toggle
- Real-time statistics
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from maze import Maze
from algorithms import (
    bfs, dfs, a_star, 
    bfs_animated, dfs_animated, a_star_animated,
    dfs_optimized, bfs_bidirectional,
    dfs_optimized_animated, bfs_bidirectional_animated
)
from analysis import compare_all_algorithms, show_runtime_graph
from maze_generator import (
    generate_random_maze, 
    generate_recursive_backtracking, 
    generate_empty_maze,
    grid_to_string
)
import time


class MazePathfinderAdvanced:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Maze Pathfinder")
        self.root.geometry("1400x800")
        
        # Core data
        self.maze = None
        self.animation_generator = None
        self.animation_running = False
        self.animation_id = None
        
        # UI State
        self.dark_mode = False
        self.edit_mode = False
        self.selected_algorithm = "BFS"
        self.animation_speed = 50  # milliseconds per step
        self.cell_size = 20
        self.separator_frames = []
        self.legend_color_boxes = []
        
        # Statistics
        self.stats = {
            'algorithm': 'None',
            'nodes_explored': 0,
            'path_length': 0,
            'execution_time': 0.0,
            'status': 'Ready'
        }
        
        # Color schemes
        self.color_schemes = {
            'light': {
                'bg': '#ECF0F1',
                'panel_bg': '#FFFFFF',
                'title_bg': '#2C3E50',
                'title_fg': '#FFFFFF',
                'wall': '#34495E',
                'path': '#FFFFFF',
                'start': '#F39C12',
                'goal': '#E74C3C',
                'explored': '#85C1E9',
                'solution': '#58D68D',
                'current': '#FFD700',
                'grid_line': '#BDC3C7',
                'text': '#2C3E50',
                'button_bg': '#3498DB',
                'button_fg': '#FFFFFF'
            },
            'dark': {
                'bg': '#000000',
                'panel_bg': '#0D1117',
                'title_bg': '#010409',
                'title_fg': '#F0F6FC',
                'wall': '#3D444D',
                'path': '#0D1117',
                'start': '#F0883E',
                'goal': '#F85149',
                'explored': '#388BFD',
                'solution': '#3FB950',
                'current': '#D29922',
                'grid_line': '#21262D',
                'text': '#E6EDF3',
                'button_bg': '#238636',
                'button_fg': '#FFFFFF'
            }
        }
        
        self.colors = self.color_schemes['light']
        
        # Build UI
        self.create_ui()
        
        # Load default maze
        self.load_default_maze()
    
    def create_ui(self):
        """Create the main user interface"""
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Title bar
        self.create_title_bar()
        
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Left panel (controls)
        self.create_left_panel(self.main_container)
        
        # Center panel (maze canvas)
        self.create_center_panel(self.main_container)
        
        # Right panel (statistics & legend)
        self.create_right_panel(self.main_container)
        
        # Bottom status bar
        self.create_status_bar()
    
    def create_title_bar(self):
        """Create top title bar with dark mode toggle"""
        self.title_frame = tk.Frame(self.root, bg=self.colors['title_bg'], height=70)
        self.title_frame.pack(fill=tk.X)
        self.title_frame.pack_propagate(False)
        
        # Title label
        self.title_label = tk.Label(
            self.title_frame,
            text="🔍 MAZE PATHFINDER",
            font=('Arial', 24, 'bold'),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg']
        )
        self.title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Dark mode toggle button
        self.dark_mode_btn = tk.Button(
            self.title_frame,
            text="🌙 Dark Mode",
            command=self.toggle_dark_mode,
            font=('Arial', 11, 'bold'),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            cursor='hand2',
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.dark_mode_btn.pack(side=tk.RIGHT, padx=20, pady=15)
    
    def create_left_panel(self, parent):
        """Create left control panel with scrolling support"""
        self.left_frame = tk.Frame(parent, bg=self.colors['panel_bg'], width=320)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        self.left_frame.pack_propagate(False)
        
        # Create canvas with scrollbar for scrollable content
        self.left_canvas = tk.Canvas(
            self.left_frame,
            bg=self.colors['panel_bg'],
            highlightthickness=0,
            bd=0
        )
        self.left_scrollbar = tk.Scrollbar(
            self.left_frame,
            orient=tk.VERTICAL,
            command=self.left_canvas.yview
        )
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)
        
        # Pack scrollbar and canvas
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create interior frame for content
        self.left_content = tk.Frame(self.left_canvas, bg=self.colors['panel_bg'])
        self.left_canvas_window = self.left_canvas.create_window(
            (0, 0),
            window=self.left_content,
            anchor='nw'
        )
        
        # Bind events to update scroll region and canvas width
        self.left_content.bind('<Configure>', self._on_left_content_configure)
        self.left_canvas.bind('<Configure>', self._on_left_canvas_configure)
        
        # Bind mousewheel scrolling for left panel
        self.left_canvas.bind('<Enter>', self._bind_left_panel_mousewheel)
        self.left_canvas.bind('<Leave>', self._unbind_left_panel_mousewheel)
        
        # Add padding frame inside left_content
        self.left_inner = tk.Frame(self.left_content, bg=self.colors['panel_bg'])
        self.left_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Algorithm Selection
        self.create_section_label(self.left_inner, "🎯 ALGORITHM SELECTION")
        
        self.algorithm_var = tk.StringVar(value="BFS")
        algorithms = [
            ("BFS - Breadth First", "BFS"), 
            ("DFS - Depth First", "DFS"), 
            ("A* - Heuristic", "A*"),
            ("DFS Optimized - Sorted", "DFS_OPT"),
            ("Bi-directional BFS", "BFS_BI")
        ]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(
                self.left_inner,
                text=text,
                variable=self.algorithm_var,
                value=value,
                font=('Arial', 10),
                bg=self.colors['panel_bg'],
                fg=self.colors['text'],
                selectcolor=self.colors['bg'],
                activebackground=self.colors['panel_bg'],
                cursor='hand2'
            )
            rb.pack(anchor=tk.W, pady=3)
        
        self.add_separator(self.left_inner)
        
        # Speed Control
        self.create_section_label(self.left_inner, "⚡ ANIMATION SPEED")
        
        speed_frame = tk.Frame(self.left_inner, bg=self.colors['panel_bg'])
        speed_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            speed_frame,
            text="Slow",
            font=('Arial', 9),
            bg=self.colors['panel_bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.speed_slider = tk.Scale(
            speed_frame,
            from_=1,
            to=200,
            orient=tk.HORIZONTAL,
            showvalue=False,
            bg=self.colors['panel_bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['bg']
        )
        self.speed_slider.set(50)
        self.speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(
            speed_frame,
            text="Fast",
            font=('Arial', 9),
            bg=self.colors['panel_bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.add_separator(self.left_inner)
        
        # Control Buttons
        self.create_section_label(self.left_inner, "🎮 CONTROLS")
        
        btn_config = {
            'font': ('Arial', 11, 'bold'),
            'cursor': 'hand2',
            'relief': tk.FLAT,
            'height': 2
        }
        
        self.run_btn = tk.Button(
            self.left_inner,
            text="▶ RUN ALGORITHM",
            command=self.run_animation,
            bg='#27AE60',
            fg='white',
            **btn_config
        )
        self.run_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(
            self.left_inner,
            text="⏸ STOP",
            command=self.stop_animation,
            bg='#E74C3C',
            fg='white',
            state=tk.DISABLED,
            **btn_config
        )
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        self.reset_btn = tk.Button(
            self.left_inner,
            text="🔄 RESET",
            command=self.reset_maze,
            bg='#F39C12',
            fg='white',
            **btn_config
        )
        self.reset_btn.pack(fill=tk.X, pady=5)
        
        # Compare Algorithms button
        self.compare_btn = tk.Button(
            self.left_inner,
            text="📊 COMPARE ALGORITHMS",
            command=self.compare_algorithms,
            bg='#9B59B6',
            fg='white',
            **btn_config
        )
        self.compare_btn.pack(fill=tk.X, pady=5)
        
        self.add_separator(self.left_inner)
        
        # Maze Generation
        self.create_section_label(self.left_inner, "🎲 MAZE GENERATION")
        
        gen_btn_config = {
            'font': ('Arial', 10, 'bold'),
            'cursor': 'hand2',
            'relief': tk.FLAT,
            'height': 2,
            'fg': 'white'
        }
        
        tk.Button(
            self.left_inner,
            text="🎲 Random Maze",
            command=self.generate_random,
            bg='#8E44AD',
            **gen_btn_config
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            self.left_inner,
            text="🌀 Recursive Backtracking",
            command=self.generate_recursive,
            bg='#2980B9',
            **gen_btn_config
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            self.left_inner,
            text="📄 Empty Maze",
            command=self.generate_empty,
            bg='#95A5A6',
            **gen_btn_config
        ).pack(fill=tk.X, pady=3)
        
        self.add_separator(self.left_inner)
        
        # Edit Mode
        self.create_section_label(self.left_inner, "✏️ EDIT MODE")
        
        self.edit_mode_var = tk.BooleanVar(value=False)
        self.edit_check = tk.Checkbutton(
            self.left_inner,
            text="Enable Maze Editing",
            variable=self.edit_mode_var,
            command=self.toggle_edit_mode,
            font=('Arial', 10, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['bg'],
            activebackground=self.colors['panel_bg'],
            cursor='hand2'
        )
        self.edit_check.pack(anchor=tk.W, pady=5)
        
        edit_info = tk.Label(
            self.left_inner,
            text="Left Click: Toggle Wall\nRight Click: Set Start/Goal",
            font=('Arial', 9),
            bg=self.colors['panel_bg'],
            fg=self.colors['text'],
            justify=tk.LEFT
        )
        edit_info.pack(anchor=tk.W, pady=5)
        
        self.add_separator(self.left_inner)
        
        # File Operations
        self.create_section_label(self.left_inner, "📁 FILE OPERATIONS")
        
        file_btn_config = {
            'font': ('Arial', 10),
            'cursor': 'hand2',
            'relief': tk.FLAT,
            'height': 2,
            'fg': 'white',
            'bg': '#16A085'
        }
        
        tk.Button(
            self.left_inner,
            text="📂 Load Maze",
            command=self.load_from_file,
            **file_btn_config
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            self.left_inner,
            text="💾 Save Maze",
            command=self.save_to_file,
            **file_btn_config
        ).pack(fill=tk.X, pady=3)
    
    def create_center_panel(self, parent):
        """Create center maze canvas panel"""
        self.center_frame = tk.Frame(parent, bg=self.colors['panel_bg'])
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Info label
        self.info_label = tk.Label(
            self.center_frame,
            text="Current Maze: Default (15×15)",
            font=('Arial', 12, 'bold'),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            pady=10
        )
        self.info_label.pack(fill=tk.X)
        
        # Canvas with scrollbars
        self.canvas_frame = tk.Frame(self.center_frame, bg=self.colors['bg'])
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg=self.colors['path'],
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set,
            highlightthickness=0,
            highlightbackground=self.colors['grid_line'],
            bd=0
        )
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)
        
        # Pack
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events for editing
        self.canvas.bind('<Button-1>', self.on_canvas_left_click)
        self.canvas.bind('<Button-3>', self.on_canvas_right_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<Enter>', self._bind_canvas_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_canvas_mousewheel)
    
    def create_right_panel(self, parent):
        """Create right panel with statistics and legend"""
        self.right_frame = tk.Frame(parent, bg=self.colors['panel_bg'], width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)
        
        # Statistics Section
        self.stats_header = tk.Label(
            self.right_frame,
            text="📊 STATISTICS",
            font=('Arial', 12, 'bold'),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            pady=10
        )
        self.stats_header.pack(fill=tk.X)
        
        # Stats content
        stats_content = tk.Frame(self.right_frame, bg=self.colors['panel_bg'])
        stats_content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Create stat labels
        self.stat_labels = {}
        
        stats_info = [
            ('Algorithm', 'algorithm', 'None'),
            ('Status', 'status', 'Ready'),
            ('Nodes Explored', 'nodes_explored', '0'),
            ('Path Length', 'path_length', '0'),
            ('Execution Time', 'execution_time', '0.000 ms')
        ]
        
        for label, key, default in stats_info:
            frame = tk.Frame(stats_content, bg=self.colors['panel_bg'])
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                frame,
                text=f"{label}:",
                font=('Arial', 10, 'bold'),
                bg=self.colors['panel_bg'],
                fg=self.colors['text'],
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text=default,
                font=('Arial', 10),
                bg=self.colors['panel_bg'],
                fg=self.colors['button_bg'],
                anchor=tk.E
            )
            value_label.pack(side=tk.RIGHT)
            
            self.stat_labels[key] = value_label
        
        # Separator
        sep = tk.Frame(
            self.right_frame,
            height=2,
            bg=self.colors['grid_line']
        )
        sep.pack(fill=tk.X, padx=15, pady=10)
        self.separator_frames.append(sep)
        
        # Legend Section
        self.legend_header = tk.Label(
            self.right_frame,
            text="🎨 LEGEND",
            font=('Arial', 12, 'bold'),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            pady=10
        )
        self.legend_header.pack(fill=tk.X)
        
        # Legend content
        legend_content = tk.Frame(self.right_frame, bg=self.colors['panel_bg'])
        legend_content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        legend_items = [
            ('Wall', 'wall'),
            ('Path', 'path'),
            ('Start', 'start'),
            ('Goal', 'goal'),
            ('Explored', 'explored'),
            ('Solution', 'solution'),
            ('Current', 'current')
        ]
        
        for text, color_key in legend_items:
            frame = tk.Frame(legend_content, bg=self.colors['panel_bg'])
            frame.pack(fill=tk.X, pady=5)
            
            # Color box
            color_box = tk.Label(
                frame,
                text="  ",
                bg=self.colors[color_key],
                width=3,
                relief=tk.SOLID,
                borderwidth=1
            )
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            self.legend_color_boxes.append((color_box, color_key))
            
            # Text
            tk.Label(
                frame,
                text=text,
                font=('Arial', 10),
                bg=self.colors['panel_bg'],
                fg=self.colors['text'],
                anchor=tk.W
            ).pack(side=tk.LEFT)
    
    def create_status_bar(self):
        """Create bottom status bar"""
        self.status_frame = tk.Frame(self.root, bg=self.colors['title_bg'], height=35)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_text = tk.Label(
            self.status_frame,
            text="Ready | Load a maze or generate one to begin",
            font=('Arial', 10),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            anchor=tk.W
        )
        self.status_text.pack(side=tk.LEFT, padx=15, pady=5)
    
    def create_section_label(self, parent, text):
        """Helper to create section labels"""
        label = tk.Label(
            parent,
            text=text,
            font=('Arial', 11, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['text'],
            anchor=tk.W
        )
        label.pack(fill=tk.X, pady=(10, 5))
        return label
    
    def add_separator(self, parent):
        """Helper to add horizontal separator"""
        sep = tk.Frame(
            parent,
            height=2,
            bg=self.colors['grid_line']
        )
        sep.pack(fill=tk.X, pady=15)
        self.separator_frames.append(sep)
    
    # ========== MAZE RENDERING ==========
    
    def draw_maze(self, explored=None, path=None, current=None):
        """Draw the maze on canvas"""
        self.canvas.delete("all")
        if not self.maze:
            return
        
        width = self.maze.cols * self.cell_size
        height = self.maze.rows * self.cell_size
        self.canvas.config(scrollregion=(0, 0, width, height))
        
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                cell = self.maze.grid[r][c]
                color = self.colors['path']
                
                # Determine cell color
                if cell == '#':
                    color = self.colors['wall']
                elif cell == 'S':
                    color = self.colors['start']
                elif cell == 'G':
                    color = self.colors['goal']
                
                # Override with exploration/path colors
                if explored and (r, c) in explored and cell not in ['S', 'G']:
                    color = self.colors['explored']
                
                if path and (r, c) in path and cell not in ['S', 'G']:
                    color = self.colors['solution']
                
                if current and current == (r, c) and cell not in ['S', 'G']:
                    color = self.colors['current']
                
                # Draw cell
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=self.colors['grid_line'],
                    width=1
                )
    
    def _bind_canvas_mousewheel(self, event=None):
        """Enable mouse wheel scrolling when pointer is over the canvas"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)
    
    def _unbind_canvas_mousewheel(self, event=None):
        """Disable mouse wheel scrolling when pointer leaves the canvas"""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")
    
    def _on_mousewheel(self, event):
        """Scroll vertically with the mouse wheel"""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_shift_mousewheel(self, event):
        """Scroll horizontally when holding Shift + wheel"""
        if self.canvas.winfo_exists():
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    # ========== LEFT PANEL SCROLLING ==========
    
    def _on_left_content_configure(self, event):
        """Update scroll region when left panel content changes size"""
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
    
    def _on_left_canvas_configure(self, event):
        """Update inner frame width when left canvas is resized"""
        canvas_width = event.width
        self.left_canvas.itemconfig(self.left_canvas_window, width=canvas_width)
    
    def _bind_left_panel_mousewheel(self, event=None):
        """Enable mouse wheel scrolling for left panel"""
        self.left_canvas.bind_all("<MouseWheel>", self._on_left_panel_mousewheel)
    
    def _unbind_left_panel_mousewheel(self, event=None):
        """Disable mouse wheel scrolling for left panel"""
        self.left_canvas.unbind_all("<MouseWheel>")
    
    def _on_left_panel_mousewheel(self, event):
        """Scroll left panel vertically with mouse wheel"""
        if self.left_canvas.winfo_exists():
            self.left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    # ========== ANIMATION CONTROL ==========
    
    def run_animation(self):
        """Start the pathfinding animation"""
        if self.animation_running:
            return
        
        if not self.maze or not self.maze.start or not self.maze.goal:
            messagebox.showwarning("Warning", "Please ensure maze has Start and Goal!")
            return
        
        # Get selected algorithm
        algo_name = self.algorithm_var.get()
        
        algo_map = {
            'BFS': bfs_animated,
            'DFS': dfs_animated,
            'A*': a_star_animated,
            'DFS_OPT': dfs_optimized_animated,
            'BFS_BI': bfs_bidirectional_animated
        }
        
        algo_func = algo_map[algo_name]
        
        # Initialize animation
        self.animation_running = True
        self.animation_generator = algo_func(self.maze)
        self.animation_start_time = time.perf_counter()
        
        # Update UI state
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.edit_check.config(state=tk.DISABLED)
        
        # Update stats
        self.stats['algorithm'] = algo_name
        self.stats['status'] = 'Running...'
        self.stats['nodes_explored'] = 0
        self.stats['path_length'] = 0
        self.update_stats_display()
        
        self.update_status(f"Running {algo_name}...")
        
        # Start animation loop
        self.animate_step()
    
    def animate_step(self):
        """Execute one step of the animation"""
        if not self.animation_running:
            return
        
        try:
            # Get next step from generator
            current, explored, path, is_goal = next(self.animation_generator)
            
            # Update statistics
            self.stats['nodes_explored'] = len(explored)
            self.stats['path_length'] = len(path) if path else 0
            elapsed = time.perf_counter() - self.animation_start_time
            self.stats['execution_time'] = elapsed * 1000  # Convert to ms
            self.update_stats_display()
            
            # Draw current state
            self.draw_maze(explored=explored, path=path, current=current)
            
            # Check if goal reached
            if is_goal:
                self.animation_complete(success=True, path=path)
                return
            
            # Schedule next step
            delay = 201 - self.speed_slider.get()  # Invert so right is faster
            self.animation_id = self.root.after(delay, self.animate_step)
            
        except StopIteration:
            # No more steps - path not found
            self.animation_complete(success=False)
    
    def animation_complete(self, success=True, path=None):
        """Handle animation completion"""
        self.animation_running = False
        self.animation_generator = None
        
        # Update UI state
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.edit_check.config(state=tk.NORMAL)
        
        if success:
            self.stats['status'] = '✅ Success!'
            self.update_status(f"Path found! Length: {len(path)}")
        else:
            self.stats['status'] = '❌ No Path'
            self.update_status("No path found")
        
        self.update_stats_display()
    
    def stop_animation(self):
        """Stop the running animation"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        self.animation_running = False
        self.animation_generator = None
        
        # Update UI state
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.edit_check.config(state=tk.NORMAL)
        
        self.stats['status'] = 'Stopped'
        self.update_stats_display()
        self.update_status("Animation stopped by user")
    
    def reset_maze(self):
        """Reset the maze to initial state"""
        self.stop_animation()
        
        if self.maze:
            self.draw_maze()
            self.stats = {
                'algorithm': 'None',
                'nodes_explored': 0,
                'path_length': 0,
                'execution_time': 0.0,
                'status': 'Ready'
            }
            self.update_stats_display()
            self.update_status("Maze reset")
    
    # ========== MAZE GENERATION ==========
    
    def generate_random(self):
        """Generate random maze"""
        self.stop_animation()
        grid = generate_random_maze(25, 25, wall_density=0.3)
        maze_string = grid_to_string(grid)
        self.load_maze_from_string(maze_string, "Random Maze (25×25)")
        self.update_status("Generated random maze")
    
    def generate_recursive(self):
        """Generate maze using recursive backtracking"""
        self.stop_animation()
        grid = generate_recursive_backtracking(25, 25)
        maze_string = grid_to_string(grid)
        self.load_maze_from_string(maze_string, "Recursive Maze (25×25)")
        self.update_status("Generated recursive backtracking maze")
    
    def generate_empty(self):
        """Generate empty maze for editing"""
        self.stop_animation()
        grid = generate_empty_maze(25, 25)
        maze_string = grid_to_string(grid)
        self.load_maze_from_string(maze_string, "Empty Maze (25×25)")
        self.update_status("Generated empty maze - ready for editing")
    
    # ========== MAZE LOADING ==========
    
    def load_default_maze(self):
        """Load a default maze"""
        default_maze = """###############
#S............#
#.###.#####.#.#
#.#.#.....#.#.#
#.#.#####.#.#.#
#.#.......#.#.#
#.###########.#
#.............#
#.#########.###
#.#.......#...#
#.#.#####.###.#
#.#.#...#.....#
#.#.#.#.#####.#
#.....#.....#G#
###############"""
        self.load_maze_from_string(default_maze, "Default (15×15)")
    
    def load_maze_from_string(self, maze_string, name):
        """Load maze from string"""
        self.maze = Maze()
        self.maze.load_from_string(maze_string)
        self.info_label.config(text=f"Current Maze: {name}")
        self.draw_maze()
        self.reset_stats()
    
    def load_from_file(self):
        """Load maze from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    maze_string = f.read()
                import os
                name = os.path.basename(filename)
                self.load_maze_from_string(maze_string, name)
                self.update_status(f"Loaded maze from {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load maze:\n{str(e)}")
    
    def save_to_file(self):
        """Save current maze to file"""
        if not self.maze:
            messagebox.showwarning("Warning", "No maze to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.maze.to_string())
                self.update_status(f"Saved maze to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save maze:\n{str(e)}")
    
    # ========== INTERACTIVE EDITING ==========
    
    def toggle_edit_mode(self):
        """Toggle edit mode on/off"""
        self.edit_mode = self.edit_mode_var.get()
        if self.edit_mode:
            self.update_status("Edit Mode: ON | Left Click: Wall | Right Click: Start/Goal")
        else:
            self.update_status("Edit Mode: OFF")
    
    def on_canvas_left_click(self, event):
        """Handle left click on canvas - toggle walls"""
        if not self.edit_mode or not self.maze:
            return
        
        # Convert canvas coordinates to grid coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        col = int(canvas_x // self.cell_size)
        row = int(canvas_y // self.cell_size)
        
        if 0 <= row < self.maze.rows and 0 <= col < self.maze.cols:
            current = self.maze.get_cell(row, col)
            
            # Don't allow editing borders, start, or goal with left click
            if current in ['S', 'G'] or row == 0 or row == self.maze.rows - 1 or col == 0 or col == self.maze.cols - 1:
                return
            
            # Toggle between wall and path
            new_value = '#' if current == '.' else '.'
            self.maze.set_cell(row, col, new_value)
            self.draw_maze()
    
    def on_canvas_right_click(self, event):
        """Handle right click on canvas - place start/goal"""
        if not self.edit_mode or not self.maze:
            return
        
        # Convert canvas coordinates to grid coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        col = int(canvas_x // self.cell_size)
        row = int(canvas_y // self.cell_size)
        
        if 0 <= row < self.maze.rows and 0 <= col < self.maze.cols:
            current = self.maze.get_cell(row, col)
            
            # Don't allow on walls or borders
            if current == '#' or row == 0 or row == self.maze.rows - 1 or col == 0 or col == self.maze.cols - 1:
                return
            
            # Cycle: . -> S -> G -> .
            if current == '.':
                self.maze.set_cell(row, col, 'S')
            elif current == 'S':
                self.maze.set_cell(row, col, 'G')
            elif current == 'G':
                self.maze.set_cell(row, col, '.')
            
            self.draw_maze()
    
    def on_canvas_drag(self, event):
        """Handle dragging on canvas - continuous wall drawing"""
        if not self.edit_mode or not self.maze:
            return
        
        self.on_canvas_left_click(event)
    
    # ========== DARK MODE ==========
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        
        # Switch color scheme
        self.colors = self.color_schemes['dark' if self.dark_mode else 'light']
        
        # Update button text
        self.dark_mode_btn.config(text="☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        
        # Refresh entire UI
        self.refresh_colors()
        
        # Redraw maze
        self.draw_maze()
        
        self.update_status(f"{'Dark' if self.dark_mode else 'Light'} mode activated")
    
    def refresh_colors(self):
        """Refresh all UI colors after theme change"""
        self.root.configure(bg=self.colors['bg'])
        self.main_container.configure(bg=self.colors['bg'])
        
        # Title & status areas
        self.title_frame.configure(bg=self.colors['title_bg'])
        self.status_frame.configure(bg=self.colors['title_bg'])
        self.title_label.configure(bg=self.colors['title_bg'], fg=self.colors['title_fg'])
        self.info_label.configure(bg=self.colors['title_bg'], fg=self.colors['title_fg'])
        self.status_text.configure(bg=self.colors['title_bg'], fg=self.colors['title_fg'])
        self.dark_mode_btn.configure(
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_bg'],
            activeforeground=self.colors['button_fg']
        )
        
        # Panels & canvas container
        for frame in [self.left_frame, self.left_content, self.left_inner, self.center_frame, self.right_frame]:
            frame.configure(bg=self.colors['panel_bg'])
        self.canvas_frame.configure(bg=self.colors['bg'])
        
        # Left panel canvas and scrollbar
        self.left_canvas.configure(bg=self.colors['panel_bg'])
        self.left_scrollbar.configure(
            bg=self.colors['panel_bg'],
            activebackground=self.colors['panel_bg'],
            troughcolor=self.colors['bg'],
            highlightthickness=0
        )
        
        # Scrollbars and canvas
        self.canvas.configure(bg=self.colors['path'], highlightbackground=self.colors['grid_line'])
        self.v_scroll.configure(
            bg=self.colors['panel_bg'],
            activebackground=self.colors['panel_bg'],
            troughcolor=self.colors['bg'],
            highlightthickness=0
        )
        self.h_scroll.configure(
            bg=self.colors['panel_bg'],
            activebackground=self.colors['panel_bg'],
            troughcolor=self.colors['bg'],
            highlightthickness=0
        )
        
        # Stats header, legend header, separators and legend swatches
        self.stats_header.configure(bg=self.colors['title_bg'], fg=self.colors['title_fg'])
        self.legend_header.configure(bg=self.colors['title_bg'], fg=self.colors['title_fg'])
        for sep in self.separator_frames:
            sep.configure(bg=self.colors['grid_line'])
        for widget, color_key in self.legend_color_boxes:
            widget.configure(bg=self.colors[color_key])
        for label in self.stat_labels.values():
            label.configure(bg=self.colors['panel_bg'], fg=self.colors['button_bg'])
        
        # Propagate to remaining children (labels, radio buttons, etc.)
        for container in [self.left_frame, self.right_frame, self.center_frame]:
            self._apply_theme_recursive(container)
        
        # Redraw maze so cells use updated palette
        self.draw_maze()
    
    def _apply_theme_recursive(self, widget):
        """Recursively apply palette to supported widget types"""
        for child in widget.winfo_children():
            if child in (self.title_label, self.info_label, self.status_text, self.dark_mode_btn):
                continue
            if child in (getattr(self, "stats_header", None), getattr(self, "legend_header", None)):
                continue
            if child in self.stat_labels.values():
                continue
            if any(child is swatch for swatch, _ in self.legend_color_boxes):
                continue
            
            if isinstance(child, tk.Frame):
                if child in self.separator_frames:
                    child.configure(bg=self.colors['grid_line'])
                elif child == self.canvas_frame:
                    child.configure(bg=self.colors['bg'])
                else:
                    child.configure(bg=self.colors['panel_bg'])
            elif isinstance(child, tk.Label):
                child.configure(bg=self.colors['panel_bg'], fg=self.colors['text'])
            elif isinstance(child, (tk.Radiobutton, tk.Checkbutton)):
                child.configure(
                    bg=self.colors['panel_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['panel_bg'],
                    activeforeground=self.colors['text']
                )
            elif isinstance(child, tk.Scale):
                child.configure(
                    bg=self.colors['panel_bg'],
                    fg=self.colors['text'],
                    troughcolor=self.colors['bg'],
                    highlightthickness=0
                )
            elif isinstance(child, tk.Scrollbar):
                child.configure(
                    bg=self.colors['panel_bg'],
                    activebackground=self.colors['panel_bg'],
                    troughcolor=self.colors['bg'],
                    highlightthickness=0
                )
            elif isinstance(child, tk.Canvas):
                # Left panel canvas uses panel_bg, maze canvas uses path color
                if child == self.left_canvas:
                    child.configure(bg=self.colors['panel_bg'])
                else:
                    child.configure(
                        bg=self.colors['path'],
                        highlightbackground=self.colors['grid_line']
                    )
            
            self._apply_theme_recursive(child)
    
    # ========== HELPERS ==========
    
    def update_stats_display(self):
        """Update statistics display"""
        self.stat_labels['algorithm'].config(text=self.stats['algorithm'])
        self.stat_labels['status'].config(text=self.stats['status'])
        self.stat_labels['nodes_explored'].config(text=str(self.stats['nodes_explored']))
        self.stat_labels['path_length'].config(text=str(self.stats['path_length']))
        self.stat_labels['execution_time'].config(text=f"{self.stats['execution_time']:.3f} ms")
    
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'algorithm': 'None',
            'nodes_explored': 0,
            'path_length': 0,
            'execution_time': 0.0,
            'status': 'Ready'
        }
        self.update_stats_display()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_text.config(text=message)
    
    # ========== ALGORITHM COMPARISON ==========
    
    def compare_algorithms(self):
        """
        Compare BFS, DFS, and A* algorithms on the current maze
        Runs algorithms sequentially and displays results in a table
        """
        # Validation: Check if maze is loaded and has start/goal
        if not self.maze or not self.maze.start or not self.maze.goal:
            messagebox.showwarning("Warning", "Please ensure maze has Start and Goal positions!")
            return
        
        # Stop any running animation
        self.stop_animation()
        
        # Update status
        self.update_status("Comparing algorithms... Please wait.")
        self.root.update()  # Force UI update
        
        # Dictionary to store results for each algorithm
        results = {}
        
        # List of algorithms to compare: (name, function)
        algorithms_to_test = [
            ("BFS", bfs),
            ("DFS", dfs),
            ("A*", a_star),
            ("DFS Optimized", dfs_optimized),
            ("Bi-dir BFS", bfs_bidirectional)
        ]
        
        # Run each algorithm sequentially and collect metrics
        for algo_name, algo_func in algorithms_to_test:
            try:
                # Run the algorithm
                path, nodes_explored, runtime, explored_cells = algo_func(self.maze)
                
                # Store results
                results[algo_name] = {
                    'path_length': len(path) if path else 0,
                    'nodes_visited': nodes_explored,
                    'time_ms': runtime * 1000,  # Convert to milliseconds
                    'path_found': path is not None
                }
                
            except Exception as e:
                # Handle any errors during algorithm execution
                results[algo_name] = {
                    'path_length': 0,
                    'nodes_visited': 0,
                    'time_ms': 0,
                    'path_found': False,
                    'error': str(e)
                }
        
        # Display results in a popup window
        self.display_comparison_results(results)
        
        # Convert results to format expected by show_runtime_graph
        # The bar graph function expects a list with 'algorithm' and 'avg_runtime' keys
        graph_results = []
        for algo_name in ["BFS", "DFS", "A*", "DFS Optimized", "Bi-dir BFS"]:
            graph_results.append({
                'algorithm': algo_name,
                'avg_runtime': results[algo_name]['time_ms'] / 1000  # Convert back to seconds
            })
        
        # Show the bar graph using the existing analysis.py function
        show_runtime_graph(self.maze, graph_results)
        
        # Reset maze visualization
        self.draw_maze()
        self.update_status("Algorithm comparison complete")
    
    def display_comparison_results(self, results):
        """
        Display comparison results in a clean popup window with a table
        
        Args:
            results: Dictionary with algorithm names as keys and metrics as values
        """
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Algorithm Comparison Results")
        popup.geometry("700x450")
        popup.configure(bg=self.colors['bg'])
        popup.resizable(True, True)
        popup.minsize(600, 400)
        
        # Center the popup window
        popup.transient(self.root)
        popup.grab_set()
        
        # Title
        title_label = tk.Label(
            popup,
            text="📊 ALGORITHM COMPARISON RESULTS",
            font=('Arial', 16, 'bold'),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            pady=15
        )
        title_label.pack(fill=tk.X)
        
        # Create frame for table with padding
        table_container = tk.Frame(popup, bg=self.colors['panel_bg'])
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create table frame using grid layout
        table_frame = tk.Frame(table_container, bg=self.colors['panel_bg'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns to expand evenly
        for col in range(5):
            table_frame.columnconfigure(col, weight=1, uniform="cols")
        
        # Table headers
        headers = ["Algorithm", "Path Length", "Nodes Visited", "Time (ms)", "Status"]
        
        # Create header row using grid
        for col, header in enumerate(headers):
            label = tk.Label(
                table_frame,
                text=header,
                font=('Consolas', 11, 'bold'),
                bg=self.colors['title_bg'],
                fg=self.colors['title_fg'],
                pady=10,
                padx=15
            )
            label.grid(row=0, column=col, sticky='nsew', padx=1, pady=(0, 2))
        
        # Create data rows for each algorithm using grid
        for row_idx, algo_name in enumerate(["BFS", "DFS", "A*", "DFS Optimized", "Bi-dir BFS"], start=1):
            data = results.get(algo_name, {})
            
            # Determine status text and color
            if 'error' in data:
                status_text = "Error"
                status_color = '#F85149'
            elif data.get('path_found', False):
                status_text = "✓ Found"
                status_color = '#3FB950'
            else:
                status_text = "✗ No Path"
                status_color = '#F85149'
            
            # Row data
            row_data = [
                algo_name,
                str(data.get('path_length', 0)),
                str(data.get('nodes_visited', 0)),
                f"{data.get('time_ms', 0):.4f}",
                status_text
            ]
            
            # Alternate row background for better readability
            row_bg = self.colors['panel_bg'] if row_idx % 2 == 1 else self.colors['bg']
            
            # Create cells using grid
            for col, value in enumerate(row_data):
                # Use status color for last column
                if col == len(row_data) - 1:
                    fg_color = status_color
                    font_weight = 'bold'
                elif col == 0:
                    fg_color = self.colors['button_bg'] if not self.dark_mode else '#58A6FF'
                    font_weight = 'bold'
                else:
                    fg_color = self.colors['text']
                    font_weight = 'normal'
                
                cell = tk.Label(
                    table_frame,
                    text=value,
                    font=('Consolas', 11, font_weight),
                    bg=row_bg,
                    fg=fg_color,
                    pady=12,
                    padx=15,
                    relief=tk.GROOVE,
                    borderwidth=1
                )
                cell.grid(row=row_idx, column=col, sticky='nsew', padx=1, pady=1)
        
        # Add summary/notes section
        notes_frame = tk.Frame(popup, bg=self.colors['panel_bg'])
        notes_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        notes_text = (
            "Note: Results show performance on the current maze.\n"
            "• Path Length: Number of steps in the solution path\n"
            "• Nodes Visited: Total cells explored during search\n"
            "• Time: Execution time in milliseconds"
        )
        
        notes_label = tk.Label(
            notes_frame,
            text=notes_text,
            font=('Arial', 9),
            bg=self.colors['panel_bg'],
            fg=self.colors['text'],
            justify=tk.LEFT,
            anchor=tk.W
        )
        notes_label.pack(anchor=tk.W, pady=5)
        
        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            font=('Arial', 11, 'bold'),
            bg=self.colors['button_bg'],
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        close_btn.pack(pady=(0, 15))


def main():
    root = tk.Tk()
    app = MazePathfinderAdvanced(root)
    root.mainloop()


if __name__ == "__main__":
    main()

