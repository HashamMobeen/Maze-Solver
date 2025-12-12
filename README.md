Maze Solver (Python)

This project solves mazes using three algorithms: BFS, DFS, and A*. The program reads a maze from a text file, finds a path from the start (S) to the goal (G), and compares the performance of the algorithms. This project was made for the Data Structures and Algorithms (DSA) course.

Features:
  -> Load maze from a text file
  -> Solve using BFS, DFS, and A*
  -> Show path in the console
  -> Count explored nodes
  -> Measure runtime
  -> Compare all algorithms
  -> Includes small, medium, and large test mazes
  
Project Structure:
  maze.py          # Maze loading, validation, neighbors, printing  
  algorithms.py    # BFS, DFS, A* implementations  
  analysis.py      # Benchmarking, sorting, performance comparison  
  main.py          # Menu system, test cases, user interaction  
  test_small.txt
  test_medium.txt
  test_large.txt

How to Run:
  1. Open the project folder.
  2. Run:
        python main.py
  3. Follow the menu options to:
     ● Load a maze
     ● Run BFS / DFS / A*
     ● Compare algorithms
     ● Run the test cases

Test Cases:
  The project includes three test mazes:
    ● Small (10x10)
    ● Medium (20x20)
    ● Large (30x30)

Notes:
  -> The project runs in the console.
  -> Only 4-direction movement is allowed (up, down, left, right).
  -> The mazes must follow the provided text format.
