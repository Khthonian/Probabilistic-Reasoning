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
