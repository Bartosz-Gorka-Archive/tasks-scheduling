from random_scheduler import RandomScheduler
from validator import Validator
from shifter import Shifter
from writer import Writer
from reader import Reader
from calc import Calc
import sys


def main():
    # Start with validator and check parameters from user
    validator = Validator()
    if validator.are_valid_parameters(sys.argv):
        # When all correct - fetch it
        n, k, h = validator.parameters()

        # Read tasks from file
        reader = Reader()
        tasks = reader.read_tasks(k=k, n=n)

        # Calculate total processing time and due date
        calc = Calc()
        tasks_processing_time, due_date = calc.setup(tasks=tasks, h=h)

        # Run random scheduler
        random_scheduler = RandomScheduler(n=n, tasks=tasks)
        random_scheduled_tasks = random_scheduler.schedule()

        # Shifter module - find best start time value
        shifter = Shifter(due_date=due_date)
        goal, start_time = shifter.find_best_shift(tasks=random_scheduled_tasks)

        # Store results in file
        writer = Writer()
        writer.save(tasks=random_scheduled_tasks, start=start_time, goal=goal, n=n, k=k, h=h)

    else:
        print('RUN as main.py FILE_NUMBER INSTANCE H')


if __name__ == '__main__':
    main()
