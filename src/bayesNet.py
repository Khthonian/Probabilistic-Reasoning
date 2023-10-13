# Import libraries
from sklearn.metrics import confusion_matrix, balanced_accuracy_score, roc_curve, auc, brier_score_loss, f1_score

import numpy as np
import pandas as pd

# Define a class for a naive Bayesian network
class NaiveBayes:
    def __init__(self, train, test, queries):
        # Read in the training and testing DataFrames
        self.train = pd.read_csv(train)
        self.test = pd.read_csv(test)
        # Dynamically find the target column
        self.target = self.train.columns[-1]
        # Store the user query
        self.queries = queries
        self.classProbs = None
        self.featureProbs = {}
        self.laplace = True
        self.laplacianConstant = 1

    # Define a function to train the model
    def trainNaiveBayes(self):
        # Assumes all features are conditionally independent given the class label
        self.classProbs = self.train[self.target].value_counts(normalize=True)
        self.featureProbs = {}
        for feature in self.train.columns[:-1]:
            self.featureProbs[feature] = self.train.groupby(self.target)[feature].value_counts(normalize=True)

    # Define a function to make predictions from the model
    def predict(self, instance):
        maxProb = 0
        bestClass = None
        for label, classProb in self.classProbs.items():
            prob = classProb
            for feature, value in instance.items():
                if self.laplace == True:
                    # Apply Laplacian smoothing
                    probability = self.featureProbs[feature][label].get(value, 0)
                    prior = np.sum(self.featureProbs[feature][label])
                    length = len(self.featureProbs[feature][label])
                    smoothedProb = (probability + self.laplacianConstant) / (prior + self.laplacianConstant * length)
                    prob *= smoothedProb
                else:
                    try:
                        prob *= self.featureProbs[feature][label][value]
                    except KeyError:
                        # Handle case when the feature-value pair has not been observed in the training data
                        prob = 0
            if prob > maxProb:
                maxProb = prob
                bestClass = label
        return bestClass

    # Define a function to evaluate the model performance
    def evaluate(self):
        yTrue = self.test[self.target].values
        yPred = [self.predict(self.test.iloc[i].drop(self.target).to_dict()) for i in range(len(self.test))]
        cm = confusion_matrix(yTrue, yPred)
        balancedAcc = balanced_accuracy_score(yTrue, yPred)
        fpr, tpr, _ = roc_curve(yTrue, yPred)
        rocAuc = auc(fpr, tpr)
        brierScore = brier_score_loss(yTrue, yPred)
        f1 = f1_score(yTrue, yPred)
        return {
            'Confusion Matrix': cm,
            'Balanced Accuracy': balancedAcc,
            'AUC': rocAuc,
            'Brier Score': brierScore,
            'F1 Score': f1
        }
    
    # Define a function to parse the user query
    def parseQuery(self, queryStr):
        queryVars = {}
        try:
            # Remove 'P(' and ')' from the query string
            queryStr = queryStr[2:-1]
            
            # Extract the target and conditions from the query string
            targetStr, conditionsStr = queryStr.split('|')
            targetVar, targetValue = targetStr.split('=')
            
            # Parse the multiple conditionals
            conditionals = conditionsStr.split(',')
            
            for conditional in conditionals:
                var, value = conditional.split('=')
                queryVars[var.strip()] = int(value.strip())
            
            # Add the target variable to the queryVars dictionary
            queryVars[targetVar.strip()] = int(targetValue.strip())
            
        except Exception as e:
            print(f"Invalid query format. Please use the format: P(target=x|var1=y,var2=z,...) \nError: {e}")
        return queryVars

    # Define a function to predict the user query
    def predictProb(self, instance):
        probPerClass = {}
        for label, classProb in self.classProbs.items():
            prob = classProb
            for feature, value in instance.items():
                if self.laplace == True:
                    # Apply Laplacian smoothing in compact form
                    probability = self.featureProbs[feature][label].get(value, 0)
                    prior = np.sum(self.featureProbs[feature][label])
                    length = len(self.featureProbs[feature][label])
                    smoothedProb = (probability + self.laplacianConstant) / (prior + self.laplacianConstant * length)
                    prob *= smoothedProb
                else:
                    try:
                        prob *= self.featureProbs[feature][label][value]
                    except KeyError:
                        # Handle case when the feature-value pair has not been observed in the training data
                        prob = 0
            probPerClass[label] = prob
        return probPerClass

    # Define a function to run the user query
    def runQueries(self):
        results = {}
        for queryStr in self.queries:
            queryVars = self.parseQuery(queryStr)
            if queryVars:
                targetVarValue = queryVars.pop(self.target, None)
                probPerClass = self.predictProb(queryVars)
                results[queryStr] = probPerClass.get(targetVarValue, 0)
        return results
