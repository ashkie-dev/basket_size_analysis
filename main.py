from .scripts import analysis_helpers, analyze
import argparse


parser = argparse.ArgumentParser(
    description='Create a report detailing which products a customer is most likely to purchase together')
parser.add_argument('-f', '--file', type=str, help='')
parser.add_argument('-s', '--string', type=str)
parser.add_argument('-m', '-multi', type=str, nargs='+')

args = parser.parse_args()


if __name__ == "__main__":
    print('')


# <-----------------------EXAMPLE PARSER----------------------->

# parser = argparse.ArgumentParser(description='Create barcodes from excel file')
# parser.add_argument('-f', type=str)
# parser.add_argument('-s', type=str)
# parser.add_argument('-m', '-multiple', type=str, nargs='+')

# args = parser.parse_args()
