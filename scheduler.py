import re
import sys
from time import time
from operator import itemgetter
from numpy import sum, floor, delete


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

    def schedule_from_due_date_percentage(self):
        """Split 50-50 percentage and schedule"""
        # Extra variables with lists - to store calculations
        ordered = []
        used_tasks = []

        # Sort task on list
        sorted_tasks = self.sort_before_due_date()

        # We want split it 50-50 - first part before, second after due date
        # Reversed also to start from due date
        first_part = sorted_tasks[0:int(self.n/2)]
        first_part.reverse()

        # Start in due date
        time = self.due_date

        # Iterations over tasks
        for index, task in enumerate(first_part):
            time -= task['p']
            if time < 0:
                time -= task['p']
                break

            ordered.append(task)
            used_tasks.append(index)

        # Reverse tasks because started from due date
        ordered.reverse()

        # Remove used tasks from list and sort it
        tasks_to_schedule = delete(sorted_tasks, used_tasks)
        sorted_tasks = self.sort_after_due_date(tasks_to_schedule)

        # Order tasks after due date
        [ordered.append(task) for task in sorted_tasks]

        # Calculate goal function value
        value = self.calculate_penalties(ordered, time)
        return ordered, value, time

    def schedule_from_due_date_time(self):
        """Split 50-50 by time (processing time) and schedule"""
        # Extra variables with lists - to store calculations
        ordered = []
        used_tasks = []

        # Sort task on list
        sorted_tasks = self.sort_before_due_date()

        # We want split it 50-50 - first part before, second after due date
        # Reversed also to start from due date
        first_part = []
        sum_of_time = 0
        all_task_processing_half_time = self.tasks_processing_time / 2
        for task in sorted_tasks:
            sum_of_time += task['p']
            if sum_of_time > self.due_date or sum_of_time > all_task_processing_half_time:
                # We should finish append action without this task
                break
            else:
                first_part.append(task)
        first_part.reverse()

        # Start in due date
        time = self.due_date

        # Iterations over tasks
        for index, task in enumerate(first_part):
            time -= task['p']
            if time < 0:
                time -= task['p']
                break

            ordered.append(task)
            used_tasks.append(index)

        # Reverse tasks because started from due date
        ordered.reverse()

        # Remove used tasks from list and sort it
        tasks_to_schedule = delete(sorted_tasks, used_tasks)
        sorted_tasks = self.sort_after_due_date(tasks_to_schedule)

        # Order tasks after due date
        [ordered.append(task) for task in sorted_tasks]

        # Calculate goal function value
        value = self.calculate_penalties(ordered, time)
        return ordered, value, time

    def find_best_shift(self, tasks):
        best_start_time = 0

        # We should always start in Time = 0 to check one of possibled optional point
        # Next we will move x time units to ensure task finish in due date line
        start_time = 0
        min_value = self.calculate_penalties(tasks, start_time)

        # Now we should move tasks to finish in due date line
        last_task_index = None
        for index, task in enumerate(tasks):
            start_time += task['p']
            if start_time >= self.due_date:
                start_time -= (start_time - task['p'])
                last_task_index = index - 1
                break

        # Now in loop we can shift time and verify penalties
        for index in range(last_task_index, -1, -1):
            value = self.calculate_penalties(tasks, start_time)
            if value < min_value:
                min_value = value
                best_start_time = start_time
            start_time += tasks[index]['p']

        return min_value, best_start_time


    def shedule_shift_and_verify(self):
        min_value = sys.maxsize
        best_start_time = None
        ordered_tasks = None

        for start in range(0, int(self.due_date / 3)):
            ordered = []
            sorted_tasks = self.sort_before_due_date()

            # Order tasks before due date line
            used_tasks = []
            time = 0
            for index, task in enumerate(sorted_tasks):
                time += task['p']
                if time > self.due_date:
                    break
                ordered.append(task)
                used_tasks.append(index)

            # Remove used tasks from list and sort it
            tasks_to_schedule = delete(sorted_tasks, used_tasks)
            sorted_tasks = self.sort_after_due_date(tasks_to_schedule)

            # Order tasks after due date
            [ordered.append(task) for task in sorted_tasks]

            # Calculate goal function value
            value = self.calculate_penalties(ordered, start)
            if value < min_value:
                min_value = value
                best_start_time = start
                ordered_tasks = ordered.copy()

        return ordered_tasks, min_value, best_start_time

    def sort_before_due_date(self):
        sorder_by_max_b_ratio_first = sorted(self.original_tasks, key=itemgetter('b_ratio'), reverse=True)
        return sorted(sorder_by_max_b_ratio_first, key=itemgetter('a_ratio'))

    def sort_after_due_date(self, tasks):
        sorder_by_min_a_ratio_first = sorted(tasks, key=itemgetter('a_ratio'))
        return sorted(sorder_by_min_a_ratio_first, key=itemgetter('b_ratio'), reverse=True)

    def run_processing(self):
        self.read_tasks()
        self.calculate_sum_times()
        self.calculate_due_date()

        start = time()
        best_scheduled, goal_value, start_time_line = self.shedule_shift_and_verify()
        total = time() - start
        print(f'{total * 1000}'.replace('.', ','))

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
                'id': current_line - 2,
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
