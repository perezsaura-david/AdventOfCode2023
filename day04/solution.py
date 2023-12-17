import os, argparse
import numpy as np
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 4: Scratchcards')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')

class solver04(aoc_solver):
    def __init__(self):
        self.winning_numbers = []
        self.our_numbers = []
        self.scores = []
        self.cards = []
        self.scratchcards = {} 

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        if mode == 'a':
            self.calculate_scores()
            score = sum(self.scores)
            print(f'Score: {score}')
        if mode == 'b':
            self.calculate_scratchcards()
            sum_of_scratchcards = 0
            for card in self.scratchcards:
                sum_of_scratchcards += self.scratchcards[card]
            print(f'Sum of scratchcards: {sum_of_scratchcards}')

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            
            for line in f:
                line = line.strip()
                # print(f'Line: {line}')
                card, numbers = line.split(':')
                card_id = int(card.strip().split(' ')[-1])
                self.cards.append(card_id)
                raw_winning_numbers, raw_our_numbers = numbers.split('|')
                raw_winning_numbers = raw_winning_numbers.strip().split(' ')
                raw_our_numbers = raw_our_numbers.strip().split(' ')
                winning_numbers = []
                our_numbers = []
                for number in raw_winning_numbers:
                    if number == '':
                        continue
                    winning_numbers.append(int(number))
                    
                for number in raw_our_numbers:
                    if number == '':
                        continue
                    our_numbers.append(int(number))
                
                winning_numbers = set(winning_numbers)
                our_numbers = set(our_numbers)

                self.winning_numbers.append(winning_numbers)
                self.our_numbers.append(our_numbers)

    def calculate_scores(self):
        for i in range(len(self.winning_numbers)):
            score_numbers = self.winning_numbers[i].intersection(self.our_numbers[i])
            # print(f'Score numbers: {score_numbers}')
            score = 2**(len(score_numbers) - 1) if len(score_numbers) > 0 else 0
            # print(f'Score: {score}')
            self.scores.append(score)

    def calculate_scratchcards(self):
        for card in self.cards:
            self.scratchcards[card] = 1
        for i in range(len(self.cards)):
            score_numbers = self.winning_numbers[i].intersection(self.our_numbers[i])
            number_of_scratchcards = len(score_numbers)
            if number_of_scratchcards == 0:
                continue
            for j in range(number_of_scratchcards):
                card_id = i + j + 1
                self.scratchcards[self.cards[card_id]] += self.scratchcards[self.cards[i]]
            # print(f'Scratchcards: {self.scratchcards}')


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = solver04()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
