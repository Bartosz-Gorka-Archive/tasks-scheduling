from calc import Calc


class Shifter():
    def __init__(self, due_date):
        self.due_date = due_date

    def find_best_shift(self, tasks):
        calc = Calc()
        best_start_time = 0

        # We should always start in Time = 0 to check one of possibled optional point
        # Next we will move x time units to ensure task finish in due date line
        start_time = 0
        min_value = calc.calculate_penalties(tasks=tasks, start=start_time, due_date=self.due_date)

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
            value = calc.calculate_penalties(tasks=tasks, start=start_time, due_date=self.due_date)
            if value < min_value:
                min_value = value
                best_start_time = start_time
            start_time += tasks[index]['p']

        return min_value, best_start_time
