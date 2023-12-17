import os, argparse
import numpy as np
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Day 5: If You Give A Seed A Fertilizer')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')


class solver05(aoc_solver):
    def __init__(self):
        self.seeds = None
        self.conversions = {}
        self.conversion_map = {}
        self.locations = []

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.convert_seeds(mode)
        if mode == 'a':
            print('Min location')
            print(min(self.locations))
        if mode == 'b':
            self.locations.sort()
            min_location = self.locations[0][0]
            print('Min location')
            print(min_location)

        return

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            source = ''
            destination = ''
            creating_conversion = False
            conversion_list = []
            
            for line in f:
                line = line.strip()
                if line == '':
                    if creating_conversion:
                        self.conversion_map[source+'2'+destination] = conversion_list
                        conversion_list = []
                        creating_conversion = False
                    continue
                if line.startswith('seeds'):
                    seeds = line.split(':')[1].strip()
                    self.seeds = [int(i) for i in seeds.split(' ')]
                    continue
                if line.endswith(':'):
                    creating_conversion = True
                    conversion = line.split(' ')[0]
                    source = conversion.split('-')[0]
                    destination = conversion.split('-')[2]
                    self.conversions[source] = destination
                    continue
                split_line = line.strip().split(' ')
                src_rng_start = int(split_line[1])
                dst_rng_start = int(split_line[0])
                rng_length = int(split_line[2])-1

                source_range = [src_rng_start, src_rng_start+rng_length]
                destination_range = [dst_rng_start, dst_rng_start+rng_length]
                conversion_list.append((source_range, destination_range))

            if creating_conversion:
                self.conversion_map[source+'2'+destination] = conversion_list
                conversion_list = []
                creating_conversion = False
                    
    def generate_seed_pairs(self):
        pairs = []
        for i in range(len(self.seeds)):
            if i % 2 == 0:
                continue
            pair = [self.seeds[i-1], self.seeds[i-1]+self.seeds[i]-1]
            pairs.append(pair) 
        return pairs

    def convert_seeds(self, mode):
        src_type = 'seed'
        src_data = self.seeds
        if mode == 'b':
            src_data = self.generate_seed_pairs()
        while src_type in self.conversions:
            dest_type = self.conversions[src_type]
            if mode == 'a':
                src_data = self.convert(src_type, dest_type, src_data)
            if mode == 'b':
                src_data = self.convert_pairs(src_type, dest_type, src_data)
            src_type = dest_type
        self.locations = src_data

    def convert_pairs(self, src_type, dst_type, src_data):
        dst_data = []
        key = src_type + '2' + dst_type
        cnv_map = self.conversion_map[key]
        src_pairs = []
        for i in range(len(src_data)):
            src_pairs = [src_data[i]]
            for cnv in cnv_map:
                dst_pairs, src_pairs = self.find_pairs(cnv, src_pairs)
                if len(dst_pairs) > 0:
                    dst_data.extend(dst_pairs)
                if len(src_pairs) == 0:
                    break
            dst_data.extend(src_pairs)
        return dst_data

    def find_pairs(self, ranges, pairs):
        converted_pairs = []
        remaining_pairs = []
        for pair in pairs:
            new_pairs, old_pairs = self.find_new_pairs(ranges, pair)
            converted_pairs.extend(new_pairs)
            remaining_pairs.extend(old_pairs)
        return converted_pairs, remaining_pairs

    def find_new_pairs(self, ranges, pair):
        new_pairs = []
        old_pairs = []
        src_rng = ranges[0]
        dst_rng = ranges[1]
        new_pair = [0,0]
        # if pair_0 in range
        if pair[0] >= src_rng[0] and pair[0] <= src_rng[1]:
            new_pair[0] = dst_rng[0] + (pair[0] - src_rng[0])
            # if pair_1 in range
            if pair[1] >=src_rng[0] and pair[1] <= src_rng[1]:
                # print("INSIDE")
                new_pair[1] = dst_rng[0] + (pair[1] - src_rng[0])
                new_pairs.append(new_pair)
            # if pair_1 > range
            else:
                # print("FILO")
                new_pair[1] = dst_rng[1]
                new_pairs.append(new_pair)
                remaining_pair = [src_rng[1] + 1 , pair[1]]
                old_pairs.append(remaining_pair)
        # if pair_0 < range and pair_1 in range
        elif pair[1] >= src_rng[0] and pair[1] <= src_rng[1]:
            # print("FOLI")
            new_pair[0] = dst_rng[0]
            new_pair[1] = dst_rng[0] + (pair[1] - src_rng[0])
            new_pairs.append(new_pair)
            remaining_pair = [pair[0], src_rng[0] - 1]
            old_pairs.append(remaining_pair)
        else:
            # if pair_0 < range and pair_1 > range
            if pair[0] < src_rng[0] and pair[1] > src_rng[1]:
                # print("BIGGER")
                new_pair = [dst_rng[0], dst_rng[1]]
                new_pairs.append(new_pair)
                remaining_pair = [pair[0], src_rng[0] - 1]
                old_pairs.append(remaining_pair)
                remaining_pair = [src_rng[1] + 1 , pair[1]]
                old_pairs.append(remaining_pair)
            else:
                # print("OUT")
                old_pairs.append(pair)

        return new_pairs, old_pairs

    def convert(self, src_type, dst_type, src_data):
        dst_data = []
        key = src_type + '2' + dst_type
        cnv_map = self.conversion_map[key]
        for element in src_data:
            dst_number = element
            for cnv in cnv_map:
                src_rng = cnv[0]
                dst_rng = cnv[1]
                if element >= src_rng[0] and element <= src_rng[1]:
                    dst_number = dst_rng[0] + (element - src_rng[0])
                    break
            dst_data.append(dst_number)

        return dst_data

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = solver05()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
