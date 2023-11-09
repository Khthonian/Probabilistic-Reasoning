# Import libraries
import csv
import matplotlib.pyplot as plt
import networkx as nx

displayGraph = False  # TODO: Set this boolean from main script


def generateNaiveDAG(dataFile):
    """
    A function to generate a DAG for a Naive Bayes structure.

    Parameters:
    - dataFile (str): The path to the data file used for generate the DAG.

    Returns:
    - (nx.DiGraph): The generated DAG.
    """

    # Collect column names
    with open(dataFile, "r") as csvFile:
        reader = csv.reader(csvFile)
        columnNames = next(reader)

    # Create an empty graph
    DG = nx.DiGraph()

    # Add nodes
    for col in columnNames:
        DG.add_node(col)

    # Add edges from the last column to all other columns
    lastCol = columnNames[-1]
    for col in columnNames[:-1]:
        DG.add_edge(lastCol, col)

    print(DG.edges())

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
