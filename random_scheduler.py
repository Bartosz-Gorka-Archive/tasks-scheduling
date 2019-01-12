from random import shuffle


class RandomScheduler:
    def __init__(self, n, tasks):
        self.n = n
        self.tasks = tasks.copy()

    def schedule(self):
        indexes = list(range(0, self.n))
        shuffle(indexes)
        tasks = [self.tasks[index] for index in indexes]

        return tasks
