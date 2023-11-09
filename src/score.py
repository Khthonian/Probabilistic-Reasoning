# Import libraries
from math import log

import pandas as pd
import numpy as np
import networkx as nx


def scoreFunction(DAG: nx.DiGraph, data: str):
    """
    A function to calculate the LL and BIC scores from a given DAG and dataset.

    Parameters:
    - DAG (nx.DiGraph): The DAG.
    - data (str): The path to the dataset.
    """

    # Read the data into a pandas DataFrame
    dataDF = pd.read_csv(data, encoding='utf-8-sig')
    dataDF.columns = [col.encode('utf-8').decode('utf-8-sig')
                      if col.startswith('\ufeff') else col for col in dataDF.columns]

    # Initialise LL and parameter count
    logLikelihood = 0
    numParameters = 0

    # For each node, estimate its CPT given its parents in the DAG
    for node in DAG.nodes:
        parents = list(DAG.predecessors(node))
        if not parents:
            # Calculate frequencies and probabilities
            counts = dataDF[node].value_counts()
            probs = counts / counts.sum()
            logLikelihood += (dataDF[node].map(probs) +
                              1e-9).apply(np.log).sum()
            numParameters += len(probs) - 1
        else:
            # Calculate CPT for nodes with parents
            cpt = (dataDF.groupby(parents)[node]
                   .value_counts()
                   .unstack(fill_value=0) + 1e-9)  # Laplace smoothing
            cpt /= cpt.sum(axis=1).values[:, None]
            for _, row in dataDF.iterrows():
                parent_values = tuple(row[parent] for parent in parents)
                node_value = row[node]
                logLikelihood += np.log(cpt.loc[parent_values, node_value])
            numParameters += np.prod([len(dataDF[parent].unique())
                                     for parent in parents]) * (len(dataDF[node].unique()) - 1)

    # Calculate BIC
    n = len(dataDF)
    bic = logLikelihood - (log(n) / 2) * numParameters

    print(logLikelihood)
    print(bic)  # TODO: Return the values
