import sys
import re
from os import path
from numpy import sum
from numpy import floor


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


def calculate_sum_times(tasks):
    return sum([time[0] for time in tasks.values()])


def calculate_due_date(times, h):
    return int(floor(times * float(h)))


def calculate_penalties(tasks, due_date):
    return sum([val[1] * max(due_date - (val[0] + val[3]), 0) + val[2] * max((val[0] + val[3]) - due_date, 0) for val in tasks.values()])


def main():
    if validate_arguments(sys.argv) and validate_file_name(sys.argv[1]) and \
            validate_instance_no(sys.argv[2]) and validate_param_h(sys.argv[3]):
        file_path = path.join(FILE_PATH, 'sch' + sys.argv[1] + '.txt')

        # Tasks dictionary with values
        tasks = {}

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
                values = re.sub('\s+', ' ', line).split(' ')
                int_values = [int(i) for i in values]
                tasks.update({str(current_line - 2): int_values})

        print('Tasks details')
        for (key, value) in tasks.items():
            print(f' Task {int(key) + 1} => {value}')

        # Total tasks times (sum)
        sum_tasks_times = calculate_sum_times(tasks)
        print(f'Tasks total time = {sum_tasks_times}')

        # Calculate due date value
        due_date_value = calculate_due_date(sum_tasks_times, sys.argv[3])
        print(f'Due date value = {due_date_value}')

        # Fake tasks scheduling
        scheduled = {}
        time = 0
        for (key, value) in tasks.items():
            times = value
            times.append(time)
            time += value[0]
            scheduled.update({key: times})

        scheduled_tasks_penalties = calculate_penalties(scheduled, due_date_value)
        print(scheduled.values())
        print(f'Penalties = {scheduled_tasks_penalties}')

    else:
        print('RUN as main.py FILE_NUMBER K H')


if __name__ == '__main__':
    main()
