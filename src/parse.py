# Import libraries
import argparse


def createParser():
    # Create a parser object
    parser = argparse.ArgumentParser()

    # Create a mutually exclusive group for datasets
    dataGroup = parser.add_mutually_exclusive_group(required=True)
    # Create a flag for the cardiovascular dataset
    dataGroup.add_argument("-c", "--cardio", action="store_true",
                           help="Use cardiovascular dataset.")
    # Create a flag for the diabetes dataset
    dataGroup.add_argument("-d", "--diabetes", action="store_true",
                           help="Use diabetes dataset.")

    # Create a flag for continuous data
    parser.add_argument("-C", "--continuous",
                        action="store_true", help="Use continuous data.")

    # Create a flag for naive structure generation
    parser.add_argument("-n", "--naive", action="store_true",
                        help="Use a naive structure.")

    # Create a flag for calculating LL and BIC scores
    parser.add_argument("-s", "--score", action="store_true",
                        help="Calculate LL and BIC scores.")

    return parser
