import os, argparse
import numpy as np
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 9: Mirage Maintenance')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')

class Solver09(aoc_solver):
    def __init__(self):
        self.metrics = []
        self.predictions = []
        self.mode = ''

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.mode = mode
        self.predict_metrics()
        print('Sum of predictions:')
        print(f'{sum(self.predictions)}')

    def parse_input(self, input):
        with open(args.input, 'r') as f:
            content = f.readlines()
            for line in content:
                self.metrics.append([int(i) for i in line.strip().split(' ')])

    def predict_metrics(self):
        for metric in self.metrics:
            # print(f'{metric}')
            new_value = self.make_prediction(metric)
            self.predictions.append(new_value)

    def make_prediction(self, metric):
        differences = self.calculate_differences(metric)
        relation_found = False
        if sum(differences) == 0:
            relation_found = True
            for value in differences:
                if value > 0:
                    relation_found = False
                    break
        if relation_found:
            if self.mode == 'a':
                # new_value = metric[-1] + differences[-1]
                relation = differences[-1]
            if self.mode == 'b':
                # new_value = metric[0] + differences[0]
                relation = differences[0]
            # print(f'{differences}')
        else:
            # new_value = metric[-1] + self.make_prediction(differences)
            relation = self.make_prediction(differences)
        if self.mode == 'a':
            new_value = metric[-1] + relation
            # print(f'{metric} -> {new_value}')
        if self.mode == 'b':
            new_value = metric[0] - relation
            # print(f'{new_value} <- {metric}')
        return new_value

    def calculate_differences(self, values):
        differences = []
        for i in range(1, len(values)):
            differences.append(values[i] - values[i-1])
        return differences

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = Solver09()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
