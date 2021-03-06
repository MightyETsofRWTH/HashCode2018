import os


def num_list(string):
    """
    "1 2 3 4" -> [1, 2, 3, 4]

    :param string: string
    :return: list of the ints in the string
    """
    return list(map(int, string.strip().split()))


def parse_problem(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("Invalid file path!")

    with open(file_path, 'r') as file:
        rows, columns, vehicles, rides_count, bonus, steps = num_list(next(file))
        rides = [num_list(row) for row in file]

    return rows, columns, vehicles, rides_count, bonus, steps, rides


def write_solution(file_path, solution):
    file_name, ext = os.path.splitext(os.path.basename(file_path))
    new_name = '{}.out'.format(file_name)

    out_dir = 'solutions_{}'.format(os.getlogin().lower())
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, new_name), 'w') as file:
        for line in solution:
            file.write(line)
            file.write('\n')
