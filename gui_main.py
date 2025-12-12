"""
Name: Muhammad Hasham Mobeen
CMS: 516259
GUI Main - FIXED with Scrollable Panel and Hover Effects
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from maze import Maze
from algorithms import bfs, dfs, a_star
from analysis import compare_all_algorithms, sort_results_by_runtime, show_runtime_graph, generate_comparison_chart

# Test mazes
SMALL_MAZE = """##########
#S.......#
#.####.#.#
#....#.#.#
####.#.#.#
#....#.#.#
#.########
#........#
#.######.#
#......#G#
##########"""

MEDIUM_MAZE = """####################
#S.................#
#.####.##.####.###.#
#....#....#....#...#
####.####.#.##.#.###
#........#....#....#
#.######.####.####.#
#.#............#...#
#.#.##########.#.###
#.#.#..........#...#
#.#.#.############.#
#...#..............#
#####.##########.###
#.....#........#...#
#.###.#.######.###.#
#.#.#.#.#......#...#
#.#.#.#.#.######.###
#.#.....#..........#
#.###############..#
#................#G#
####################"""

LARGE_MAZE = """##############################
#S...........................#
#.##.#####.#######.#######.#.#
#.##.#.....#.....#.......#.#.#
#.##.#.#####.###.#######.#.#.#
#....#.#.....#...#.......#.#.#
######.#.#####.###.#######.#.#
#......#.....#...#.........#.#
#.##########.###.###########.#
#.#..........#...#...........#
#.#.##########.###.###########
#.#.#..........#...#.........#
#.#.#.##########.###.#######.#
#...#............#...#.......#
#####.############.###.#######
#.....#..........#.....#.....#
#.#####.########.#######.###.#
#.#.....#......#.........#...#
#.#.#####.####.###########.###
#.#.#.....#..#.............#.#
#.#.#.#####..#############.#.#
#.#.#.....#................#.#
#.#.#####.##################.#
#.#.......#..................#
#.#########.##################
#...........#................#
###########.#.##############.#
#...........#.#..............#
#.###########.#.##############
#...........................G#
##############################"""


class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Maze Pathfinder - DSA Project")
        self.root.geometry("1100x650")
        self.root.configure(bg='#ECF0F1')
        
        self.maze = None
        self.current_path = None
        self.explored_cells = set()
        self.cell_size = 18
        self.last_comparison_results = None
        
        self.colors = {
            'wall': '#34495E',
            'path': '#FFFFFF',
            'start': '#F39C12',
            'goal': '#E74C3C',
            'explored': '#5DADE2',
            'solution': '#58D68D'
        }
        
        self.create_widgets()
        self.load_maze(SMALL_MAZE, "Small Maze (10x10)")
    
    def create_hover_button(self, parent, text, command, bg, **kwargs):
        """Create button with hover effect"""
        # Calculate lighter color
        hover_colors = {
            '#3498DB': '#5DADE2',
            '#F39C12': '#F8B739',
            '#E74C3C': '#EC7063',
            '#95A5A6': '#B2BABB',
            '#5DADE2': '#85C1E9',
            '#EC7063': '#F1948A',
            '#AF7AC5': '#C39BD3',
            '#58D68D': '#7DCEA0',
            '#8E44AD': '#A569BD',
            '#16A085': '#48C9B0'
        }
        hover_bg = hover_colors.get(bg, bg)
        
        btn = tk.Button(parent, text=text, command=command, bg=bg, **kwargs)
        
        def on_enter(e):
            btn['bg'] = hover_bg
        
        def on_leave(e):
            btn['bg'] = bg
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_widgets(self):
        # Title bar
        title_bar = tk.Frame(self.root, bg='#2C3E50', height=70)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        tk.Label(
            title_bar,
            text="🔍 MAZE PATHFINDER",
            font=('Arial', 22, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(pady=20)
        
        # Main container
        container = tk.Frame(self.root, bg='#ECF0F1')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== SCROLLABLE LEFT PANEL ==========
        left_frame = tk.Frame(container, bg='white', width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Create canvas for scrolling
        left_canvas = tk.Canvas(left_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame, orient='vertical', command=left_canvas.yview)
        
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(left_canvas, bg='white')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        left_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Now add all buttons to scrollable_frame
        left = scrollable_frame
        
        # Maze selection
        tk.Label(left, text="SELECT MAZE", font=('Arial', 12, 'bold'), bg='white').pack(pady=15)
        
        self.create_hover_button(
            left,
            text="Small (10×10)",
            command=lambda: self.load_maze(SMALL_MAZE, "Small (10x10)"),
            bg='#3498DB',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="Medium (20×20)",
            command=lambda: self.load_maze(MEDIUM_MAZE, "Medium (20x20)"),
            bg='#F39C12',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="Large (30×30)",
            command=lambda: self.load_maze(LARGE_MAZE, "Large (30x30)"),
            bg='#E74C3C',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="📂 Load File",
            command=self.load_from_file,
            bg='#95A5A6',
            fg='white',
            font=('Arial', 10),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        # Separator
        tk.Frame(left, height=2, bg='#BDC3C7').pack(fill=tk.X, pady=20, padx=10)
        
        # Algorithm buttons
        tk.Label(left, text="RUN ALGORITHM", font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
        
        self.create_hover_button(
            left,
            text="🔵 BFS",
            command=lambda: self.run_algorithm('BFS', bfs),
            bg='#5DADE2',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="🔴 DFS",
            command=lambda: self.run_algorithm('DFS', dfs),
            bg='#EC7063',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="⭐ A*",
            command=lambda: self.run_algorithm('A*', a_star),
            bg='#AF7AC5',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        self.create_hover_button(
            left,
            text="📊 Compare All",
            command=self.compare_all,
            bg='#58D68D',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        # Separator
        tk.Frame(left, height=2, bg='#BDC3C7').pack(fill=tk.X, pady=20, padx=10)
        
        # ========== GRAPHICAL COMPARISON SECTION ==========
        tk.Label(
            left,
            text="📊 GRAPH COMPARISON",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#8E44AD'
        ).pack(pady=10)
        
        # THE BIG BUTTON YOU WANT
        self.create_hover_button(
            left,
            text="📊 SHOW GRAPH",
            command=self.show_graph,
            bg='#8E44AD',
            fg='white',
            font=('Arial', 13, 'bold'),
            width=25,
            height=3,
            cursor='hand2',
            relief=tk.RAISED,
            borderwidth=3
        ).pack(pady=10, padx=10)
        
        self.create_hover_button(
            left,
            text="💾 Save Chart",
            command=self.save_chart,
            bg='#16A085',
            fg='white',
            font=('Arial', 10),
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=5, padx=10)
        
        # Add padding at bottom
        tk.Frame(left, height=30, bg='white').pack()
        
        # ========== CENTER PANEL ==========
        center = tk.Frame(container, bg='white')
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.info_label = tk.Label(
            center,
            text="Current Maze: Small (10×10)",
            font=('Arial', 12, 'bold'),
            bg='#2C3E50',
            fg='white',
            pady=12
        )
        self.info_label.pack(fill=tk.X)
        
        # Legend
        legend = tk.Frame(center, bg='#F5F5F5', height=45)
        legend.pack(fill=tk.X)
        
        legend_inner = tk.Frame(legend, bg='#F5F5F5')
        legend_inner.pack(expand=True)
        
        tk.Label(legend_inner, text="  ", bg='#F39C12', width=2).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_inner, text="Start", bg='#F5F5F5', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(legend_inner, text="  ", bg='#E74C3C', width=2).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_inner, text="Goal", bg='#F5F5F5', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(legend_inner, text="  ", bg='#5DADE2', width=2).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_inner, text="Explored", bg='#F5F5F5', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(legend_inner, text="  ", bg='#58D68D', width=2).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_inner, text="Path", bg='#F5F5F5', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Canvas
        canvas_frame = tk.Frame(center, bg='#ECF0F1')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        v_scroll.config(command=self.canvas.yview)
        h_scroll.config(command=self.canvas.xview)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ========== RIGHT PANEL ==========
        right = tk.Frame(container, bg='white', width=270)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)
        
        tk.Label(
            right,
            text="📋 RESULTS",
            font=('Arial', 12, 'bold'),
            bg='#2C3E50',
            fg='white',
            pady=12
        ).pack(fill=tk.X)
        
        results_frame = tk.Frame(right)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll = tk.Scrollbar(results_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            results_frame,
            font=('Courier', 9),
            bg='#F8F9FA',
            wrap=tk.WORD,
            yscrollcommand=scroll.set
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.results_text.yview)
        
        self.update_results("👋 Welcome!\n\nLoad a maze and run algorithms.\n\n💡 Scroll down in left\npanel to see:\n\n📊 SHOW GRAPH button!")
    
    def load_maze(self, maze_string, name):
        self.maze = Maze()
        self.maze.load_from_string(maze_string)
        self.current_path = None
        self.explored_cells = set()
        
        self.info_label.config(text=f"Current Maze: {name}")
        self.draw_maze()
        self.update_results(f"✅ Loaded: {name}\nSize: {self.maze.rows}×{self.maze.cols}\n\nReady to run!")
    
    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.load_maze(f.read(), filename.split('/')[-1])
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def draw_maze(self, explored=None, path=None):
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
                
                if cell == '#':
                    color = self.colors['wall']
                elif cell == 'S':
                    color = self.colors['start']
                elif cell == 'G':
                    color = self.colors['goal']
                
                if explored and (r, c) in explored and cell not in ['S', 'G']:
                    color = self.colors['explored']
                
                if path and (r, c) in path and cell not in ['S', 'G']:
                    color = self.colors['solution']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#BDC3C7')
    
    def run_algorithm(self, name, func):
        if not self.maze:
            messagebox.showwarning("No Maze", "Load a maze first!")
            return
        
        path, nodes, runtime, explored = func(self.maze)
        self.draw_maze(explored, path)
        
        if path:
            text = f"✅ {name} SUCCESS\n"
            text += "="*30 + "\n"
            text += f"Path: {len(path)} steps\n"
            text += f"Nodes: {nodes}\n"
            text += f"Time: {runtime*1000:.3f}ms\n"
        else:
            text = f"❌ {name} - No path\n"
        
        self.update_results(text)
    
    def compare_all(self):
        if not self.maze:
            messagebox.showwarning("No Maze", "Load a maze first!")
            return
        
        results = compare_all_algorithms(self.maze)
        self.last_comparison_results = results
        sorted_results = sort_results_by_runtime(results)
        
        text = "📊 COMPARISON\n" + "="*30 + "\n"
        for i, r in enumerate(sorted_results, 1):
            text += f"\n{i}. {r['algorithm']}\n"
            text += f"   {r['avg_runtime']*1000:.3f}ms\n"
            text += f"   {int(r['avg_nodes'])} nodes\n"
        
        self.update_results(text)
        best = sorted_results[0]
        self.draw_maze(best['explored_cells'], best['path'])
    
    def show_graph(self):
        """SHOW THE RUNTIME GRAPH - Uses same results as Compare All"""
        if not self.maze:
            messagebox.showwarning("No Maze", "Load a maze first!")
            return
            
        # Check if we already have results from Compare All
        if not hasattr(self, 'last_comparison_results') or self.last_comparison_results is None:
            self.update_results("⏳ Running algorithms...\n\nFirst time graph.\nPlease wait...")
            self.root.update()
            results = compare_all_algorithms(self.maze, runs=3)
            self.last_comparison_results = results
            
        else:
            # Reuse existing results
            results = self.last_comparison_results
            
        show_runtime_graph(self.maze, results)
            
        self.update_results("✅ Graph displayed!\n\nShowing same results\nas Compare All button.")

    
    def save_chart(self):
        test_mazes = [(SMALL_MAZE, "10x10"), (MEDIUM_MAZE, "20x20"), (LARGE_MAZE, "30x30")]
        all_results = []
        
        self.update_results("💾 Generating chart...\n\nTesting 3 maze sizes...")
        self.root.update()
        
        for maze_str, size in test_mazes:
            temp = Maze()
            temp.load_from_string(maze_str)
            all_results.append(compare_all_algorithms(temp))
        
        generate_comparison_chart(all_results, ["10x10", "20x20", "30x30"])
        messagebox.showinfo("Saved!", "Chart saved as\nperformance_chart.png")
    
    def update_results(self, text):
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', text)


def main():
    root = tk.Tk()
    app = MazeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
