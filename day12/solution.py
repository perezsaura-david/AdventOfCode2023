import os, argparse
import numpy as np
import sys
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 12: Hot Springs') 
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')
parser.add_argument('--show', help='Show map', action='store_true')

class Solver10(aoc_solver):
    def __init__(self):
        self.mode = ''
        self.map = None
        self.map_size = [0, 0]
        self.map_input = None
        self.galaxy_map = None
        self.galaxies = []
        self.path_lengths = []
        self.empty_rows = []
        self.empty_columns = []
        self.time_multiplier = 1

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        # if mode == 'a':
        # elif mode == 'b':
        self.parse_input(input)
        # print('Number of galaxy pairs:')
        # print(f'{len(self.path_lengths)}')
        # print(f'Sum of path lengths:')
        # print(f'{sum(self.path_lengths)}')

    def parse_input(self, input):
        with open(args.input, 'r') as f:
            content = f.readlines()
            self.map_size[0] = len(content)
            self.map_size[1] = len(content[0].strip())
            self.map_input = np.zeros((self.map_size[0], self.map_size[1]), dtype=np.chararray)
            for i in range(self.map_size[0]):
                line = content[i].strip()
                for j in range(len(line)):
                    self.map_input[i, j] = line[j]

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = Solver10()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
