import os, argparse
import numpy as np
import sys
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 10: Pipe Maze')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')
parser.add_argument('--show', help='Show map', action='store_true')

class Map:
    def __init__(self, input_map):
        self.size = input_map.shape 
        self.plot_cell_size = 3
        self.map = input_map
        self.plot = np.zeros((self.size[0] * self.plot_cell_size, 
                              self.size[1] * self.plot_cell_size, 3), dtype=np.uint8)

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
        if mode == 'a':
            self.time_multiplier = 2 - 1
        elif mode == 'b':
            self.time_multiplier = 1000000 - 1
        self.parse_input(input)
        galaxy_map = self.generate_galaxy_map(self.map_input)
        self.map = Map(galaxy_map)
        self.draw_map()
        self.plot_map(0)
        # self.expand_universe(mode)
        self.find_empty_space()
        self.find_galaxies()
        # self.draw_map()
        # self.plot_map(0)
        self.find_galaxy_paths()
        print('Number of galaxy pairs:')
        print(f'{len(self.path_lengths)}')
        print(f'Sum of path lengths:')
        print(f'{sum(self.path_lengths)}')

    def find_galaxies(self):
        map_size = self.map.size
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if self.map.map[i, j] > 0:
                    self.galaxies.append((i, j))

    def find_empty_space(self):
        self.empty_rows = []
        self.empty_columns = []
        map_size = self.map.size
        for i in range(map_size[0]):
            if sum(self.map.map[i, :]) == 0:
                # print(f'Inserting row {i}')
                self.empty_rows.append(i)
        for j in range(map_size[1]):
            if sum(self.map.map[:, j]) == 0:
                # print(f'Inserting column {j}')
                self.empty_columns.append(j)


    # def expand_universe(self, mode):
    #     map_size = self.map.size
    #     expanded_map = self.map.map.copy()
    #     if mode == 'a':
    #         n_spaces = 1
    #     elif mode == 'b':
    #         n_spaces = 1000000 - 1 
    #     self.empty_rows = []
    #     self.empty_columns = []

    #     insertions = 0
    #     new_space = np.zeros((n_spaces, map_size[1]), dtype=np.int)
    #     for i in range(map_size[0]):
    #         if sum(self.map.map[i, :]) == 0:
    #             print(f'Inserting row {i}')
    #             expanded_map = np.insert(expanded_map, i + insertions, new_space, axis=0)
    #             insertions += 1
    #     new_space = np.zeros((n_spaces, map_size[0] + insertions*n_spaces), dtype=np.int)
    #     insertions = 0
    #     for j in range(map_size[1]):
    #         if sum(self.map.map[:, j]) == 0:
    #             print(f'Inserting column {j}')
    #             expanded_map = np.insert(expanded_map, j + insertions*n_spaces, new_space, axis=1)
    #             insertions += 1
    #     self.map = Map(expanded_map)

    def find_galaxy_paths(self):
        for i in range(len(self.galaxies)):
            for j in range(i,len(self.galaxies)):
                if i == j:
                    continue
                galaxy_origin = self.galaxies[i]
                galaxy_destination = self.galaxies[j]
                distance = self.find_path_between_galaxy(galaxy_origin, galaxy_destination)
                # print(f'Galaxy {i} to {j}: {distance}')
                self.path_lengths.append(distance)

    def find_path_between_galaxy(self, galaxy_origin, galaxy_destination):
        # print(f'Finding path between {galaxy_origin} and {galaxy_destination}')
        manhattan_distance = abs(galaxy_origin[0] - galaxy_destination[0]) + abs(galaxy_origin[1] - galaxy_destination[1])
        # Find empty space rows and columns between galaxies
        min_row = min(galaxy_origin[0], galaxy_destination[0])
        max_row = max(galaxy_origin[0], galaxy_destination[0])
        min_column = min(galaxy_origin[1], galaxy_destination[1])
        max_column = max(galaxy_origin[1], galaxy_destination[1])
        for i in self.empty_rows:
            if i > min_row and i < max_row:
                # print(f'Found empty row {i}')
                manhattan_distance += self.time_multiplier
        for j in self.empty_columns:
            if j > min_column and j < max_column:
                # print(f'Found empty column {j}')
                manhattan_distance += self.time_multiplier 

        return manhattan_distance

    def generate_galaxy_map(self, input_map):
        galaxy_number = 1
        map_size = input_map.shape
        galaxy_map = np.zeros((map_size[0], map_size[1]), dtype=int)
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if self.map_input[i, j] == '#':
                    galaxy_map[i, j] = galaxy_number
                    galaxy_number += 1
        return galaxy_map

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

    def draw_map(self):
        map_size = self.map.size
        print(self.map.map)
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                self.draw_cell(i, j)

    def draw_cell(self, i, j, channel=0):
        if self.map.map[i, j] == 0:
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 1,
                    0] = 100 
        elif self.map.map[i, j] > 0:
            for k in range(0,2):
                self.map.plot[
                    i * self.map.plot_cell_size:(i+1) * self.map.plot_cell_size,
                    j * self.map.plot_cell_size:(j+1) * self.map.plot_cell_size,
                    k] = 255

    def plot_map(self, time=1):
        cv2.namedWindow('Map', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('Map', self.map.plot)
        cv2.waitKey(time)

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
