from re import sub


class Reader():
    SOURCE_DIR = 'source'

    def read_tasks(self, n, k):
        path = f'{self.SOURCE_DIR}/sch{n}.txt'

        with open(path) as data:
            # Skip first line from file - number of instances
            next(data)

            how_many_records = n + 1
            start_line = (k - 1) * how_many_records
            current_line = 1

            # Skip X record from file
            while current_line <= start_line:
                current_line += 1
                next(data)

            # Skip task counter
            next(data)

            # Read instances
            current_line = 1
            original_tasks = []
            while current_line < how_many_records:
                line = data.readline().strip()
                val = [int(i) for i in sub('\s+', ' ', line).split(' ')]
                current_line += 1
                original_tasks.append({
                'id': current_line - 2,
                'p': val[0],
                'a': val[1],
                'b': val[2],
                'a_ratio': val[1] / val[0],
                'b_ratio': val[2] / val[0]
                })

            return original_tasks
