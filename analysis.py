"""
Ahmad Mustafa
Performance Analysis Module
"""

import time
import matplotlib.pyplot as plt
from algorithms import bfs, dfs, a_star


def compare_all_algorithms(maze, runs=3):
    """Run all three algorithms and return results"""
    algorithms = [
        (bfs, 'BFS'),
        (dfs, 'DFS'),
        (a_star, 'A*')
    ]
    
    results = []
    for algo_func, algo_name in algorithms:
        runtimes = []
        nodes_counts = []
        path_length = 0
        final_path = None
        explored_cells = set()
        
        for _ in range(runs):
            path, nodes_explored, runtime, exp_cells = algo_func(maze)
            runtimes.append(runtime)
            nodes_counts.append(nodes_explored)
            if path and not final_path:
                path_length = len(path)
                final_path = path
                explored_cells = exp_cells
        
        results.append({
            'algorithm': algo_name,
            'avg_runtime': sum(runtimes) / len(runtimes),
            'avg_nodes': sum(nodes_counts) / len(nodes_counts),
            'path_length': path_length,
            'path': final_path,
            'explored_cells': explored_cells
        })
    
    return results


def show_runtime_graph(maze, results):
    """
    SIMPLE GRAPH: Runtime on Y-axis, Algorithms on X-axis
    FIXED: Better label spacing and correct maze dimensions
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    algorithms = [r['algorithm'] for r in results]
    runtimes = [r['avg_runtime'] * 1000 for r in results]  # milliseconds
    
    # Colors for each algorithm (Blue, Red, Green, Purple, Orange)
    colors = ['#3498DB', '#E74C3C', '#2ECC71', '#9B59B6', '#F39C12']
    
    bars = ax.bar(algorithms, runtimes, color=colors, edgecolor='black', linewidth=2, width=0.6)
    
    # FIXED: Reduced spacing - labels closer to bars
    for bar, value in zip(bars, runtimes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (max(runtimes) * 0.01),
                f'{value:.3f} ms',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # FIXED: Show actual maze dimensions (subtract 2 for border walls on each side if needed)
    # Calculate inner dimensions (excluding border walls)
    display_rows = maze.rows
    display_cols = maze.cols
    
    # If maze has walls on all 4 sides, show inner dimensions
    # Check if first/last row and first/last column are all walls
    if all(maze.grid[0][c] == '#' for c in range(maze.cols)):  # Top row all walls
        if all(maze.grid[-1][c] == '#' for c in range(maze.cols)):  # Bottom row all walls
            if all(maze.grid[r][0] == '#' for r in range(maze.rows)):  # Left column all walls
                if all(maze.grid[r][-1] == '#' for r in range(maze.rows)):  # Right column all walls
                    display_rows = maze.rows  # Keep as is - borders are part of the maze
                    display_cols = maze.cols
    
    ax.set_xlabel('Algorithm', fontsize=14, fontweight='bold')
    ax.set_ylabel('Runtime (milliseconds)', fontsize=14, fontweight='bold')
    ax.set_title(f'⏱️  Runtime Comparison - Maze {display_rows}×{display_cols}', 
                fontsize=16, fontweight='bold')
    ax.set_ylim(0, max(runtimes) * 1.15)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def sort_results_by_runtime(results):
    """Sort by runtime"""
    return sorted(results, key=lambda x: x['avg_runtime'])


def generate_comparison_chart(all_results, maze_sizes, filename='performance_chart.png'):
    """Save chart to file"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bfs_times = [r[0]['avg_runtime'] * 1000 for r in all_results]
    dfs_times = [r[1]['avg_runtime'] * 1000 for r in all_results]
    astar_times = [r[2]['avg_runtime'] * 1000 for r in all_results]
    
    x = range(len(maze_sizes))
    width = 0.25
    
    ax.bar([i - width for i in x], bfs_times, width, label='BFS', color='#3498DB')
    ax.bar(x, dfs_times, width, label='DFS', color='#E74C3C')
    ax.bar([i + width for i in x], astar_times, width, label='A*', color='#2ECC71')
    
    ax.set_xlabel('Maze Size', fontweight='bold')
    ax.set_ylabel('Runtime (ms)', fontweight='bold')
    ax.set_title('Performance Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(maze_sizes)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
