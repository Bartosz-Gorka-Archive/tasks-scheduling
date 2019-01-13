from operator import itemgetter
from numpy import delete
import sys


class Scheduler():
    def __init__(self, n, tasks, tasks_processing_time, due_date):
        self.n = n
        self.original_tasks = tasks
        self.tasks_processing_time = tasks_processing_time
        self.due_date = due_date

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
        for task in first_part:
            time -= task['p']
            if time < 0:
                time -= task['p']
                break

            ordered.append(task)
            used_tasks.append(task['id'])

        # Reverse tasks because started from due date
        ordered.reverse()

        # Remove used tasks from list and sort it
        tasks_to_schedule = [task for task in sorted_tasks if task['id'] not in used_tasks]
        sorted_tasks = self.sort_after_due_date(tasks_to_schedule)

        # Order tasks after due date
        [ordered.append(task) for task in sorted_tasks]

        # Return sequence of tasks
        return ordered

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
        for task in first_part:
            time -= task['p']
            if time < 0:
                time -= task['p']
                break

            ordered.append(task)
            used_tasks.append(task['id'])

        # Reverse tasks because started from due date
        ordered.reverse()

        # Remove used tasks from list and sort it
        tasks_to_schedule = [task for task in sorted_tasks if task['id'] not in used_tasks]
        sorted_tasks = self.sort_after_due_date(tasks_to_schedule)

        # Order tasks after due date
        [ordered.append(task) for task in sorted_tasks]

        # Return sequence of tasks
        return ordered

    def schedule_from_start(self):
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

        # Return sequence of tasks
        return ordered

    def sort_before_due_date(self):
        sorder_by_max_b_ratio_first = sorted(self.original_tasks, key=itemgetter('b_ratio'), reverse=True)
        return sorted(sorder_by_max_b_ratio_first, key=itemgetter('a_ratio'))

    def sort_after_due_date(self, tasks):
        sorder_by_min_a_ratio_first = sorted(tasks, key=itemgetter('a_ratio'))
        return sorted(sorder_by_min_a_ratio_first, key=itemgetter('b_ratio'), reverse=True)
