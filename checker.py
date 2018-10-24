import glob


class Checker:
    def __init__(self):
        self.results_dir = 'results'

    def get_results_list(self):
        return [file for file in glob.glob(f'{self.results_dir}/sch[0-9]*_[0-9]_[2468].txt')]


def main():
    checker = Checker()
    print(checker.get_results_list())


if __name__ == '__main__':
    main()
