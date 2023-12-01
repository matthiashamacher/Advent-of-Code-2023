from datetime import datetime
from typing import List

from aocd.models import Puzzle
from aocd.examples import Example

## Packages to solve the puzzle
import re
from word2number import w2n


def parse(puzzle_input):
    input_array = puzzle_input.split('\n')

    return input_array


def part_a(data):
    result = 0

    for line in data:
        numbers = re.findall("\d", line)

        if len(numbers) == 1:
            line_result = (int(numbers[0]) * 10) + int(numbers[0])
        else:
            line_result = (int(numbers[0]) * 10) + int(numbers[len(numbers) - 1])

        result = result + line_result

    return result


def part_b(data):
    result = 0

    for line in data:
        letters = list(line)
        numbers = []
        word = ''

        for letter in letters:
            if re.match('\d', letter):
                numbers.append(int(letter))
            else:
                word = word + letter
                match = re.match('.*(one|two|three|four|five|six|seven|eight|nine)', word)
                if match is not None:
                    try:
                        number_word = match.group(1)
                        number = w2n.word_to_num(number_word)
                        numbers.append(int(number))
                        word = list(word)[len(word) - 1]
                    except ValueError:
                        continue

        if len(numbers) == 1:
            line_result = (int(numbers[0]) * 10) + int(numbers[0])
        else:
            line_result = (int(numbers[0]) * 10) + int(numbers[len(numbers) - 1])

        result = result + line_result

    return result


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
    puzzle = Puzzle(year=2023, day=1)

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
