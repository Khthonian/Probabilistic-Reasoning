from collections import defaultdict
from pcstable import generateDAG  

def writeConfigFile(graph, fileName, modelName):
    with open(fileName, 'w', encoding='utf-8') as f:
        # Write the model name
        f.write(f"name:{modelName}\n\n")
        
        # Write the random variables
        randomVariables = ";".join([f"{node.strip()}({node.strip()})" for node in graph.nodes()])
        f.write(f"random_variables:{randomVariables}\n\n")
        
        # Write the structure
        structureDict = defaultdict(list)
        for edge in graph.edges():
            parent, child = edge
            structureDict[child].append(parent)
        
        structure = []
        for child, parents in structureDict.items():
            parentsStr = ",".join(parents)
            structure.append(f"P({child}|{parentsStr})")
        
        # Adding nodes with no parents
        noParentNodes = set(graph.nodes()) - set(structureDict.keys())
        for node in noParentNodes:
            structure.append(f"P({node})")
        
        structureStr = ";".join(structure)
        f.write(f"structure:{structureStr}\n")

# Generate the graph using the function from pcstable.py
DG = generateDAG("../data/diabetes_data-discretized-train.csv")  # Replace with your actual path

# Write the config file
writeConfigFile(DG, "../config/modelConfig.txt", "YourModelName")  # Replace with your actual path and model name

