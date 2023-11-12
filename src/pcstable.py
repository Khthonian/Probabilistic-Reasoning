# Import libraries
from independence import Independence
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx


def findSubsets(S: set, m: int):
    """
    A function to find all subsets of a given set.

    Parameters:
    - S (set): The original set from which subsets will be generated.
    - m (int): The size of each subset.

    Returns:
    - (list of set): A list of subsets from S, each of size m.
    """

    return [set(combo) for combo in combinations(S, m)]


def formsCycle(DG: nx.DiGraph, start: str, end: str):
    """
    A function to check if orienting an edge would create a cycle.

    Parameters:
    - DG (nx.DiGraph): The directed graph in which to check for cycles.
    - start (node): The start node of the potential edge.
    - end (node): The end node of the potential edge.

    Returns:
    - (bool): A boolean that is True if the potential edge creates a cycle.
    """

    # Temporarily add the directed edge
    DG.add_edge(start, end)

    # Check for cycles
    try:
        nx.find_cycle(DG, orientation="original")
        # If a cycle is found, remove the edge and return True
        DG.remove_edge(start, end)
        return True
    except nx.NetworkXNoCycle:
        # No cycle found, keep the edge and return False
        return False


def removeCycles(DG: nx.DiGraph):
    """
    A function to remove all cycles from the graph.

    Parameters:
    - DG (nx.DiGraph): The directed graph in which to check for cycles.
    """

    while True:
        try:
            cycle = nx.find_cycle(DG, orientation="original")
            DG.remove_edge(cycle[-1][0], cycle[-1][1])
        except nx.NetworkXNoCycle:
            break


def generateDAG(dataFile: str, displayGraph: bool):
    """
    A function to generate a DAG using the PC-Stable algorithm.

    Parameters:
    - dataFile (str): The path to the data file used for generating the DAG.

    Returns:
    - (nx.DiGraph): The generated DAG.
    """

    # Initialise Independence object
    independenceTest = Independence(dataFile)

    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph based on the dataset columns
    G.add_nodes_from(independenceTest.randomVariables)

    # Initially connect all nodes
    for col1, col2 in combinations(independenceTest.randomVariables, 2):
        G.add_edge(col1, col2)

    # PC-Stable Algorithm
    for col in independenceTest.randomVariables:
        # neighbours to be checked for conditional independence with col
        neighbours = list(G.neighbors(col))
        for neighbour in neighbours:
            # Nodes that are still neighbours of both col and neighbour
            candidates = set(G.neighbors(col)).intersection(
                G.neighbors(neighbour)) - {col, neighbour}

            # Start with zero conditioning set and increase
            for k in range(len(candidates) + 1):
                isIndependent = False

                # Check all subsets of candidates of size k
                for subset in findSubsets(candidates, k):
                    # Perform the conditional independence test
                    pValue = independenceTest.computePValue(
                        col, neighbour, list(subset))
                    if pValue > 0.05:
                        isIndependent = True
                        break

                if isIndependent:
                    # Remove the edge between col and neighbour
                    G.remove_edge(col, neighbour)
                    break

    # Convert the graph to a DiGraph for directed operations
    DG = nx.DiGraph()
    DG.add_edges_from(G.edges())

    # Orient V-structures
    for node in DG.nodes():
        neighbours = list(DG.neighbors(node)) + list(DG.predecessors(node))
        for neighbour1, neighbour2 in combinations(neighbours, 2):
            pValue = independenceTest.computePValue(
                neighbour1, neighbour2, [node])
            if pValue > 0.05:
                # Check if adding the edge would create a cycle
                if not formsCycle(DG, neighbour1, node) and not formsCycle(DG, neighbour2, node):
                    DG.add_edge(neighbour1, node)
                    DG.add_edge(neighbour2, node)
        # Remove all cycles
        removeCycles(DG)

    if displayGraph:
        shellPos = nx.shell_layout(DG)

        # Draw nodes and labels
        nx.draw_networkx_nodes(
            DG, shellPos, node_color="lightblue", node_size=1000)
        nx.draw_networkx_labels(DG, shellPos, font_size=12, font_weight="bold")

        # Draw edges with arrows
        nx.draw_networkx_edges(DG, shellPos, edge_color="k",
                               arrows=True, arrowsize=20, connectionstyle="arc3,rad=0.2")

        # Turn off the axis for a cleaner look
        plt.axis("off")
        plt.title("Directed Graph after PC-Stable Algorithm")
        plt.show()

    return DG
