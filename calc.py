from math import floor


class Calc():
    def __init__(self, tasks, h):
        self.h = h
        self.tasks = tasks.copy()
        self.tasks_processing_time = None
        self.due_date = None

    def calculate_sum_times(self):
        self.tasks_processing_time = sum([task['p'] for task in self.tasks])

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

    def setup(self):
        self.calculate_sum_times()
        self.calculate_due_date()

    def parameters(self):
        return self.tasks_processing_time, self.due_date
