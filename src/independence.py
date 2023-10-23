# Adapted from ConditionalIndependence.py from the workshops

# Import libraries
from causallearn.utils.cit import CIT

class Independence:
    # Object to store the CIT instance
    chiSquaredObj = None
    # List to store the random variables from the dataset
    randomVariables = []
    # List to store all values of random variables
    randomVariablesAll = []
    # Flag to decide which test to use, Chi Squared by default
    chiSquaredTest = True

    def __init__(self, fileName):
        # Read the data from the CSV file
        data = self.readData(fileName)
        # Assign the test to be used
        test = "chisq" if self.chiSquaredTest else "gsq"
        # Initialise the CIT object
        self.chiSquaredObj = CIT(data, test)

    def readData(self, fileName):
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

    def getVariableIndex(self, targetVariable):
        for i in range(0, len(self.randomVariables)):
            if self.randomVariables[i] == targetVariable:
                return i
        return None

    def getVariableIndices(self, parentVariables):
        if len(parentVariables) == 0:
            return None
        else:
            indexVector = []
            for parent in parentVariables:
                indexVector.append(self.getVariableIndex(parent))
            return indexVector

    def computePValue(self, x, y, z):
        varX = self.getVariableIndex(x)
        varY = self.getVariableIndex(y)
        parZ = self.getVariableIndices(z)
        # Execute the test
        p = self.chiSquaredObj(varX, varY, parZ)
        return p
