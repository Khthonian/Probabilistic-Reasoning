# Import libraries
import argparse


def createParser():
    # Create a parser object
    parser = argparse.ArgumentParser()

    # Create a mutually exclusive group for inference methods
    inferenceGroup = parser.add_mutually_exclusive_group(required=False)
    # Create a flag for Gaussian processing, -g
    inferenceGroup.add_argument(
        "-g", action="store_true", help="Use Gaussian Processes.")
    # Create a flag for inference by enumeration
    inferenceGroup.add_argument(
        "-i", action="store_true", help="Use Inference By Enumeration.")
    # Create a flag for rejection sampling
    inferenceGroup.add_argument(
        "-r", action="store_true", help="Use Rejection Sampling.")

    # Create a mutually exclusive group for datasets
    dataGroup = parser.add_mutually_exclusive_group(required=True)
    # Create a flag for the cardiovascular dataset
    dataGroup.add_argument("-c", action="store_true",
                           help="Use cardiovascular dataset.")
    # Create a flag for the diabetes dataset
    dataGroup.add_argument("-d", action="store_true",
                           help="Use diabetes dataset.")

    # Create a flag for continuous data
    parser.add_argument("-C", action="store_true", help="Use continuous data.")

    # Create a flag for naive structure generation
    parser.add_argument("-n", action="store_true",
                        help="Use a naive structure.")

    # Create a flag for calculating LL and BIC scores
    parser.add_argument("-s", action="store_true",
                        help="Calculate LL and BIC scores.")

    return parser
