import glob


class Checker:
    def __init__(self):
        self.results_dir = 'results'

    def get_results_list(self):
        return [file for file in glob.glob(f'{self.results_dir}/sch[0-9]*_[0-9]_[2468].txt')]

    def check_file(self, name):
        print(f'Validate file {name}')
        # Replace file's name and split to variables
        variables = name.replace(f'{self.results_dir}/sch', '').replace('.txt', '').split('_')
        n_in_name = int(variables[0])
        k_in_name = int(variables[1])
        h_in_name = int(variables[2]) / 10

        # Open file and validate result
        with open(name) as file:
            try:
                # Check H in file, verify it with name
                h_in_file = file.readline().strip()
                if (int(h_in_file) / 10) != h_in_name:
                    raise ValueError('H in file not equal to name')

                # Read and parse to int original result value (to check at the end)
                result_in_file = int(file.readline().strip())

                # Check number of tasks in file, validate value with file name
                n_in_file = int(file.readline().strip())
                if int(n_in_file) != n_in_name:
                    raise ValueError('N in file not equal to name')

                # Check start time value - when < 0, raise error
                start_time_value = int(file.readline().strip())
                if start_time_value < 0:
                    raise ValueError('R should be greater than or equal to zero')

                # Read tasks
            except ValueError as error:
                [print(er) for er in error.args]


def main():
    checker = Checker()
    for file in checker.get_results_list():
        checker.check_file(file)


if __name__ == '__main__':
    main()
