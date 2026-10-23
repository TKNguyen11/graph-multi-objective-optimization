"""
This module implements multi-objective optimization on a graph using
greedy and recursive backtracking approaches.

Usage:
    python Mehrzieloptimierung.py <graph_file>
"""

__author__ = "8487104, Nguyen, 8647593, Migowski"


import sys


class Graph:
    """
    Represents a graph and uses greedy approach or recursive backtracking to find optimal paths.
    Attributes:
        nodes_list: A dictionary where keys are node names and values are lists of tuples
                    (neighbor, cost, distraction).
    """

    def __init__(self):
        """Initializes an adjacency list for the graph."""
        self.nodes_list = {}

    def add_node(self, node):
        """
        Adds a node to the graph.
        Args:
            node: The name of the node to be added.

        Examples:
            >>> g = Graph()

            >>> # Test 1: Adding a single node
            >>> g.add_node("A")
            >>> "A" in g.nodes_list
            True

            >>> # Test 2: Adding another node
            >>> g.add_node("B")
            >>> "B" in g.nodes_list
            True

            >>> # Test 3: Adding an existing node (should not duplicate)
            >>> g.add_node("A")
            >>> len(g.nodes_list)
            2
        """

        if node not in self.nodes_list:
            self.nodes_list[node] = []

    def add_edge(self, u, v, cost, distraction):
        """
        Adds an undirected edge between nodes with cost and distraction.
        Args:
            u: The starting node.
            v: The ending node.
            cost: The cost associated with the edge.
            distraction: The distraction associated with the edge.

        Examples:
            >>> g = Graph()

            >>> # Test 1: Adding an edge between two new nodes
            >>> g.add_node("A")
            >>> g.add_node("B")
            >>> g.add_edge("A", "B", 5, 3)
            >>> g.nodes_list["A"]
            [('B', 5, 3)]

            >>> # Test 2: Adding another edge
            >>> g.add_node("C")
            >>> g.add_edge("A", "C", 2, 4)
            >>> g.nodes_list["A"]
            [('B', 5, 3), ('C', 2, 4)]

            >>> # Test 3: Adding edge where one node does not exist
            >>> g.add_edge("B", "Z", 1, 1)
            >>> g.nodes_list["B"]
            [('A', 5, 3), ('Z', 1, 1)]
        """

        if u not in self.nodes_list:
            self.add_node(u)

        if v not in self.nodes_list:
            self.add_node(v)

        self.nodes_list[u].append((v, cost, distraction))
        self.nodes_list[v].append((u, cost, distraction))

    def get_neighbors(self, node):
        """
        Returns neighbors of a given node as a list of tuples (neighbor, cost, distraction).
        Args:
            node: The node whose neighbors are to be retrieved.

        Returns:
            List of tuples representing neighbors.

        Examples:
            >>> g = Graph()

            >>> # Test 1: Node with one neighbor
            >>> g.add_node("A")
            >>> g.add_node("B")
            >>> g.add_edge("A", "B", 5, 3)
            >>> g.get_neighbors("A")
            [('B', 5, 3)]

            >>> # Test 2: Node with multiple neighbors
            >>> g.add_node("C")
            >>> g.add_edge("A", "C", 2, 4)
            >>> g.get_neighbors("A")
            [('B', 5, 3), ('C', 2, 4)]

            >>> # Test 3: Non-existing node
            >>> g.get_neighbors("D")
            []
        """

        return self.nodes_list.get(node, [])

    def recursive(
        self,
        start,
        end,
        optimize,
        visited=None,
        path=None,
        cost=0,
        distraction=0,
    ):
        """
        Finds the optimal path from start to end using recursive backtracking.
        Args:
            start: The starting node.
            end: The destination node.
            optimize: A function that takes cost and distraction and returns a score.
            visited: A set of visited nodes to avoid cycles.
            path: The current path taken.
            cost: The accumulated cost so far.
            distraction: The accumulated distraction so far.

        Returns:
            A tuple (cost, distraction, path) of the optimal path found or None if no path exists.

        Examples:
            >>> g = example_graph()

            >>> # Test 1: Optimize for minimum cost
            >>> g.recursive("A", "F", optimize_min_cost)
            (6, 7, ['A', 'C', 'D', 'F'])

            >>> # Test 2: Optimize for maximum distraction
            >>> g.recursive("A", "F", optimize_max_distraction)
            (10, 11, ['A', 'B', 'D', 'F'])

            # Test 3: Searching for non-existing path
            >>> g.recursive("A", "Z", optimize_min_cost) is None
            True
        """

        if visited is None:
            visited = set()

        if path is None:
            path = []

        visited.add(start)
        path.append(start)

        if start == end:
            res = cost, distraction, list(path)
            visited.remove(start)
            path.pop()
            return res

        best_result = None
        best_score = None

        for neighbor, edge_cost, edge_distraction in self.get_neighbors(start):
            if neighbor not in visited:
                result = self.recursive(
                    neighbor,
                    end,
                    optimize,
                    visited,
                    path,
                    cost + edge_cost,
                    distraction + edge_distraction,
                )
                # Update best result if current one is better
                if result is not None:
                    score = optimize(result[0], result[1])
                    if best_result is None or score > best_score:
                        best_result = result
                        best_score = score

        # Delete current node from visited and path before backtracking
        visited.remove(start)
        path.pop()

        return best_result

    def find_best_greedy_path(self, weight_function, start_node, end_node):
        """
        Finds a path from start to end using a specific greedy heuristic.

        This function traverses the graph by always selecting the 'best' next
        neighbor according to the provided weight_function.

        The search terminates and returns None if:
        1. A dead end is reached (weight_function returns None).
        2. A cycle is detected (the path visits a node twice).

        Args:
            weight_function (callable): A function that takes a list of neighbor
                tuples and returns the single best tuple to visit next.
            start_node: The identifier of the starting node.
            end_node: The identifier of the destination node.

        Returns:
            Tuple or None: A tuple containing: (path_list, total_cost, total_distraction).
            If a valid path is found. Returns None if the path is invalid or blocked.

        Examples:
            >>> from Mehrzieloptimierung import Graph
            >>> g = Graph()
            >>> # Edge Format: (u, v, cost, distraction)
            >>> g.add_edge('A', 'B', 10, 5)
            >>> g.add_edge('B', 'C', 5, 2)
            >>> g.add_edge('A', 'C', 20, 1) # Direct route is more expensive than A->B

            >>> # Test 1: Successful greedy path (A -> B -> C)
            >>> # It picks 'B' from 'A' because cost 10 < cost 20.
            >>> g.find_best_greedy_path(lowest_cost, 'A', 'C')
            (['A', 'B', 'C'], 15, 7)

            >>> # Test 2: Start equals End
            >>> g.find_best_greedy_path(lowest_cost, 'A', 'A')
            (['A'], 0, 0)

            >>> # Test 3: Cycle detection
            >>> g.add_edge('A', 'D', 1, 0)
            >>> g.add_edge('D', 'A', 0, 0)
            >>> g.add_edge('D', 'Exit', 100, 0)
            >>> g.find_best_greedy_path(lowest_cost, 'A', 'Exit') is None
            False
        """

        path = [start_node]
        cost = 0
        distraction = 0
        while path[-1] != end_node:
            all = self.get_neighbors(path[-1])
            valid = [
                n for n in all if n[0] not in path
            ]  # don't allow cycles, especially A -> B -> A
            next_edge = weight_function(valid)
            if next_edge is None:
                return None
            cost += next_edge[1]
            distraction += next_edge[2]
            path.append(next_edge[0])
        return (path, cost, distraction)


# Optimization functions for recursive backtracking
def optimize_min_cost(cost, distraction):
    """
    Optimizes for minimum cost.
    Args: cost: The total cost of the path.
          distraction: The total distraction of the path.

    Returns: A score that prioritizes lower cost.

    Examples:
        >>> # Test 1: Cost higher than distraction
        >>> optimize_min_cost(10, 5)
        -10

        >>> # Test 2: Cost lower than distraction
        >>> optimize_min_cost(3, 8)
        -3

        >>> # Test 3: Invalid data type
        >>> optimize_min_cost('a', 5)
        Traceback (most recent call last):
        ...
        TypeError: bad operand type for unary -: 'str'
    """

    return -cost


def optimize_max_distraction(cost, distraction):
    """
    Optimizes for maximum distraction.
    Args: cost: The total cost of the path.
          distraction: The total distraction of the path.

    Returns: A score that prioritizes higher distraction.

    Examples:
        >>> # Test 1: Distraction higher than cost
        >>> optimize_max_distraction(5, 10)
        10

        >>> # Test 2: Distraction lower than cost
        >>> optimize_max_distraction(8, 3)
        3

        >>> # Test 3: String input for distraction
        >>> optimize_max_distraction(5, 'b')
        'b'
    """

    return distraction


def optimize_balanced(cost, distraction):
    """
    Optimizes for a balance between cost and distraction and takes the lowest value.
    Args:
        cost: The total cost of the path.
        distraction: The total distraction of the path.

    Returns: A score that balances cost and distraction.

    Examples:
        >>> # Test 1: Higher distraction than cost
        >>> optimize_balanced(5, 10)
        5

        >>> # Test 2: Higher cost than distraction
        >>> optimize_balanced(12, 7)
        -5

        >>> # Test 3: Invalid data type for cost
        >>> optimize_balanced('c', 8)
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'int' and 'str'
    """

    return distraction - cost


# Optimization strategies for greedy approach
def lowest_cost(neighbors):
    """
    Heuristic strategy: Selects the neighbor with the lowest cost.

    Args:
        neighbors (list): A list of tuples in the format (node, cost, distraction).

    Returns:
        tuple or None: The neighbor tuple with the minimum cost value, or
        None if the neighbors list is empty.

    Examples:
        >>> neighbors_list = [('A', 10, 2), ('B', 5, 8), ('C', 20, 1)]
        >>> lowest_cost(neighbors_list)
        ('B', 5, 8)

        >>> lowest_cost([]) is None
        True

        >>> neighbors_list = [('A', 0, 243), ('B', 1, 42348), ('C', 54, 3)]
        >>> lowest_cost(neighbors_list)
        ('A', 0, 243)
    """

    if len(neighbors) == 0:
        return None
    candidate = neighbors[-1]
    for neighbor in neighbors:
        if neighbor[1] < candidate[1]:
            candidate = neighbor
    return candidate


def highest_distraction(neighbors):
    """
    Heuristic strategy: Selects the neighbor with the highest distraction.

    Args:
        neighbors (list): A list of tuples in the format (node, cost, distraction).

    Returns:
        tuple or None: The neighbor tuple with the maximum distraction value,
        or None if the neighbors list is empty.

    Examples:
        >>> neighbors_list = [('A', 10, 2), ('B', 5, 8), ('C', 20, 1)]
        >>> highest_distraction(neighbors_list)
        ('B', 5, 8)

        >>> highest_distraction([]) is None
        True

        >>> neighbors_list = [('A', 0, 243), ('B', 1, 42348), ('C', 54, 3)]
        >>> highest_distraction(neighbors_list)
        ('B', 1, 42348)
    """

    if len(neighbors) == 0:
        return None
    candidate = neighbors[-1]
    for neighbor in neighbors:
        if neighbor[2] > candidate[2]:
            candidate = neighbor
    return candidate


def lowest_difference(neighbors):
    """
    Heuristic strategy: Selects the neighbor with the lowest difference
    between cost and distraction.

    Calculates (cost - distraction) for each neighbor and picks the minimum.

    Args:
        neighbors (list): A list of tuples in the format (node, cost, distraction).

    Returns:
        tuple or None: The neighbor tuple that minimizes (cost - distraction),
        or None if the neighbors list is empty.

    Examples:
        >>> neighbors_list = [('A', 10, 2), ('B', 5, 8), ('C', 20, 1)]
        >>> lowest_difference(neighbors_list)
        ('B', 5, 8)

        >>> lowest_difference([]) is None
        True

        >>> neighbors_list = [('A', 0, 243), ('B', 1, 42348), ('C', 54, 3)]
        >>> lowest_difference(neighbors_list)
        ('B', 1, 42348)
    """

    if len(neighbors) == 0:
        return None
    candidate = neighbors[-1]
    for neighbor in neighbors:
        if neighbor[1] - neighbor[2] < candidate[1] - candidate[2]:
            candidate = neighbor
    return candidate


def example_graph():
    """
    Creates an example graph.
    Returns: A graph saved as a dictionary with nodes and edges with costs and distractions.
    """

    g = Graph()

    g.add_edge("A", "B", 3, 2)
    g.add_edge("A", "C", 1, 0)
    g.add_edge("B", "D", 4, 5)
    g.add_edge("B", "E", 2, 1)
    g.add_edge("C", "D", 2, 3)
    g.add_edge("D", "F", 3, 4)
    g.add_edge("E", "F", 5, 0)

    return g


def main(path):
    """
    Demonstrates the multi-objective optimization on an example graph.

    Args:
        path (str): a path to the graph file
    Returns:
        Path, cost, and distraction for different optimization strategies.
    """
    from loader import load_graph

    graph, start, end = load_graph(path)

    # Returns for recursive backtracking approach
    optimizations = [
        ("Minimiere Kosten", optimize_min_cost),
        ("Maximiere Ablenkung", optimize_max_distraction),
        ("Balanciere Kosten und Ablenkung", optimize_balanced),
    ]

    for optimization, optimization_function in optimizations:
        result = graph.recursive(start, end, optimization_function)
        print(f"\n--- Rekursiv optimiert nach: {optimization} ---")
        if result:
            cost, distraction, path = result
            print(f"Pfad:      {' -> '.join(path)}")
            print(f"Kosten:    {cost}")
            print(f"Ablenkung: {distraction}")
        else:
            print("Kein Weg gefunden")

    # Returns for greedy approach
    strategies = [
        ("Minimiere Kosten", lowest_cost),
        ("Maximiere Ablenkung", highest_distraction),
        ("Balanciere Kosten und Ablenkung", lowest_difference),
    ]
    for optimization, optimization_function in strategies:
        result = graph.find_best_greedy_path(optimization_function, start, end)
        print(f"\n--- Greedy optimiert nach: {optimization} ---")
        if result:
            path, cost, distraction = result
            print(f"Pfad:      {' -> '.join(path)}")
            print(f"Kosten:    {cost}")
            print(f"Ablenkung: {distraction}")
        else:
            print("Kein Weg gefunden")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    main(sys.argv[1])
