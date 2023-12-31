from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import re


def parse(puzzle_input):
    input_array = puzzle_input.split('\n')

    return {
        'times': [int(x.group(0)) for x in re.finditer(r'\d+', input_array[0])],
        'distances': [int(x.group(0)) for x in re.finditer(r'\d+', input_array[1])]
    }


def part_a(data):
    times = data['times']
    distances = data['distances']
    number_of_winnable_ways = 0

    for index, time in enumerate(times):
        wins = 0
        distance = distances[index]

        for i in range(0, time):
            if (i * (time - i)) > distance:
                wins += 1

        if number_of_winnable_ways == 0:
            number_of_winnable_ways = wins
        else:
            number_of_winnable_ways *= wins

    return number_of_winnable_ways


def part_b(data):
    times = data['times']
    distances = data['distances']

    full_time = int(''.join(map(str, times)))
    full_distance = int(''.join(map(str, distances)))

    wins = 0

    for i in range(0, full_time):
        if (i * (full_time - i)) > full_distance:
            wins += 1

    return wins


def test(examples: List[Example], solve_part_a=True, solve_part_b=True):
    part_a_success = False
    part_b_success = False

    for index, example in enumerate(examples):
        print(f"Testing example {index + 1}")
        data = parse(example.input_data)

        if solve_part_a:
            if example.answer_a is None:
                print(f"Part A: No example solution provided.")
            else:
                result = part_a(data)

                if result == int(example.answer_a):
                    print("Part A: OK")
                    part_a_success = True
                else:
                    print(f"Part A: ERROR, expected {example.answer_a}, got {result}")

        if solve_part_b:
            if example.answer_b is None:
                print(f"Part B: No example solution provided.")
            else:
                result = part_b(data)

                if result == int(example.answer_b):
                    print("Part B: OK")
                    part_b_success = True
                else:
                    print(f"Part B: ERROR, expected {example.answer_b}, got {result}")

    return part_a_success, part_b_success


def solve(puzzle: Puzzle, solve_part_a=True, solve_part_b=True, submit_solution=True, part_a_example_success=False, part_b_example_success=False):
    data = parse(puzzle.input_data)

    if solve_part_a:
        solution_a = part_a(data)
        print(f"Part A: {solution_a}")

        if submit_solution and part_a_example_success:
            puzzle.answer_a = solution_a
        elif not part_a_example_success:
            print("Part A: Not all examples were successful, not submitting solution")

    if solve_part_b:
        solution_b = part_b(data)
        print(f"Part B: {solution_b}")

        if submit_solution and part_b_example_success:
            puzzle.answer_b = solution_b
        elif not part_b_example_success:
            print("Part B: Not all examples were successful, not submitting solution")


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=6)

    localzone = datetime.now().astimezone().tzinfo
    now = datetime.now().astimezone(tz=localzone)

    if puzzle.unlock_time() > now:
        print(f"AOC Day {puzzle.day} will unlock at {puzzle.unlock_time()}!")
        exit(0)

    print(f"Day {puzzle.day}: {puzzle.title}")
    print()
    print("Testing examples")
    [part_a_example_success, part_b_example_success] = test(puzzle.examples, True, True)
    print()
    print("Solving Input")
    solve(puzzle, True, True, True, part_a_example_success, part_b_example_success)
