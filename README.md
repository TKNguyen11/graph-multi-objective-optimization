# Multi-Objective Graph Optimization

The program "multi-objective-optimization.py" solves the problem of multi-objective optimization in a graph by searching for a path from start to end that minimizes effort and maximizes distraction. To use this program, the auxiliary modules "perf.py" and "loader.py" are required. "perf.py" contains functions that prompt the user for the file path of a graph and the number of runs, then measures the execution times of the two traversal methods, while "loader.py" loads a graph which "multi-objective-optimization.py" traverses.

The graph is traversed using two different approaches: recursive and greedy. When running the program, the user is first prompted for the file path of the graph, after which the start-to-target path, total effort of the path, and total cost (distraction/effort metrics) are output for the following three optimization modes:
1. Minimize effort
2. Maximize distraction
3. Find a balance between distraction and effort, choosing the path with the lowest difference

## Requirements & Execution
* A Python interpreter version 3.11 or newer with standard libraries and support programs from www.python.org must be installed.
* Start the program "multi-objective-optimization.py" in the usual manner for the respective operating system, from the interpreter shell or in an IDE, e.g., IDLE.

## Additional Notes
* No bugs are known.
