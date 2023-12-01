import os, argparse
import numpy as np
parser = argparse.ArgumentParser(description='Day 1: Calorie Counting')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"digits" or "c_digits"')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    digits = []
    for n in range(10):
        digits.append(str(n))

    c_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    calibration_values=[]
    with open(args.input, 'r') as f:
        for line in f:
            digit_list = []
            for digit in digits:
                idx = line.find(digit)
                if idx == -1:
                    continue
                digit_list.append((idx, digit))
                idx = line.rfind(digit)
                if idx == -1:
                    continue
                digit_list.append((idx, digit))
            if args.mode == 'c_digits':
                for i in range(len(c_digits)):
                    idx = line.find(c_digits[i])
                    if idx == -1:
                        continue
                    digit_list.append((idx, str(i+1)))
                    idx = line.rfind(c_digits[i])
                    if idx == -1:
                        continue
                    digit_list.append((idx, str(i+1)))
            digit_list.sort(key=lambda x: x[0])
            first_digit = digit_list[0][1]
            last_digit = digit_list[-1][1]
            value = int(first_digit + last_digit)
            calibration_values.append(value)    

    calibration_value=0
    for value in calibration_values:
        calibration_value += value

    if args.mode == 'digits':
        print(f'{calibration_value=}')
    elif args.mode == 'c_digits':
        print(f'{calibration_value=}')
    else:
        print('Unknown mode.')
        exit(1)

