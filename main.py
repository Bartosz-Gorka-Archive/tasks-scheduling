from random_scheduler import RandomScheduler
from scheduler import Scheduler
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

        # Run own scheduler
        scheduler = Scheduler(n=n, tasks=tasks, tasks_processing_time=tasks_processing_time, due_date=due_date)

        ## Schedule from Time = 0
        seq_1 = scheduler.schedule_from_start()

        ## Schedule 50/50 percentage - time
        seq_2 = scheduler.schedule_from_due_date_time()

        ## Schedule 50/50 percentage - tasks count
        seq_3 = scheduler.schedule_from_due_date_percentage()

        # Shifter module
        shifter = Shifter(due_date=due_date)

        # Find best start time of each sequence
        goal = sys.maxsize
        selected_sequence = None
        start_time = None

        goal_rs, start_time_rs = shifter.find_best_shift(tasks=random_scheduled_tasks)
        goal = goal_rs
        selected_sequence = random_scheduled_tasks
        start_time = start_time_rs
        print('SELECTED Random')

        goal_seq_1, start_time_seq_1 = shifter.find_best_shift(tasks=seq_1)
        if goal_seq_1 < goal:
            print('SELECTED SEQ 1')
            goal = goal_seq_1
            selected_sequence = seq_1
            start_time = start_time_seq_1

        goal_seq_2, start_time_seq_2 = shifter.find_best_shift(tasks=seq_2)
        if goal_seq_2 < goal:
            print('SELECTED SEQ 2')
            goal = goal_seq_2
            selected_sequence = seq_2
            start_time = start_time_seq_2

        goal_seq_3, start_time_seq_3 = shifter.find_best_shift(tasks=seq_3)
        if goal_seq_3 < goal:
            print('SELECTED SEQ 3')
            goal = goal_seq_3
            selected_sequence = seq_3
            start_time = start_time_seq_3

        # Store best results in file
        writer = Writer()
        writer.save(tasks=selected_sequence, start=start_time, goal=goal, n=n, k=k, h=h)

    else:
        print('RUN as main.py FILE_NUMBER INSTANCE H')


if __name__ == '__main__':
    main()
