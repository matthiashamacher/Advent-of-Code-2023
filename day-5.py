from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import re


def parse(puzzle_input):
    input_array = puzzle_input.split('\n\n')

    result = {}

    for input_line in input_array:
        if re.match(r'seeds: ([\d+\s]+)', input_line):
            seeds = re.match(r'seeds: ([\d+\s]+)', input_line).group(1).split()
            result['seeds'] = seeds
        elif re.match(r'[a-z]+-[a-z]+-[a-z]+ map:.*', input_line):
            line_parts = input_line.split('\n')
            map_name = re.match(r'([a-z]+-[a-z]+-[a-z]+) map:.*', line_parts[0]).group(1)
            map_array = []

            for line in line_parts[1:]:
                [destination, source, range] = line.split()
                map_array.append([int(source), int(destination), int(range)])

            result[map_name] = map_array

    return result


def part_a(data):
    lowest_location = 0
    seeds = data['seeds']
    maps = list(data.items())[1:]

    for seed in seeds:
        seed = int(seed)

        for map in maps:
            for [source, destination, range] in map[1]:
                if seed < source or seed > (source + range):
                    continue
                elif seed <= (source + range):
                    seed = destination + (seed - source)
                    break

        if seed < lowest_location or lowest_location == 0:
            lowest_location = seed

    return lowest_location


def part_b(data):
    all_seeds = [int(seed) for seed in data['seeds']]
    maps = list(data.items())[1:]

    seeds = list(map(lambda i: range(all_seeds[i], all_seeds[i] + all_seeds[i + 1]), range(0, len(all_seeds), 2)))

    current_gen = seeds

    for map_definition in maps:
        found = []
        pre_search = current_gen

        for [source, destination, map_range_value] in map_definition[1]:
            map_range = range(source, source + map_range_value)
            offset = destination - source

            new_unconverted = []

            for r in pre_search:
                overlap = range(r.start, r.start)

                if r.start < map_range.stop and r.stop >= map_range.start:
                    overlap = range(max(r.start, map_range.start), min(r.stop, map_range.stop))

                left = range(r.start, overlap.start)
                if left.stop > left.start:
                    new_unconverted.append(left)

                if overlap.stop > overlap.start:
                    found.append(range(overlap.start + offset, overlap.stop + offset))

                right = range(overlap.stop, r.stop)
                if right.stop > right.start:
                    new_unconverted.append(right)

            pre_search = new_unconverted

        current_gen = found + pre_search

    return min(map(lambda r: r.start, current_gen))


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
    puzzle = Puzzle(year=2023, day=5)

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
