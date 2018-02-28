from iohandling import parse_problem, write_solution


def process(file_path):
    raw = parse_problem(file_path)

    # solution goes here
    solution = []

    write_solution(file_path, solution)

