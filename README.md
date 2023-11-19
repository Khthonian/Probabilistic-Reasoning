# Probabilistic-Reasoning
A software application designed to solve medical diagnostic problems by performing probabilistic reasoning from data.

## Configuration File Generation
The main script, `main.py`, uses an argument parser from `parse.py` to dynamically select the output. The flags that can be used are:
- `-c` | `--cardio`: Use cardiovascular dataset.
- `-d` | `--diabetes`: Use diabetes dataset.
- `-C` | `--continuous`: Use continuous data.
- `-n` | `--naive`: Use a naive structure.
- `-s` | `--score`: Calculate LL and BIC scores.
- `-g` | `--graph`: Display the structure graph.

## Structure Learning
This application offers two options for generating a structure for the given data:
- Naive structure generation
- PC-Stable structure learning

Both of these options utilise the `networkx` library to manage the structure of the directed acyclic graphs and the nodes within.

## Usage
When using the Bayesian networks, use the `main.py` script first to setup the configuration file, then apply the configuration file and data with the inference models or model evaluator.

### Example
```
# Running the main script, selecting the diabetes dataset, and opting to display the graph and structure scores
python main.py -dgs

# Applying inference by enumeration to the generated configuration file and data
python BayesNetInference.py InferenceByEnumeration ../config/modelConfig.txt "P(Outcome|BMI=3,Pregnancies=4)"
```

### `BayesNetInference.py`
The `BayesNetInference.py` script can only be applied to non-Gaussian structures.

## Video
The video can be found in the `task` directory.

## Source Code 
The source code can also be found at https://github.com/Khthonian/Probabilistic-Reasoning.


