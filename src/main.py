# Import libraries
from configGenerator import generateConfig
from cleanBOM import cleanBOM
from parse import createParser


# Declare the path of the config file
configFile = "../config/modelConfig.txt"


def selectData(useContinuous: bool, useDiabetes: bool, useCardio: bool):
    # Declare variables to store dataset paths
    trainSet, testSet, modelName = None

    # Select dataset
    if useDiabetes:
        print("You chose the diabetes dataset")
        if not useContinuous:
            trainSet = "../data/diabetes_data-original-train.csv"
            testSet = "../data/diabetes_data-original-test.csv"
        else:
            trainSet = "../data/diabetes_data-discretized-train.csv"
            testSet = "../data/diabetes_data-discretized-test.csv"
        modelName = "Diabetes Model"
    elif useCardio:
        print("You chose the cardiovascular dataset")
        if not useContinuous:
            trainSet = "../data/cardiovascular_data-original-train.csv"
            testSet = "../data/cardiovascular_data-original-test.csv"
        else:
            trainSet = "../data/cardiovascular_data-discretized-train.csv"
            testSet = "../data/cardiovascular_data-discretized-test.csv"
        modelName = "Cardiovascular Model"

    # Clean BOM from train/test set
    cleanBOM(trainSet)
    cleanBOM(testSet)

    return trainSet, testSet, modelName


def main():
    # Create a parser object
    parser = createParser()

    # Parse the CLI arguments
    args = parser.parse_args()

    # Access the values of the arguments
    useGaussian = args.g
    useInferEnumerate = args.i
    useRejection = args.r
    useCardio = args.c
    useDiabetes = args.d
    useContinuous = args.C
    useNaive = args.n
    useScore = args.s

    # Declare a variable for the query
    query = None

    # Check the flags
    if useGaussian or useInferEnumerate or useRejection:
        query = input("Enter a query e.g. P(X|A,B): ")
        print("Your query: ", query)

    # Select datasets
    trainSet, testSet, modelName = selectData(
        useContinuous, useDiabetes, useCardio)
    print("Train set path: " + trainSet)
    print("Test set path: " + testSet)

    # Generate model
    generateConfig(trainSet, modelName, useNaive, useScore)

    # Select CPT or PDF generation
    if useGaussian:
        # Insert logic to run PDF generator
    else:
        # Insert logic to run CPT generator

        # TODO: Implement logic for inferences and model evaluation
