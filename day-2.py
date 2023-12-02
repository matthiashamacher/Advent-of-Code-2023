from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import re


def parse(puzzle_input):
    input_array = puzzle_input.split('\n')
    games = {}

    for input_line in input_array:
        parts = re.match(r'Game (\d+): (.*)', input_line)
        game_id = int(parts.group(1))
        game_subsets = parts.group(2).split('; ')
        game_subset_arrays = []

        for subset in game_subsets:
            cubes = subset.split(', ')
            cubes_array = {}

            for cube in cubes:
                cube_notation = re.match(r'(\d+) ([a-z]+)', cube)
                cube_count = int(cube_notation.group(1))
                cube_color = cube_notation.group(2)
                cubes_array[cube_color] = cube_count

            game_subset_arrays.append(cubes_array)

        games[game_id] = game_subset_arrays

    return games


def part_a(data):
    possible = 0

    for game_id, game_subsets in data.items():
        impossible = False

        for game_subset in game_subsets:
            # Fail if one of them is higher than the limit
            if 'red' in game_subset.keys():
                if game_subset['red'] > 12:
                    impossible = True
                    break
            if 'green' in game_subset.keys():
                if game_subset['green'] > 13:
                    impossible = True
                    break
            if 'blue' in game_subset.keys():
                if game_subset['blue'] > 14:
                    impossible = True
                    break

        if impossible is False:
            possible = possible + game_id

    return possible


def part_b(data):
    power_sum = 0

    for game_id, game_subsets in data.items():
        red = 0
        blue = 0
        green = 0

        for game_subset in game_subsets:
            if 'red' in game_subset.keys():
                if game_subset['red'] > red:
                    red = game_subset['red']
            if 'green' in game_subset.keys():
                if game_subset['green'] > green:
                    green = game_subset['green']
            if 'blue' in game_subset.keys():
                if game_subset['blue'] > blue:
                    blue = game_subset['blue']

        power = red * green * blue
        power_sum = power_sum + power

    return power_sum


def test(examples: List[Example], solve_part_a=True, solve_part_b=True):
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
                else:
                    print(f"Part A: ERROR, expected {example.answer_a}, got {result}")

        if solve_part_b:
            if example.answer_b is None:
                print(f"Part B: No example solution provided.")
            else:
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
    puzzle = Puzzle(year=2023, day=2)

    localzone = datetime.now().astimezone().tzinfo
    now = datetime.now().astimezone(tz=localzone)

    if puzzle.unlock_time() > now:
        print(f"AOC Day {puzzle.day} will unlock at {puzzle.unlock_time()}!")
        exit(0)

    print(f"Day {puzzle.day}: {puzzle.title}")
    print()
    print("Testing examples")
    test(puzzle.examples, True, True)
    print()
    print("Solving Input")
    solve(puzzle, True, True, True)
