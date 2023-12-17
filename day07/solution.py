import os, argparse
import numpy as np
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from base import aoc_solver

parser = argparse.ArgumentParser(description='Day 7: Camel Cards')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')


class Hand:
    def __init__(self, hand_id, cards, bid):
        self.id = hand_id
        self.cards = cards
        self.bid = int(bid)
        self.rank = 0
        self.type = 0
        self.cards_code = ''
        self.enum_card_type = {
            'A': 'a',
            'K': 'b',
            'Q': 'c',
            'J': 'd',
            'T': 'e',
        }

        self.generate_hand_code()

    def generate_hand_code(self):
        digit_code_init = 101 # f
        if args.mode == 'b':
            self.enum_card_type['T'] = 'd'
            self.enum_card_type['J'] = 'm'
            digit_code_init = 100 # e
        for card in self.cards:
            if card.isdigit():
                card_value = abs(int(card) - 10)
                self.cards_code += chr(digit_code_init + card_value)
            else:
                self.cards_code += self.enum_card_type[card]

    # def __str__(self):
    #     return f'{self.id=}, {self.cards=}, {self.bid=}, {self.rank=}, {self.type=}'

    def __repr__(self):
        return f'[{self.id=}, {self.cards=}, {self.bid=}, {self.rank=}, {self.type=}, {self.cards_code=}]'

    def __eq__(self, other):
        return self.cards_code == other.cards_code

    def __lt__(self, other):
        return self.cards_code < other.cards_code

    def __le__(self, other):
        return self.cards_code <= other.cards_code

    def __gt__(self, other):
        return self.cards_code > other.cards_code

    def __ge__(self, other):
        return self.cards_code >= other.cards_code

class Solver06(aoc_solver):
    def __init__(self):
        self.hands = []
        self.hand_groups = []
        self.enum_hand_types = {
            1: 'Five of a kind',
            2: 'Four of a kind',
            3: 'Full house',
            4: 'Three of a kind',
            5: 'Two pairs',
            6: 'One pair',
            7: 'High Card',
        }

        for hand_type in self.enum_hand_types:
            self.hand_groups.append([])

    def solve_a(self, input):
        self.solve(input, 'a')

    def solve_b(self, input):
        self.solve(input, 'b')

    def solve(self, input, mode):
        self.parse_input(input)
        self.group_hands()
        self.rank_hands()

        # sort hands by rank
        self.hands.sort(key=lambda x: x.rank, reverse=True)

        # for hand in self.hands:
        #     print(hand.cards)
        # self.calculate_score()
        # print('Solution: ')
        # print(self.score)

    def parse_input(self, input):

        with open(args.input, 'r') as f:
            content = f.readlines()
            for i in range(len(content)):
                line = content[i]
                if line == '\n':
                    continue
                hand = line.strip().split(' ')
                self.hands.append(Hand(i, hand[0], hand[1]))

    def group_hands(self):
        for hand in self.hands:
            # print(f'{hand.cards=}')
            unique_cards = set(hand.cards)
            # print(f'{unique_cards=}')
            number_of_Jokers = 0
            if args.mode == 'b':
                for i in range(len(hand.cards)):
                    if hand.cards[i] == 'J':
                        number_of_Jokers += 1
            # print(f'{number_of_Jokers=}')
            if len(unique_cards) == 1:
                hand.type = 1
            if len(unique_cards) == 4:
                hand.type = 6
            if len(unique_cards) == 5:
                hand.type = 7
            if len(unique_cards) == 2:
                # Can be Four of a kind of Full house
                first_card = hand.cards[0]
                same_cards = 1
                for i in range(1, len(hand.cards)):
                    if hand.cards[i] == first_card:
                        same_cards += 1
                if (same_cards == 1 or same_cards == 4):
                    hand.type = 2
                else:
                    hand.type = 3
            if len(unique_cards) == 3:
                # Can be Two pairs of Three of a kind
                first_card = hand.cards[0]
                same_cards = 1
                # print('Checking first_card')
                for i in range(1, len(hand.cards)):
                    if hand.cards[i] == first_card:
                        same_cards += 1
                if (same_cards == 3):
                    hand.type = 4
                elif (same_cards == 2):
                    hand.type = 5
                else:
                    second_card = hand.cards[1]
                    same_cards = 1
                    # print('Checking second_card')
                    for i in range(2, len(hand.cards)):
                        if hand.cards[i] == second_card:
                            same_cards += 1
                        if (same_cards == 3 or same_cards == 1):
                            hand.type = 4
                        else:
                            hand.type = 5
            if args.mode == 'b' and number_of_Jokers > 0:
                # print(f'Initial: {self.enum_hand_types[hand.type]}')
                if hand.type == 2 or hand.type == 3:
                    # Four of a kind or Full house with Jokers (1,4/2,3)
                    # became Five of a kind
                    hand.type = 1
                elif hand.type == 4:
                    # Three of a kind with Jokers (1,3)
                    # became Four of a kind
                    hand.type = 2
                elif hand.type == 5:
                    if number_of_Jokers == 1:
                        # Two pairs with one Joker
                        # became Full house
                        hand.type = 3
                    else:
                        # Two pairs with two Jokers
                        # became Four of a kind
                        hand.type = 2
                elif hand.type == 6:
                    # One pair with (1 or 2) Jokers
                    # became Three of a kind
                    hand.type = 4
                elif hand.type == 7:
                    # High Card with one Joker
                    # became One pair
                    hand.type = 6
                # print(f'Final: {self.enum_hand_types[hand.type]}')
            # print(f'{hand=}')
            # print(self.enum_hand_types[hand.type])
            self.hand_groups[hand.type-1].append(hand)

    def rank_hands(self):
        last_rank = 1
        score = 0
        for group in self.hand_groups[::-1]:
            group.sort(reverse=True)
            i = 0
            for i in range(len(group)):
                hand = group[i]
                hand.rank = last_rank + i
                # print(hand.rank, hand.bid)
                # print(group[i], f'{self.enum_hand_types[group[i].type]}' )
                step_score = hand.rank * hand.bid
                # score += step_score
                score += hand.rank * hand.bid
                # print(f'{hand.cards}')
                # print(f'{hand.rank=}, {hand.bid=}', f'{step_score=}') 
            last_rank += len(group)
        print(f'{score=}')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    solver = Solver06()
    if args.mode == 'a':
        solver.solve_a(args.input)
    elif args.mode == 'b':
        solver.solve_b(args.input)
    else:
        print('Unknown mode.')
    exit(0)
