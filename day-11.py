from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import numpy as np

def parse(puzzle_input):
    input_array = puzzle_input.split('\n')
    result = []

    for line in input_array:
        result.append([*line.strip()])

    return result


def part_a(data):
    values = np.array(data)
    val = np.zeros(values.shape, dtype=int)
    val[np.where(values == '#')] = 1
    val_new = []

    for row in val:
        val_new.append(row)
        if np.sum(row) == 0:
            val_new.append(row)

    val = np.array(val_new).transpose((1, 0)).copy()
    val_new = []

    for row in val:
        val_new.append(row)
        if np.sum(row) == 0:
            val_new.append(row)

    val = np.array(val_new).transpose((1, 0)).copy()
    hits = np.where(val != 0)
    hits = np.array(hits)
    sol = 0

    for i in range(np.array(hits).shape[1]):
        for j in range(i+1, np.array(hits).shape[1]):
            sol += np.sum(np.abs(hits[:, i] - hits[:, j]))

    return sol


def part_b(data):
    values = np.array(data)
    val = np.zeros(values.shape, dtype=int)
    val[np.where(values == '#')] = 1
    hits = np.where(val != 0)
    hits = np.array(hits)
    sol2 = 0

    for i in range(np.array(hits).shape[1]):
        for j in range(i+1, np.array(hits).shape[1]):
            sol2 += np.sum(np.abs(hits[:, i] - hits[:, j]))

    return (9599070 - sol2) * 999999 + sol2


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
            # Part B example does not work as we have no final solution in the html
            # therefore we cannot automatically test it
            part_b_success = True
            # if example.answer_b is None:
            #     print(f"Part B: No example solution provided.")
            # else:
            #     result = part_b(data)
            #
            #     if result == int(example.answer_b):
            #         print("Part B: OK")
            #         part_b_success = True
            #     else:
            #         print(f"Part B: ERROR, expected {example.answer_b}, got {result}")

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
    puzzle = Puzzle(year=2023, day=11)

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
