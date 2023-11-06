# Import libraries
from pcstable import generateDAG

import networkx as nx


def writeConfigFile(graph: nx.DiGraph, fileName: str, modelName: str):
    """
    A function to write a configuration file for the given DAG.

    Parameters:
    - graph (nx.DiGraph): The DAG for which to write the configuration file.
    - fileName (str): The path to the output configuration file.
    - modelName (str): The name of the model to be written into the configuration file.
    """

    # Perform topological sort
    sortedNodes = list(nx.topological_sort(graph))

    with open(fileName, 'w', encoding='utf-8') as f:
        # Write the model name
        f.write(f"name:{modelName}\n\n")

        # Write the random variables (in topological order)
        randomVariables = ";".join(
            [f"{node.strip()}({node.strip()})" for node in sortedNodes])
        f.write(f"random_variables:{randomVariables}\n\n")

        # Write the marginal probabilities first
        marginalProb = ";".join(
            [f"P({node.strip()})" for node in sortedNodes if not list(graph.predecessors(node))])

        # Write the conditional probabilities
        conditionalProb = ";".join(
            [f"P({node.strip()}|{','.join(graph.predecessors(node)).strip()})" for node in sortedNodes if list(graph.predecessors(node))])

        # Combine marginal and conditional probabilities into the final structure string
        structure = f"{marginalProb};{conditionalProb}" if marginalProb else conditionalProb
        f.write(f"structure:{structure}\n\n")


# Generate the graph using the function from pcstable.py
# TODO: Replace with dynamic path
DG = generateDAG("../data/diabetes_data-discretized-train.csv")

# Write the config file
# TODO: Replace with dynamic path and model name
writeConfigFile(DG, "../config/modelConfig.txt", "YourModelName")
