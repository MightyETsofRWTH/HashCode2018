import os


def parse_problem(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("Invalid file path!")

    with open(file_path, 'r') as file:
        pass

    return None


def write_solution(file_path, solution):
    file_name, ext = os.path.splitext(os.path.basename(file_path))
    new_name = '{}.out'.format(file_name)

    out_dir = 'solutions_{}'.format(os.getlogin().lower())
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, new_name), 'w') as file:
        for line in solution:
            file.write('')
