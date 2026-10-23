"""
Performance benchmarking suite for multi-objective graph traversal.

This module provides tools to measure and compare the execution time of
various path-finding strategies, including greedy searches and
recursive optimization. It evaluates strategies based on cost
minimization, distraction maximization, and weighted balance.

The script outputs a formatted leaderboard ranking strategies by their
computational efficiency and calculating the relative performance
difference compared to the fastest result.

Usage:
    python perf.py <passes> <graph_file>
"""


import sys
from timeit import timeit

from loader import load_graph
from Mehrzieloptimierung import (
    highest_distraction,
    lowest_cost,
    lowest_difference,
    optimize_balanced,
    optimize_max_distraction,
    optimize_min_cost,
)


def time_greedy(passes, graph, start, end):
    """
    Benchmark greedy search strategies on a graph and return timing results.

    Measures the execution time of three different greedy path-finding strategies
    over a specified number of passes and returns the results sorted by speed.

    Args:
        passes: Number of times to execute each strategy for timing (must be ≥ 1)
        graph: Graph object
        start: Starting node for path finding
        end: Destination node for path finding

    Returns:
        List of tuples (execution_time, strategy_name) for each greedy strategy

    Raises:
        ValueError: If passes is less than 1
    """
    if passes < 1:
        raise ValueError("passes must be at least 1")
    strategies = [
        ("Greedy: Minimiere Kosten", lowest_cost),
        ("Greedy: Maximale Ablenkung", highest_distraction),
        ("Greedy: Balanciere Kosten und Ablenkung", lowest_difference),
    ]
    elapsed_time = []
    for name, strategy_function in strategies:
        eval_time = timeit(
            lambda: graph.find_best_greedy_path(strategy_function, start, end),
            number=passes,
        )
        elapsed_time.append((eval_time, name))
    return elapsed_time


def time_recursive(passes, graph, start, end):
    """
    Benchmark recursive path-finding strategies on a graph and return timing results.

    Measures execution time of three different recursive optimization strategies
    over a specified number of passes and returns the results sorted by speed.

    Args:
        passes: Number of times to execute each strategy for timing (must be ≥ 1)
        graph: Graph object with recursive method for path optimization
        start: Starting node for path finding
        end: Destination node for path finding

    Returns:
        List of tuples (execution_time, strategy_name) for each recursive strategy

    Raises:
        ValueError: If passes is less than 1
    """
    strategies = [
        ("Rekursiv: Minimiere Kosten", optimize_min_cost),
        ("Rekursiv: Maximiere Ablenkung", optimize_max_distraction),
        ("Rekursiv: Balanciere Kosten und Ablenkung", optimize_balanced),
    ]
    elapsed_time = []
    for name, strategy_function in strategies:
        eval_time = timeit(
            lambda: graph.recursive(start, end, strategy_function),
            number=passes,
        )
        elapsed_time.append((eval_time, name))
    return elapsed_time


def run_benchmark(passes, graph_location):
    """
    Run a comprehensive benchmark comparing greedy and recursive path-finding strategies.

    Loads a graph from the specified location, runs both greedy and recursive benchmarks,
    and prints a formatted comparison table showing relative performance of all strategies.

    Args:
        passes: Number of executions for timing each strategy (must be ≥ 1)
        graph_location: Path to graph data file or identifier for load_graph function

    Returns:
        None (results are printed to stdout)

    Raises:
        FileNotFoundError: If graph_location cannot be loaded
    """
    graph, start_node, end_node = load_graph(graph_location)
    recursive_results = time_recursive(passes, graph, start_node, end_node)
    greedy_results = time_greedy(passes, graph, start_node, end_node)
    sorted_results = sorted(recursive_results + greedy_results)
    fastest_runtime = sorted_results[0][0]
    print("Platzierung|Strategie Name|Laufzeit|% Differenz")
    for place, (runtime, strategy_name) in enumerate(sorted_results):
        diff = fastest_runtime / runtime
        print(f"{place + 1}|{strategy_name}|{runtime}|{diff:.2%}")


if __name__ == "__main__":
    run_benchmark(int(sys.argv[1]), sys.argv[2])
    # runs = 100000
    # graph = load_graph("graph.toml")
    # greedy_results = time_greedy(runs, graph, "Cat", "Home")
    # recursive_results = time_recursive(runs, graph, "Cat", "Home")
    # print("Ergebnisse:\n")
    # print(
    #     f"Strategien nach Zeit sortiert: {sorted(greedy_results + recursive_results)}"
    # )
