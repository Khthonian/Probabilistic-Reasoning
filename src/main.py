# Import libraries
from cleanBOM import cleanBOM
from configGenerator import generateConfig
from CPT_Generator import CPT_Generator
from parse import createParser
from PDF_Generator import PDF_Generator

import time


def selectData(useContinuous: bool, useDiabetes: bool, useCardio: bool):
    # Declare variables to store dataset paths
    trainSet, testSet, modelName = (None, None, None)

    # Select dataset
    if useDiabetes:
        print("You chose the diabetes dataset")
        if useContinuous:
            trainSet = "../data/diabetes_data-original-train.csv"
            testSet = "../data/diabetes_data-original-test.csv"
            modelName = "Original Diabetes Model"
        else:
            trainSet = "../data/diabetes_data-discretized-train.csv"
            testSet = "../data/diabetes_data-discretized-test.csv"
            modelName = "Discretised Diabetes Model"
    elif useCardio:
        print("You chose the cardiovascular dataset")
        if useContinuous:
            trainSet = "../data/cardiovascular_data-original-train.csv"
            testSet = "../data/cardiovascular_data-original-test.csv"
            modelName = "Original Cardiovascular Model"
        else:
            trainSet = "../data/cardiovascular_data-discretized-train.csv"
            testSet = "../data/cardiovascular_data-discretized-test.csv"
            modelName = "Discretised Cardiovascular Model"

    # Clean BOM from train/test set
    cleanBOM(trainSet)
    cleanBOM(testSet)

    return trainSet, testSet, modelName


def main():
    configFile = "../config/modelConfig.txt"

    # Create a parser object
    parser = createParser()

    # Parse the CLI arguments
    args = parser.parse_args()

    # Access the values of the arguments
    useCardio = args.cardio
    useDiabetes = args.diabetes
    useContinuous = args.continuous
    useNaive = args.naive
    useScore = args.score
    useGraph = args.graph

    # Select datasets
    trainSet, testSet, modelName = selectData(
        useContinuous, useDiabetes, useCardio)
    print("Train set path: " + trainSet)
    print("Test set path: " + testSet)

    # Generate model
    LL, BIC = generateConfig(configFile, trainSet, modelName, useNaive, useScore, useGraph)

    # Declare training time variables
    startTime, endTime = (None, None)

    # Select CPT or PDF generation
    print(useContinuous)
    if useContinuous:
        startTime = time.time()
        PDF_Generator(configFile, trainSet)
        endTime = time.time()
    else:
        startTime = time.time()
        CPT_Generator(configFile, trainSet)
        endTime = time.time()

    executeTime = endTime - startTime
    print("Training Time: ", executeTime, " seconds")
    if useScore:
        print("LL Score: ", LL)
        print("BIC Score: ", BIC)


if __name__ == "__main__":
    main()
