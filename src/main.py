# Import libraries
import argparse

# Import Bayes class
from bayesNet import NaiveBayes

# Data switch variables
discrete = True

trainSet = ""
testSet = ""

# Create a parser object
parser = argparse.ArgumentParser(description="Your program description here")

# Create a mutually exclusive group for flags (-d and -c)
flag_group = parser.add_mutually_exclusive_group(required=True)
flag_group.add_argument("-d", action="store_true", help="Use discrete data")
flag_group.add_argument("-c", action="store_true", help="Use continuous data")

# Create a mutually exclusive group for commands (diabetes and cardio)
command_group = parser.add_mutually_exclusive_group(required=True)
command_group.add_argument("--diabetes", action="store_true", help="Specify the diabetes command")
command_group.add_argument("--cardio", action="store_true", help="Specify the cardio command")

# Define the mandatory query argument
parser.add_argument("query", help="Mandatory query")

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
use_discrete = args.d
use_continuous = args.c
diabetes_command = args.diabetes
cardio_command = args.cardio
query = args.query

# Check the flags and commands
if use_discrete:
    print("You chose to use discrete data.")    
elif use_continuous:
    print("You chose to use continuous data.")
    discrete = False

if diabetes_command:
    print("You chose the diabetes dataset")
    if not discrete:
        trainSet = "../data/diabetes_data-original-train.csv"
        testSet = "../data/diabetes_data-original-test.csv"
    else:
        trainSet = "../data/diabetes_data-discretized-train.csv"
        testSet = "../data/diabetes_data-discretized-test.csv"
elif cardio_command:
    print("You chose the cardiovascular dataset")
    if not discrete:
        trainSet = "../data/cardiovascular_data-original-train.csv"
        testSet = "../data/cardiovascular_data-original-test.csv"
    else:
        trainSet = "../data/cardiovascular_data-discretized-train.csv"
        testSet = "../data/cardiovascular_data-discretized-test.csv"

# Perform actions based on the mandatory query
print("Your query:", query)

print(trainSet)
print(testSet)
