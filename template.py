from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example


def parse(puzzle_input):
    input_array = puzzle_input.split('\n')

    return input_array


def part_a(data):
    """Solve Part A"""


def part_b(data):
    """Solve Part B"""


def test(examples: List[Example], solve_part_a=True, solve_part_b=True):
    for example in examples:
        data = parse(example.input_data)

        if solve_part_a:
            result = part_a(data)

            if result == int(example.answer_a):
                print("Part A: OK")
            else:
                print(f"Part A: ERROR, expected {example.answer_a}, got {result}")
        if solve_part_b:
            result = part_b(data)

            if result == int(example.answer_b):
                print("Part B: OK")
            else:
                print(f"Part B: ERROR, expected {example.answer_b}, got {result}")


def solve(puzzle: Puzzle, solve_part_a=True, solve_part_b=True, submit_solution=True):
    data = parse(puzzle.input_data)

    if solve_part_a:
        solution_a = part_a(data)
        print(f"Part A: {solution_a}")

        if submit_solution:
            puzzle.answer_a = solution_a

    if solve_part_b:
        solution_b = part_b(data)
        print(f"Part B: {solution_b}")

        if submit_solution:
            puzzle.answer_b = solution_b


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=1)

    localzone = datetime.now().astimezone().tzinfo
    now = datetime.now().astimezone(tz=localzone)

    if puzzle.unlock_time() > now:
        print(f"AOC Day {puzzle.day} will unlock at {puzzle.unlock_time()}!")
        exit(0)

    print(puzzle.title)
    print("Testing examples")
    test(puzzle.examples, True, False)
    print("Solving")
    solve(puzzle, True, False, True)
