import sys
import re
from os import path


# CONSTANTS
FILE_PATH = 'source/'


def validate_file_name(number):
    correct_file_numbers = ['10', '20', '50', '100', '200', '500', '1000']
    return number in correct_file_numbers


def validate_arguments(args):
    return len(args) >= 4


def validate_instance_no(instance_number):
    return instance_number in [str(i) for i in list(range(1, 11))]


def validate_param_h(h):
    return h in ['0.2', '0.4', '0.6', '0.8']


def main():
    if validate_arguments(sys.argv) and validate_file_name(sys.argv[1]) and \
            validate_instance_no(sys.argv[2]) and validate_param_h(sys.argv[3]):
        file_path = path.join(FILE_PATH, 'sch' + sys.argv[1] + '.txt')

        with open(file_path) as file:
            next(file)  # Skip first line from file with number of instances

            expected_instance = int(sys.argv[2])
            how_many_records = int(sys.argv[1]) + 1
            start_line = (expected_instance - 1) * how_many_records
            current_line = 1

            # Skip X record from file - ignored
            while current_line <= start_line:
                current_line += 1
                next(file)

            # Read instances
            next(file)  # Skip task counter

            current_line = 1
            while current_line < how_many_records:
                current_line += 1
                line = file.readline().strip()
                values = re.sub("\\s+", ' ', line).split(' ')
                print(values)
    else:
        print('RUN as main.py FILE_NUMBER K H')


if __name__ == '__main__':
    main()
