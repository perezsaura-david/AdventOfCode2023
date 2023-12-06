import os, argparse
import numpy as np
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 6: Wait For It')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')


class solver06(aoc_solver):
    def __init__(self):
        self.times = []
        self.distances = []
        self.win_ways = []

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.calculate_score()
        print('Solution: ')
        print(self.score)

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            content = f.readlines()
            time_content = content[0].strip().split(':')[1].strip()
            distance_content = content[1].strip().split(':')[1].strip()
            time_content = " ".join(time_content.split())
            distance_content= " ".join(distance_content.split())
            if args.mode == 'a':
                #convert to list of ints
                self.times = [int(i) for i in time_content.split(' ')]
                self.distances = [int(i) for i in distance_content.split(' ')]
            if args.mode == 'b':
                race_time = ''
                for t in time_content.split(' '):
                    race_time += t
                self.times.append(int(race_time))
                race_distance = ''
                for d in distance_content.split(' '):
                    race_distance += d
                self.distances.append(int(race_distance))
            print(f'{self.times=}')
            print(f'{self.distances=}')


    def calculate_score(self):
        for i in range(len(self.times)):
            time = self.times[i]
            distance = self.distances[i]
            win_ways = self.find_win_ways(time, distance)
            self.win_ways.append(win_ways)
        print(f'{self.win_ways=}')
        self.score = np.prod(self.win_ways)

    def find_win_ways(self, time, record_distance):
        win_ways = 0
        # not including 0 and max time
        for i in range(1, time):
            run_distance = (i * (time - i))
            if run_distance > record_distance:
                win_ways += 1
        return win_ways


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = solver06()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
