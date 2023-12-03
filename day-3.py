from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import re


def parse(puzzle_input):
    result = []
    input_array = puzzle_input.split('\n')

    for input_line in input_array:
        result.append(list(input_line))

    return result


def part_a(data):
    part_number_sum = 0
    discarded_numbers = []

    for line_index, line in enumerate(data):
        number = False
        part_number = ''

        for char_index, char in enumerate(line):
            if not re.match(r'\d', char):
                if number:
                    part_int = int(part_number)
                    part_number_sum = part_number_sum + part_int
                    number = False
                elif len(part_number) > 0:
                    discarded_numbers.append(part_number)

                part_number = ''
                continue
            else:
                part_number += char

                if number:
                    continue

                if find_symbol(line_index, char_index, data):
                    number = True

        if number:
            part_int = int(part_number)
            part_number_sum = part_number_sum + part_int

    return part_number_sum


def part_b(data):
    gear_ration_sum = 0

    found_numbers = []
    for line_index, line in enumerate(data):
        gear = '*' in line

        if not gear:
            continue

        for char_index, char in enumerate(line):
            if char != '*':
                continue

            part_numbers = find_part_numbers(line_index, char_index, data)

            if len(part_numbers) != 2:
                continue

            found_numbers.append([int(part_numbers[0]), int(part_numbers[1])])

            gear_ration_sum = gear_ration_sum + (int(part_numbers[0]) * int(part_numbers[1]))

    return gear_ration_sum


def find_symbol(line_index: int, char_index: int, data: List[List[str]]):
    previous_line = not line_index - 1 == -1
    next_line = not line_index + 1 == len(data)
    previous_char = not char_index - 1 == -1
    next_char = not char_index + 1 == len(data[line_index])

    if previous_line and re.match(r'[^0-9.]', data[line_index - 1][char_index]):
        return True

    if previous_line and previous_char and re.match(r'[^0-9.]', data[line_index - 1][char_index - 1]):
        return True

    if previous_line and next_char and re.match(r'[^0-9.]', data[line_index - 1][char_index + 1]):
        return True

    if next_line and re.match(r'[^0-9.]', data[line_index + 1][char_index]):
        return True

    if next_line and previous_char and re.match(r'[^0-9.]', data[line_index + 1][char_index - 1]):
        return True

    if next_line and next_char and re.match(r'[^0-9.]', data[line_index + 1][char_index + 1]):
        return True

    if previous_char and re.match(r'[^0-9.]', data[line_index][char_index - 1]):
        return True

    if next_char and re.match(r'[^0-9.]', data[line_index][char_index + 1]):
        return True

    return False


def find_part_numbers(line_index: int, char_index: int, data: List[List[str]]):
    previous_line = not line_index - 1 == -1
    next_line = not line_index + 1 == len(data)
    previous_char = not char_index - 1 == -1
    next_char = not char_index + 1 == len(data[line_index])

    part_numbers = []

    if previous_line:
        if re.match(r'\d', data[line_index - 1][char_index]):
            number = get_number(char_index, data[line_index - 1])
            part_numbers.append(number)
        else:
            if next_char and re.match(r'\d', data[line_index - 1][char_index + 1]):
                number = get_number(char_index + 1, data[line_index - 1])
                part_numbers.append(number)

            if previous_char and re.match(r'\d', data[line_index - 1][char_index - 1]):
                number = get_number(char_index - 1, data[line_index - 1])
                part_numbers.append(number)

    if len(part_numbers) == 2:
        return part_numbers

    if next_line:
        if re.match(r'\d', data[line_index + 1][char_index]):
            number = get_number(char_index, data[line_index + 1])
            part_numbers.append(number)
        else:
            if next_char and re.match(r'\d', data[line_index + 1][char_index + 1]):
                number = get_number(char_index + 1, data[line_index + 1])
                part_numbers.append(number)

            if previous_char and re.match(r'\d', data[line_index + 1][char_index - 1]):
                number = get_number(char_index - 1, data[line_index + 1])
                part_numbers.append(number)

    if len(part_numbers) == 2:
        return part_numbers

    if previous_char and re.match(r'\d', data[line_index][char_index - 1]):
        number = get_number(char_index - 1, data[line_index])
        part_numbers.append(number)

    if next_char and re.match(r'\d', data[line_index][char_index + 1]):
        number = get_number(char_index + 1, data[line_index])
        part_numbers.append(number)

    return part_numbers


def get_number(char_index: int, line: List[str]):
    number = line[char_index]
    next_char_index = char_index + 1
    previous_char_index = char_index - 1

    while next_char_index != len(line) and re.match(r'\d', line[next_char_index]):
        number += line[next_char_index]
        next_char_index += 1

    while previous_char_index != -1 and re.match(r'\d', line[previous_char_index]):
        number = line[previous_char_index] + number
        previous_char_index -= 1

    return number


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
    puzzle = Puzzle(year=2023, day=3)

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
