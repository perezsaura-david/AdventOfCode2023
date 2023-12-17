import os, argparse
import numpy as np
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 8: Haunted Wasteland')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')

class Solver08(aoc_solver):
    def __init__(self):
        self.nodes = {}
        self.instructions = []
        self.start = 'AAA'
        self.end = 'ZZZ'
        self.end_reached = False
        self.number_of_steps = 0

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        if mode == 'a':
            self.number_of_steps = self.navigate(self.start, mode)
        if mode == 'b':
            self.number_of_steps = self.navigate_like_a_ghost()
        print('Number of steps:')
        print(f'{self.number_of_steps}')

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            content = f.readlines()
            instructions = content[0].strip()
            for c in instructions:
                if c == 'L':
                    self.instructions.append(0)
                if c == 'R':
                    self.instructions.append(1)
            # print(self.instructions)

            for i in range(2,len(content)):
                line = content[i].strip()
                if line == '\n':
                    continue
                line = line.split('=')
                node_id = line[0].strip()
                node_content = ''
                for c in line[1]:
                    if c == ' ':
                        continue
                    if c == '(':
                        continue
                    if c == ')':
                        continue
                    node_content += c
                node_values = node_content.split(',')
                self.nodes[node_id] = node_values
        # print(self.nodes)

    def navigate(self, start, mode):
        current_node = start
        end_reached = False
        number_of_steps = 0
        # print('STARTING', current_node)
        while not end_reached:
            for instruction in self.instructions:
                number_of_steps += 1
                current_node = self.nodes[current_node][instruction]
                # print(f'{current_node=}')
                if self.check_end_reached(current_node, mode):
                    end_reached = True
                    break
        return number_of_steps

    def check_end_reached(self, current_node, mode):
        if mode == 'a':
            if current_node == self.end:
                return True
        if mode == 'b':
            if current_node[-1] == 'Z':
                return True
        return False

    def navigate_like_a_ghost(self):
        starting_nodes = self.find_all_starting_nodes()
        steps_per_path = []
        for node in starting_nodes:
            number_of_steps = self.navigate(node, 'b')
            steps_per_path.append(number_of_steps)
        print(f'{steps_per_path=}')
        steps_array = np.array(steps_per_path)
        mcm = np.lcm.reduce(steps_array)
        return mcm

    def find_all_starting_nodes(self):
        starting_nodes = []
        for node in self.nodes:
            # if node ends with A 
            if node[-1] == 'A':
                starting_nodes.append(node)
        return starting_nodes

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = Solver08()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
