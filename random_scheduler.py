from random import shuffle


class RandomScheduler:
    def __init__(self, h, n, k, tasks, due_date):
        self.h = h
        self.n = n
        self.k = k
        self.tasks = tasks.copy()
        self.due_date = due_date

    def schedule(self):
        indexes = list(range(0, self.n))
        shuffle(indexes)
        tasks = [self.tasks[index] for index in indexes]
        self.write_to_file(tasks)

        return tasks

    def write_to_file(self, tasks):
        goal_value = self.calculate_penalties(tasks)
        path = f'results-random/sch{self.n}_{self.k}_{int(self.h * 10)}.txt'
        with open(path, 'w') as stream:
            self.writeln(stream, int(self.h * 10))
            self.writeln(stream, goal_value)
            self.writeln(stream, self.n)
            self.writeln(stream, 0)
            for task in tasks:
                self.writeln(stream, f'{task["p"]}\t{task["a"]}\t{task["b"]}')

    def writeln(self, stream, content):
        stream.write(str(content))
        stream.write('\n')

    def calculate_penalties(self, tasks):
        result = 0
        time = 0

        for task in tasks:
            result += task['a'] * max(self.due_date - (task['p'] + time), 0) \
                      + task['b'] * max((task['p'] + time) - self.due_date, 0)
            time += task['p']

        return result
