import os


class Writer():
    RESULTS_DIR = 'results'

    @staticmethod
    def writeln(stream, content):
        stream.write(str(content))
        stream.write('\n')

    def save(self, tasks, start, goal, n, k, h):
        filename = f'{self.RESULTS_DIR}/sch{n}_{k}_{int(h * 10)}.txt'
        os.makedirs(self.RESULTS_DIR, exist_ok=True)

        with open(filename, 'w+') as stream:
            self.writeln(stream, int(h * 10))
            self.writeln(stream, goal)
            self.writeln(stream, n)
            self.writeln(stream, start)
            for task in tasks:
                self.writeln(stream, f'{task["p"]}\t{task["a"]}\t{task["b"]}')
