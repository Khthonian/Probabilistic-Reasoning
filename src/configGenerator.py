# Import libraries
from naive import generateNaiveDAG
from pcstable import generateDAG
from score import scoreFunction

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


def generateConfig(configFile: str, trainSet: str, modelName: str, naive: bool, score: bool):
    """
    A function to handle the configuration and generation process.

    Parameters:
    - configFile (str): The path to the output configuration file.
    - trainSet (str): The path to the training set file.
    - modelName (str): The name of the model to be written into the configuration file.
    - naive (bool): A flag to handle the structure learning.
    - score (bool): A flag to handle score calculation.
    """

    # Declare a variable to hold the DAG
    DG = None

    # Declare variables to hold the LL and BIC scores
    LL, BIC = (None, None)

    if naive:
        DG = generateNaiveDAG(trainSet)
    else:
        DG = generateDAG(trainSet)

    if score:
        # Get the LL and BIC scores from the DAG
        LL, BIC = scoreFunction(DG, trainSet)

    # Write the config file
    writeConfigFile(DG, configFile, modelName)

    return (LL, BIC)
