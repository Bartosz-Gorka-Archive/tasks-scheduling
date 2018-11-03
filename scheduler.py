import re
import sys
from numpy import sum, floor


def writeln(stream, content):
    stream.write(str(content))
    stream.write('\n')


class Scheduler:
    def __init__(self):
        self.n = None
        self.k = None
        self.h = None
        self.original_tasks = []
        self.tasks_processing_time = None
        self.due_date = None

    def validate_parameters(self, args):
        return self.validate_arguments(args) and \
               self.validate_file_name(args[1]) and \
               self.validate_instance_no(args[2]) and \
               self.validate_param_h(args[3])

    def validate_file_name(self, number):
        self.n = int(number)
        correct_file_numbers = ['10', '20', '50', '100', '200', '500', '1000']
        return number in correct_file_numbers

    @staticmethod
    def validate_arguments(args):
        return len(args) >= 4

    def validate_instance_no(self, instance_number):
        self.k = int(instance_number)
        return instance_number in [str(i) for i in list(range(1, 11))]

    def validate_param_h(self, h):
        self.h = float(h)
        return h in ['0.2', '0.4', '0.6', '0.8']

    def calculate_sum_times(self):
        self.tasks_processing_time = sum([task['p'] for task in self.original_tasks])

    def calculate_due_date(self):
        self.due_date = int(floor(self.tasks_processing_time * self.h))

    def calculate_penalties(self, tasks, start):
        result = 0
        time = start

        for task in tasks:
            result += task['a'] * max(self.due_date - (task['p'] + time), 0) \
                      + task['b'] * max((task['p'] + time) - self.due_date, 0)
            time += task['p']

        return result

    def run_processing(self):
        self.read_tasks()
        self.calculate_sum_times()
        self.calculate_due_date()
        # TODO run scheduling
        best_scheduled = self.original_tasks
        start_time_line = 0
        goal_value = self.calculate_penalties(best_scheduled, start_time_line)
        self.write_to_file(best_scheduled, start_time_line, goal_value)

    def read_tasks(self):
        path = f'source/sch{self.n}.txt'

        with open(path) as data:
            next(data) # Skip first line from file - number of instances
            how_many_records = self.n + 1
            start_line = (self.k - 1) * how_many_records
            current_line = 1

            # Skip X record from file
            while current_line <= start_line:
                current_line += 1
                next(data)

            # Read instances
            next(data)  # Skip task counter

            current_line = 1
            while current_line < how_many_records:
                line = data.readline().strip()
                val = [int(i) for i in re.sub('\s+', ' ', line).split(' ')]
                current_line += 1
                self.original_tasks.append({
                'p': val[0],
                'a': val[1],
                'b': val[2],
                'a_ratio': val[1] / val[0],
                'b_ratio': val[2] / val[0]
                })

    def write_to_file(self, tasks, start, goal_value):
        path = f'results/sch{self.n}_{self.k}_{int(self.h * 10)}.txt'
        with open(path, 'w') as stream:
            writeln(stream, int(self.h * 10))
            writeln(stream, goal_value)
            writeln(stream, self.n)
            writeln(stream, start)
            for task in tasks:
                writeln(stream, f'{task["p"]}\t{task["a"]}\t{task["b"]}')


def main():
    scheduler = Scheduler()
    if scheduler.validate_parameters(sys.argv):
        scheduler.run_processing()
    else:
        print('RUN as scheduler.py FILE_NUMBER INSTANCE H')


if __name__ == '__main__':
    main()
