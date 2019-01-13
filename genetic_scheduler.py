from shifter import Shifter
from random import randint, choice
from time import time


class GeneticScheduler():
    def __init__(self, n, due_date):
        self.n = n
        self.due_date = due_date
        self.max_epochs = 1000
        self.populations_after_tournament = 5
        self.populations_on_epoch_start = self.populations_after_tournament * 4
        self.mutation_rate = 0.20
        self.mutation_percentage = int(self.mutation_rate * 100)
        self.max_time_in_seconds = 60

    def mutation(self, sequence):
        # Copy sequence to enable change indexes of elements
        new_sequence = sequence.copy()

        # Random indexes
        first_index = randint(0, self.n - 1)
        second_index = randint(0, self.n - 1)

        # Ensure not the same tasks mutated
        while first_index == second_index:
            second_index = randint(0, self.n - 1)

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

    def next_epoch(self, populations):
        # Calculate how many populations we have now
        populations_count = len(populations)

        while populations_count < self.populations_on_epoch_start:
            enabled_indexes = list(range(0, populations_count))
            first_index = choice(enabled_indexes)
            second_index = choice(enabled_indexes)

            while first_index == second_index:
                second_index = choice(enabled_indexes)

            new_seq_1, new_seq_2 = self.crossover(populations[first_index], populations[second_index])
            populations.append(new_seq_1)
            populations.append(new_seq_2)
            populations_count += 2

        # Each population can prepare mutation
        for index, population in enumerate(populations):
            if randint(0, 100) < self.mutation_percentage:
                # TODO Now as replacement, but maybe as new population?
                populations[index] = self.mutation(population)

        # Run tournament and return winners
        return self.tournament(populations)

    def schedule(self, previous_populations):
        # Add first basic populations from previous algorithms
        populations = previous_populations.copy()

        # Start time store - we have X minutes
        start_time = time()

        # Start zero epoch (required to seed populations) and iterate it
        current_epoch = 0
        while (time() - start_time) < self.max_time_in_seconds and current_epoch <= self.max_epochs:
            populations = self.next_epoch(populations)
            current_epoch += 1

        # Store original tournament winners count as temp
        temp_tournament_winners = self.populations_after_tournament

        # Select only one winner - this is response
        self.populations_after_tournament = 1
        winner = self.tournament(populations)[0]
        self.populations_after_tournament = temp_tournament_winners

        # Return best sequence
        return winner
