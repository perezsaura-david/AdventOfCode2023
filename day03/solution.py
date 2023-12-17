import os, argparse
import numpy as np
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 3: Gear Ratios')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')

class solver03(aoc_solver):
    def __init__(self):
        self.content = None
        self.content_array = None
        self.map = None
        self.digit_list = []
        self.valid_numbers = []
        self.sum_of_valid_numbers = 0
        self.gear_ratios = []
        self.sum_of_gear_ratios = 0

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.extract_info(mode)
        if mode == 'a':
            self.find_valid_numbers()
            # print(f'Valid numbers: {self.valid_numbers}')
            sum_of_valid_numbers = sum(self.valid_numbers)
            print(f'Sum of valid numbers: {sum_of_valid_numbers}')
            return sum_of_valid_numbers
        elif mode == 'b':
            self.find_gear_ratios()
            # print(f'Gear ratios: {self.gear_ratios}')
            self.sum_of_gear_ratios = sum(self.gear_ratios)
            print(f'Sum of gear ratios: {self.sum_of_gear_ratios}')

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            content = []
            for line in f:
                line = line.strip()
                char_list = []
                for char in line:
                    char_list.append(char)
                content.append(char_list)
            self.content_array = np.asarray(content)

    def extract_info(self, mode):
        # self.digit_map = np.zeros((self.content_array.shape[0], self.content_array.shape[1]))
        self.symbol_map = np.zeros((self.content_array.shape[0], self.content_array.shape[1]))
        for i in range(self.content_array.shape[0]):
            creating_digit = False
            digit = ''
            digit_pos = []
            for j in range(self.content_array.shape[1]):
                if self.content_array[i][j].isdigit():
                    creating_digit = True
                    digit += self.content_array[i][j]
                    digit_pos.append((i,j))
                else:
                    if mode == 'a':
                        if self.content_array[i][j] != '.':
                            self.symbol_map[i][j] = 1
                    if mode == 'b':
                        if self.content_array[i][j] == '*':
                            self.symbol_map[i][j] = 1
                    if creating_digit:
                        self.add_digit(digit, digit_pos)
                        creating_digit = False
                        digit = ''
                        digit_pos = []
                        
            # END OF LINE
            if creating_digit:
                self.add_digit(digit, digit_pos)
                creating_digit = False
                digit = ''
                digit_pos = []

    def add_digit(self, digit, digit_pos):
        self.digit_list.append((int(digit), digit_pos))

    def find_valid_numbers(self):
        for digit_info in self.digit_list:
            digit = digit_info[0]
            digit_pos = digit_info[1]
            if self.check_digit_sorrundings(digit_pos):
                self.valid_numbers.append(digit)

    def check_digit_sorrundings(self, digit_positions):
        digit_x = digit_positions[0][0]
        digit_y_limits = [digit_positions[0][1], digit_positions[-1][1]]
        
        for i in range(digit_x-1, digit_x+2):
            if i < 0 or i >= self.symbol_map.shape[0]:
                continue
            for j in range(digit_y_limits[0]-1, digit_y_limits[1]+2):
                if i < 0 or j < 0 or i >= self.symbol_map.shape[0] or j >= self.symbol_map.shape[1]:
                    continue
                if self.symbol_map[i][j] == 1:
                    return True
        return False

    def check_gear_sorrundings(self, gear_positions):
        gear_ratio = 0
        gear_numbers = []
        for i in range(gear_positions[0]-1, gear_positions[0]+2):
            if i < 0 or i >= self.symbol_map.shape[0]:
                continue
            for j in range(gear_positions[1]-1, gear_positions[1]+2):
                if i < 0 or j < 0 or i >= self.symbol_map.shape[0] or j >= self.symbol_map.shape[1]:
                    continue
                digit_found = False
                for digit, digit_positions in self.digit_list:
                    if digit in gear_numbers:
                        continue
                    for digit_pos in digit_positions:
                        if digit_pos == (i,j):
                            gear_numbers.append(digit)
                            break
        if len(gear_numbers) == 2:
            gear_ratio = gear_numbers[0] * gear_numbers[1]
            self.gear_ratios.append(gear_ratio)

    def find_gear_ratios(self):
        for i in range(self.symbol_map.shape[0]):
            for j in range(self.symbol_map.shape[1]):
                if self.symbol_map[i][j] == 1:
                    self.check_gear_sorrundings((i,j))

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = solver03()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
