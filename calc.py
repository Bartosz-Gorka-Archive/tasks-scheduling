from math import floor


class Calc():
    def calculate_sum_times(self, tasks):
        return sum([task['p'] for task in tasks])

    def calculate_due_date(self, tasks_processing_time, h):
        return int(floor(tasks_processing_time * h))

    @staticmethod
    def calculate_penalties(tasks, start, due_date):
        result = 0
        time = start

        for task in tasks:
            result += task['a'] * max(due_date - (task['p'] + time), 0) \
                      + task['b'] * max((task['p'] + time) - due_date, 0)
            time += task['p']

        return result

    def setup(self, tasks, h):
        tasks_processing_time = self.calculate_sum_times(tasks=tasks)
        due_date = self.calculate_due_date(tasks_processing_time=tasks_processing_time, h=h)

        return tasks_processing_time, due_date
