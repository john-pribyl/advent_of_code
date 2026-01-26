import math

def part1(input, letter_to_remove = None):
    # Stack will hold letters to keep
    letter_stack = []
    
    for char in input:
        # if a skip letter is specified, skip it
        if letter_to_remove and char.lower() == letter_to_remove:
            continue

        # Check if this char is the same letter as previous but a different capitalization
        if letter_stack and char.lower() == letter_stack[-1].lower() and char != letter_stack[-1]:
            letter_stack.pop()
            continue

        # This char is ok, add it
        letter_stack.append(char)

    return "".join(letter_stack)

def part2(input):
    min_length = math.inf
    unique_letters = set(input.lower())
    for letter in unique_letters:
        # Run part 1 with removal of each char and keep track of the min result
        reacted_string = part1(input, letter)
        min_length = min(len(reacted_string), min_length)

    return min_length


def main():
    example_input = open('./example.txt', 'r').read()
    input = open('./input.txt', 'r').read()

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {len(part1_example_result)}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {len(part1_result)}")

    # Part 2 Example
    part1_example_result = part2(example_input)
    print(f"Part 2 (example): {part1_example_result}")

    # Part 2
    part1_result = part2(input)
    print(f"Part 2: {part1_result}")


main()