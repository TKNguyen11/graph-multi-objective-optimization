"""
Graph Loader Module.

This module is responsible for initializing and populating a Graph object
by reading data from a TOML configuration file. It ensures the environment
is running a compatible version of Python (3.11+) to support the standard
library's TOML parser.
"""


from sys import version_info

from tomllib import load

from Mehrzieloptimierung import Graph


def load_graph(filepath):
    """
    Loads 'graph.toml' and returns a Graph object.

    Args:
        filepath (str): The filepath to the Toml file.

    Returns:
        tuple: A tuple containing the graph, the starting node name
        and the ending node name in that order.

    (No doctest here because it relies on the file system)
    """
    with open(filepath, "rb") as graph_file:
        loaded_graph = load(graph_file)
        start_node = loaded_graph["start_node"]
        end_node = loaded_graph["end_node"]
        graph = loaded_graph["graph"]
    return (build_graph_from_dict(graph), start_node, end_node)


def build_graph_from_dict(data):
    """
    Converts a dictionary structure (like loaded TOML) into a Graph object.

    Args:
        data (dict): The dictionary containing node and edge definitions.

    Returns:
        Graph: The populated graph.

    Examples:
        >>> raw_data = {
        ...     'A': {'B': {'cost': 10, 'distraction': 2}},
        ...     'B': {}
        ... }
        >>> g = build_graph_from_dict(raw_data)
        >>> g.get_neighbors('A')
        [('B', 10, 2)]

        >>> duplicate_data = {
        ...     'A': {'B': {'cost': 5, 'distraction': 1}},
        ...     'B': {'A': {'cost': 5, 'distraction': 1}}
        ... }
        >>> g_dup = build_graph_from_dict(duplicate_data)
        >>> # Neighbors of A should just be [B], not [B, B]
        >>> len(g_dup.get_neighbors('A'))
        1

        >>> bad_data = {'Start': {'End': {}}} # No cost, No distraction
        >>> g_bad = build_graph_from_dict(bad_data)
        >>> g_bad.get_neighbors('Start')
        [('End', None, None)]
    """
    graph = Graph()
    for node, edges in data.items():
        graph.add_node(node)
        for dest, attr in edges.items():
            dest_list = [edge[0] for edge in graph.get_neighbors(node)]
            if dest in dest_list:  # Don't add the Edge twice
                continue
            graph.add_edge(
                node, dest, int(attr.get("cost")), int(attr.get("distraction"))
            )
    return graph


if __name__ == "__main__":
    if version_info[0] < 3 or (
        version_info[0] > 3 and version_info[1] < 11
    ):  # tomllib is only part of python since 3.11
        print("Dieses Script muss mit python >= 3.11 gestartet werden")
        exit(1)
    import doctest

    doctest.testmod()
