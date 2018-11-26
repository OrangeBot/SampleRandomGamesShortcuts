#!pythonn
from __future__ import print_function
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--a', required=True)
parser.add_argument('--b', default='Hello World')

args = parser.parse_args()
def test(a, b="Hello World"):
    print(a, b)

if __name__ == "__main__":
    result = test(args.a, args.b)
    if result is not None:
        print(result)
