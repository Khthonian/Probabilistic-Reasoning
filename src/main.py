# Import libraries
import argparse
import causallearn

# Import Bayes class
from bayesNet import NaiveBayes

# Data switch variables
gaussian = True

trainSet = ""
testSet = ""

# Create a parser object
parser = argparse.ArgumentParser(description="Your program description here")

# Create a mutually exclusive group for flags (-d and -c)
flagGroup = parser.add_mutually_exclusive_group(required=True)
flagGroup.add_argument("-d", action="store_true", help="Use discrete data")
flagGroup.add_argument("-c", action="store_true", help="Use continuous data")

# Create a mutually exclusive group for commands (diabetes and cardio)
commandGroup = parser.add_mutually_exclusive_group(required=True)
commandGroup.add_argument("--diabetes", action="store_true", help="Specify the diabetes command")
commandGroup.add_argument("--cardio", action="store_true", help="Specify the cardio command")

# Define the mandatory query argument
parser.add_argument("query", help="Mandatory query")

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
useDiscrete = args.d
useContinuous = args.c
diabetesCommand = args.diabetes
cardioCommand = args.cardio
query = args.query

# Check the flags and commands
if useDiscrete:
    print("You chose to use discrete data.")    
elif useContinuous:
    print("You chose to use continuous data.")
    gaussian = False

if diabetesCommand:
    print("You chose the diabetes dataset")
    if not gaussian:
        trainSet = "../data/diabetes_data-original-train.csv"
        testSet = "../data/diabetes_data-original-test.csv"
    else:
        trainSet = "../data/diabetes_data-discretized-train.csv"
        testSet = "../data/diabetes_data-discretized-test.csv"
elif cardioCommand:
    print("You chose the cardiovascular dataset")
    if not gaussian:
        trainSet = "../data/cardiovascular_data-original-train.csv"
        testSet = "../data/cardiovascular_data-original-test.csv"
    else:
        trainSet = "../data/cardiovascular_data-discretized-train.csv"
        testSet = "../data/cardiovascular_data-discretized-test.csv"

# Perform actions based on the mandatory query
print("Your query:", query)

print("Training set location: " + trainSet)
print("Testing set location: " + testSet)


# Create NaiveBayes object
naiveBayes = NaiveBayes(trainSet, testSet, [args.query])

# Train the NaiveBayes model
naiveBayes.trainNaiveBayes()

# Evaluate the model
metrics = naiveBayes.evaluate()
print(f"Evaluation Metrics: {metrics}")

# Run the query
queryResults = naiveBayes.runQueries()
print(f"Query Results: {queryResults}")
