# Adapted from ConditionalIndependence.py from the workshops

# Import libraries
from causallearn.utils.cit import CIT


class Independence:
    """
    A class to handle independence tests on data using the Chi-Squared or G-Square tests.

    The class provides methods to read data, identify variable indices, and compute p-values for independence tests between variables.
    """

    def __init__(self, fileName: str):
        """
        A function to initialise the Independence object by reading in data from a CSV file.

        Parameters:
        - fileName (str): The path to the CSV file containing the data.
        """

        # Object to store the CIT instance
        self.chiSquaredObj = None
        # List to store the random variables from the dataset
        self.randomVariables = []
        # List to store all values of random variables
        self.randomVariablesAll = []
        # Flag to decide which test to use, Chi-Squared by default
        self.chiSquaredTest = True
        # Read the data from the CSV file
        data = self.readData(fileName)
        # Assign the test to be used
        test = "chisq" if self.chiSquaredTest else "gsq"
        # Initialise the CIT object
        self.chiSquaredObj = CIT(data, test)

    def readData(self, fileName: str):
        """
        A function to read and parse the datafile.

        Parameters:
        - fileName (str): The path to the CSV file containing the data.

        Returns:
        - (list of list): Data from the CSV file.
        """

        # Read each line from the CSV file
        with open(fileName) as csvFile:
            for line in csvFile:
                # Remove the leading/trailing whitespace
                line = line.strip()
                # Check if this is the first line
                if len(self.randomVariables) == 0:
                    # Assign the variable names
                    self.randomVariables = line.split(",")
                else:
                    # The remaining content is data
                    values = line.split(",")
                    self.randomVariablesAll.append(values)
        return self.randomVariablesAll

    def getVariableIndex(self, targetVariable: str):
        """
        A function to get the variable index of a given target variable.

        Parameters:
        - targetVariable (str): The name of the variable for which the index is being retrieved.

        Returns:
        - (int or None): The index of the target variable, or None if it's not found.
        """

        for i in range(0, len(self.randomVariables)):
            if self.randomVariables[i] == targetVariable:
                return i
        return None

    def getVariableIndices(self, parentVariables: list):
        """
        A function to get the variable indices of the given parent variables.

        Parameters:
        - parentVariables (list of str): The names of the parent variables.

        Returns:
        - (list of int or None): A list of indices for the given parent variables or None if the parentVariables list is empty.
        """

        if len(parentVariables) == 0:
            return None
        else:
            indexVector = []
            for parent in parentVariables:
                indexVector.append(self.getVariableIndex(parent))
            return indexVector

    def computePValue(self, x: str, y: str, z: list):
        """
        A function to compute the P value for a set of variables.

        Parameters:
        - x (str): The name of the first variable.
        - y (str): The name of the second variable.
        - z (list of str): The names of the conditioning variables.

        Returns:
        - (float): The computed P value.
        """

        varX = self.getVariableIndex(x)
        varY = self.getVariableIndex(y)
        parZ = self.getVariableIndices(z)
        # Execute the test
        p = self.chiSquaredObj(varX, varY, parZ)
        return p
