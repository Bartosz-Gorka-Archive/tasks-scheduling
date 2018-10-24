import re
from glob import glob
from numpy import sum, floor


class Checker:
    def __init__(self):
        self.results_dir = 'results'
        self.tasks = []
        self.start_point = 0
        self.sum_times = 0
        self.h = 0.2
        self.due_date = 0
        self.result = 0

    def get_results_list(self):
        return [file for file in glob(f'{self.results_dir}/sch[0-9]*_[0-9]_[2468].txt')]

    def calculate_sum_times(self):
        self.sum_times = sum([time[0] for time in self.tasks])
        return self.sum_times

    def calculate_due_date(self):
        self.due_date = int(floor(self.sum_times * self.h))
        return self.due_date

    def calculate_result_value(self):
        time = self.start_point
        result = 0

        for task in self.tasks:
            result += task[1] * max(self.due_date - (task[0] + time), 0)\
                      + task[2] * max((task[0] + time) - self.due_date, 0)
            time += task[0]

        self.result = result
        return result

    def calculate(self):
        self.calculate_sum_times()
        self.calculate_due_date()
        return self.calculate_result_value()

    def check_file(self, name):
        print(f'Validate file {name}')
        # Replace file's name and split to variables
        variables = name.replace(f'{self.results_dir}/sch', '').replace('.txt', '').split('_')
        n_in_name = int(variables[0])
        k_in_name = int(variables[1])
        h_in_name = int(variables[2]) / 10

        # Open file and validate result
        with open(name) as file:
            try:
                # Check H in file, verify it with name
                h_in_file = file.readline().strip()
                if (int(h_in_file) / 10) != h_in_name:
                    raise ValueError('H in file not equal to name')

                # Read and parse to int original result value (to check at the end)
                result_in_file = int(file.readline().strip())

                # Check number of tasks in file, validate value with file name
                n_in_file = int(file.readline().strip())
                if int(n_in_file) != n_in_name:
                    raise ValueError('N in file not equal to name')

                # Check start time value - when < 0, raise error
                start_time_value = int(file.readline().strip())
                if start_time_value < 0:
                    raise ValueError('R should be greater than or equal to zero')
                else:
                    self.start_point = start_time_value

                # Read tasks
                counter = 0
                content = '-'
                while content:
                    counter += 1
                    if counter >= n_in_file:
                        break
                    content = file.readline().strip()
                    var = re.sub('\s+', ' ', content).split(' ')
                    if len(var) != 3:
                        raise ValueError(f'Line {counter} with invalid format')
                    self.tasks.append([int(i) for i in var])

                expected_result = self.calculate()
                if expected_result != result_in_file:
                    raise ValueError(f'Expected {expected_result} as result but receive {result_in_file}')
                else:
                    print(f'{n_in_file} | {k_in_name} | {self.h} | Correct {expected_result}')

            except ValueError as error:
                [print(er) for er in error.args]


def main():
    checker = Checker()
    for file in checker.get_results_list():
        checker.check_file(file)


if __name__ == '__main__':
    main()
