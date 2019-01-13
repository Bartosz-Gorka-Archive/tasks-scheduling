from shifter import Shifter
from random import randint, choice


class GeneticScheduler():
    def __init__(self, n, due_date):
        self.n = n
        self.due_date = due_date
        self.populations_after_tournament = 10

    def mutation(self, sequence):
        # Copy sequence to enable change indexes of elements
        new_sequence = sequence.copy()

        # Random indexes
        first_index = randint(0, self.n)
        second_index = randint(0, self.n)

        # Ensure not the same tasks mutated
        while first_index == second_index:
            second_index = randint(0, self.n)

        # Store temp task and prepare mutation
        task = new_sequence[first_index]
        new_sequence[first_index] = new_sequence[second_index]
        new_sequence[second_index] = task

        # Return new tasks' sequence
        return new_sequence

    def tournament(self, populations):
        # Now we have X populations
        current_population_count = len(populations)

        # Populations' goal value - calculate once, use multiple time
        shifter = Shifter(due_date=self.due_date)
        results = {}
        for index, population in enumerate(populations):
            value, _start_time = shifter.find_best_shift(population)
            results[index] = value

        enabled_indexes = list(range(0, current_population_count))

        # We want only `populations_after_tournament` count - we must eliminate populations
        while current_population_count > self.populations_after_tournament:
            # Random generate indexes of populations to current round of tournament
            first_index = choice(enabled_indexes)
            second_index = choice(enabled_indexes)

            # Ensure not the same population
            while first_index == second_index:
                second_index = choice(enabled_indexes)

            # Make a tournament
            current_population_count -= 1
            if results[first_index] < results[second_index]:
                enabled_indexes.remove(second_index)
            else:
                enabled_indexes.remove(first_index)

        # Now we should return only winners
        return [population for index, population in enumerate(populations) if index in enabled_indexes]

    def crossover(self, population_1, population_2):
        # Random index of crossover point
        # Min one task before or after this point
        point = randint(1, self.n - 1)

        # Prepare two new sequences
        new_seq_1 = population_1[0:point].copy()
        new_seq_2 = population_2[0:point].copy()

        used_in_seq_1 = [task['id'] for task in new_seq_1]
        used_in_seq_2 = [task['id'] for task in new_seq_2]

        [new_seq_1.append(task) for task in population_2 if task['id'] not in used_in_seq_1]
        [new_seq_2.append(task) for task in population_1 if task['id'] not in used_in_seq_2]

        return new_seq_1, new_seq_2
