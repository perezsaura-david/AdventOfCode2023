import os, argparse
import numpy as np
import sys
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 11: Cosmic Expansion')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')
parser.add_argument('--show', help='Show map', action='store_true')

class Map:
    def __init__(self, size):
        self.size = size
        self.plot_cell_size = 3
        self.map = np.zeros((size[0], size[1], 1), dtype=np.uint8)
        self.plot = np.zeros((size[0] * self.plot_cell_size, size[1] * self.plot_cell_size, 3), dtype=np.uint8)

class Solver09(aoc_solver):
    def __init__(self):
        self.mode = ''
        self.map = None
        self.map_size = [0, 0]
        self.map_input = None
        self.start = [0, 0]
        self.up = ['|', '7', 'F']
        self.down = ['|', 'J', 'L']
        self.left = ['-', 'F', 'L']
        self.right = ['-', 'J', '7']
        self.pipe = []
        # self.connections = [0, 0, 0, 0]

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.map = Map(self.map_size)
        self.draw_map()
        self.find_start_pipe()
        self.draw_cell(self.start[0], self.start[1], 2)
        self.draw_cell(self.start[0], self.start[1], 1)
        self.plot_map(0)
        self.browse_pipe(mode)
        self.plot_map(0)
        if mode == 'b':
            self.find_enclosed_area()
            self.plot_map(0)

    def find_enclosed_area(self):
        self.find_spaces()
        area = self.find_enclosed_cells()
        # external_area = self.find_external_area()
        print(f'Map area: {self.map_size[0] * self.map_size[1]}')
        print(f'Pipe area: {len(self.pipe)}')
        print(f'Area: {area}')
        print('Remaining area:')
        remaining_area = self.map_size[0] * self.map_size[1] - len(self.pipe) - area
        print(f'{remaining_area}')

    def find_enclosed_cells(self):
        found_area = 0
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                cell_centre = [
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 1]
                if self.map.plot[cell_centre[0], cell_centre[1]][2] == 150: 
                    found_area += 1
        return found_area

    def find_spaces(self):
        map_size = self.map.plot.shape
        start_node = [0, 0]
        start_node = [map_size[0] // 2, map_size[1] // 2]
        visited_area = []
        nodes_to_visit = [start_node]
        while True:
            current_node = nodes_to_visit[0]
            # print(f'Current node: {current_node}')
            self.map.plot[current_node[0], current_node[1]] = [0, 0, 150]
            # self.draw_cell(current_node[0], current_node[1], 2)
            if args.show:
                self.plot_map(1)

            visited_area.append(current_node)
            nodes_to_visit.remove(current_node)
            nodes_to_visit.extend(self.find_next_point(current_node, visited_area, nodes_to_visit))
            # print(f'Nodes to visit: {nodes_to_visit}')
            if nodes_to_visit == []:
                break

    def find_next_point(self, current_node, visited_area, nodes_to_visit):
        candidates = []
        limits = [self.map.plot.shape[0], self.map.plot.shape[1]]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                candidate = [current_node[0] + i, current_node[1] + j]
                if candidate[0] < 0 or candidate[0] >= limits[0]:
                    continue
                if candidate[1] < 0 or candidate[1] >= limits[1]:
                    continue
                if candidate in visited_area:
                    continue
                if candidate in nodes_to_visit:
                    continue
                # print(f'Candidate: {candidate}')
                if self.map.plot[candidate[0],candidate[1]][1] == 255:
                    continue
                # if candidate in self.pipe:
                #     continue
                candidates.append(candidate)
        return candidates


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
                    if line[j] == 'S':
                        self.start = [i, j]

    def find_start_pipe(self):
        connections = [0, 0, 0, 0]
        if self.map_input[self.start[0] - 1, self.start[1]] in self.up:
            connections[0] = 1
        if self.map_input[self.start[0] + 1, self.start[1]] in self.down:
            connections[2] = 1
        if self.map_input[self.start[0], self.start[1] - 1] in self.left:
            connections[3] = 1
        if self.map_input[self.start[0], self.start[1] + 1] in self.right:
            connections[1] = 1

        if connections[0] + connections[1] + connections[2] + connections[3] != 2:
            print('Start pipe has more than 2 connections')
            return
        
        if connections[0] == 1:
            if connections[1] == 1:
                self.map_input[self.start[0], self.start[1]] = 'L'
            elif connections[2] == 1:
                self.map_input[self.start[0], self.start[1]] = '|'
            elif connections[3] == 1:
                self.map_input[self.start[0], self.start[1]] = 'J'
        elif connections[2] == 1:
            if connections[1] == 1:
                self.map_input[self.start[0], self.start[1]] = 'F'
            elif connections[3] == 1:
                self.map_input[self.start[0], self.start[1]] = '7'
        elif connections[1] + connections[3] == 2:
            self.map_input[self.start[0], self.start[1]] = '-'
        # print(connections)
        print('Start pipe is:')
        print(self.map_input[self.start[0], self.start[1]])
        # self.connections = connections

    def browse_pipe(self, mode):
        map_start = self.start 
        current_nodes = []
        path_nodes = []
        for i in range(2):
            path_nodes.append([map_start])
            current_nodes.append(self.find_next_node(map_start, current_nodes))
        print('*** Browsing pipe ***')
        while True:
            if current_nodes[0] == current_nodes[1]:
                print(f'Found end of pipe at {current_nodes[0]}, {current_nodes[1]}')
                print('Path 0 length:', len(path_nodes[0]))
                print('Path 1 length:', len(path_nodes[1]))
                self.draw_cell(current_nodes[0][0], current_nodes[0][1], 1)
                self.draw_cell(current_nodes[0][0], current_nodes[0][1], 2)
                print('End of pipe')
                break
            for i in range(len(current_nodes)):
                self.draw_cell(current_nodes[i][0], current_nodes[i][1], 1)
                if args.show:
                    self.plot_map()
                path_nodes[i].append(current_nodes[i])
                node = current_nodes[i]
                current_nodes[i] = self.find_next_node(node, path_nodes[i])
        if mode == 'b':
            self.pipe.append(current_nodes[0])
            for i in range(len(path_nodes)):
                for j in range(len(path_nodes[i])):
                    if path_nodes[i][j] not in self.pipe:
                        self.pipe.append(path_nodes[i][j])


    def find_next_node(self, node, path):
        step_list = []
        step = [0, 0]
        # print('Finding next node')
        if self.map_input[node[0], node[1]] == '|':
            step_list.append([-1, 0])
            step_list.append([1, 0])
        elif self.map_input[node[0], node[1]] == '-':
            step_list.append([0, -1])
            step_list.append([0, 1])
        elif self.map_input[node[0], node[1]] == '7':
            step_list.append([1, 0])
            step_list.append([0, -1])
        elif self.map_input[node[0], node[1]] == 'J':
            step_list.append([0, -1])
            step_list.append([-1, 0])
        elif self.map_input[node[0], node[1]] == 'L':
            step_list.append([0, 1])
            step_list.append([-1, 0])
        elif self.map_input[node[0], node[1]] == 'F':
            step_list.append([0, 1])
            step_list.append([1, 0])
        for i in range(len(step_list)):
            step = step_list[i]
            next_node = [node[0] + step[0], node[1] + step[1]]
            if next_node not in path:
                return next_node


    def draw_map(self):
        print(self.map_input)
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self.draw_cell(i, j)

    def draw_cell(self, i, j, channel=0):
        if self.map_input[i, j] == '|':
            self.map.plot[
                    i * self.map.plot_cell_size:(i + 1) * self.map.plot_cell_size,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
        elif self.map_input[i, j] == '-':
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size:(j + 1) * self.map.plot_cell_size,
                    channel] = 255
        elif self.map_input[i, j] == 'L':
            self.map.plot[
                    i * self.map.plot_cell_size:i * self.map.plot_cell_size + 2,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 2:(j+1) * self.map.plot_cell_size,
                    channel] = 255
        elif self.map_input[i, j] == 'J':
            self.map.plot[
                    i * self.map.plot_cell_size:i * self.map.plot_cell_size + 2,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size:j * self.map.plot_cell_size + 2,
                    channel] = 255
        elif self.map_input[i, j] == '7':
            self.map.plot[
                    i * self.map.plot_cell_size + 2:(i+1) * self.map.plot_cell_size,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size:j * self.map.plot_cell_size + 2,
                    channel] = 255
        elif self.map_input[i, j] == 'F':
            self.map.plot[
                    i * self.map.plot_cell_size + 2:(i+1) * self.map.plot_cell_size,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 1:(j+1) * self.map.plot_cell_size,
                    channel] = 255
        elif self.map_input[i, j] == '.':
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 1,
                    channel] = 255
        elif self.map_input[i, j] == 'S':
            self.map.plot[
                    i * self.map.plot_cell_size + 1,
                    j * self.map.plot_cell_size + 1,
                    2] = 255

    def plot_map(self, time=1):
        cv2.namedWindow('Map', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('Map', self.map.plot)
        cv2.waitKey(time)

    # def find_external_area_extend(self):
    #     start_node = [0, 0]
    #     # start_node = [self.map_size[0]//2, self.map_size[1]//2]
    #     visited_area = []
    #     nodes_to_visit = [start_node]
    #     while True:
    #         current_node = nodes_to_visit[0]
    #         # print(f'Current node: {current_node}')
    #         self.draw_cell(current_node[0], current_node[1], 2)
    #         self.plot_map(1)

    #         visited_area.append(current_node)
    #         nodes_to_visit.remove(current_node)
    #         nodes_to_visit.extend(self.find_next_out_node(current_node, visited_area, nodes_to_visit))
    #         # print(f'Nodes to visit: {nodes_to_visit}')
    #         if nodes_to_visit == []:
    #             break

    #     return len(visited_area)

    # def find_next_out_node(self, current_node, visited_area, nodes_to_visit):
    #     candidates = []
    #     for i in range(-1, 2):
    #         for j in range(-1, 2):
    #             if i == 0 and j == 0:
    #                 continue
    #             candidate = [current_node[0] + i, current_node[1] + j]
    #             if candidate[0] < 0 or candidate[0] >= self.map_size[0]:
    #                 continue
    #             if candidate[1] < 0 or candidate[1] >= self.map_size[1]:
    #                 continue
    #             if candidate in visited_area:
    #                 continue
    #             if candidate in nodes_to_visit:
    #                 continue
    #             if candidate in self.pipe:
    #                 continue
    #             candidates.append(candidate)
    #     return candidates

    # def find_enclosed_area_rt(self):
    #     for i in range(self.map_size[0]):
    #         for j in range(self.map_size[1]):
    #             if [i,j] in self.pipe:
    #                 continue
    #             print(f'CURRENT CELL [{i},{j}]')
    #             number_of_pipes = 0
    #             outside = True
    #             pipe = False
    #             for k in range(0, j):
    #                 print(f'LEFT [{i},{k}]')
    #                 if [i,k] in self.pipe:
    #                     if not pipe:
    #                         print(f'PIPE')
    #                         pipe = True
    #                         outside = not outside
    #                         number_of_pipes += 1
    #                 continue
    #                 pipe = False
    #             print(f'left: {number_of_pipes}')
    #             outside = True
    #             pipe = False
    #             for k in range(j, self.map_size[0]):
    #                 print(f'RIGHT [{i},{k}]')
    #                 if [i,k] in self.pipe:
    #                     if not pipe:
    #                         print(f'PIPE')
    #                         pipe = True
    #                         outside = not outside
    #                         number_of_pipes += 1
    #                 continue
    #                 pipe = False
    #             print(f'{number_of_pipes}')
    #             if number_of_pipes > 1 and number_of_pipes % 2 == 0:
    #                 self.draw_cell(i, j, 2)
    #                 self.plot_map(0)

    #             #     print(self.map.map[k, j])
    #             # if [i,j] in self.pipe:
    #             #     outside = not outside
    #             #     print(f'Outside: {outside}')
    #             #     continue
    #             # pipe = False
    #             # print(f'pipe: {pipe}')
    #             # if outside:
    #             #     self.draw_cell(i, j, 2)
    #             #     self.plot_map(0)


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
