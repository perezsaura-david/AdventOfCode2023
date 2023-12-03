import os, argparse
import numpy as np
parser = argparse.ArgumentParser(description='Day 1: Calorie Counting')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"a" or "b"')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    # a
    bag_content = {'red':12, 'green':13, 'blue':14}
    invalid_game_ids = []
    valid_game_sum = 0
    # b
    power_list = []
    power_sum = 0

    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip()
            game, results = line.split(':')
            game_id = int(game.split(' ')[1])
            valid_game_sum += game_id
            set_results = results.split(';')
            set_result_list = []
            invalid_game = False # a
            min_bag_content = {'red':0, 'green':0, 'blue':0} # b
            for result in set_results:
                if args.mode == 'a':
                    if invalid_game:
                        break
                result = result.strip()
                subset_result = result.split(',')
                # print(f'{result=}')
                subset_result_list = []
                for subset in subset_result:
                    subset = subset.strip()
                    subset = subset.split(' ')
                    ball_number = int(subset[0])
                    ball_color = subset[1]
                    if args.mode == 'a':
                        if ball_number > bag_content[ball_color]:
                            print(f'Invalid game {game_id}: {ball_color} {ball_number} > {bag_content[ball_color]}')
                            invalid_game = True
                            valid_game_sum -= game_id
                            break
                    if args.mode == 'b':
                        if ball_number > min_bag_content[ball_color]:
                            min_bag_content[ball_color] = ball_number
            if args.mode == 'b':
                print(f'{min_bag_content=}')
                power = 1
                for key, value in min_bag_content.items():
                    power *= value 
                print(f'{power=}')
                power_sum += power

    if args.mode == 'a':
        print(f'{valid_game_sum=}')
    elif args.mode == 'b':
        print(f'{power_sum=}')
    else:
        print('Unknown mode.')
        exit(1)

