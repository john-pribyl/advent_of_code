def part1(input):
    num_doubles = 0
    num_triples = 0

    for line in input:
        # Build char map of the line
        seen_letters = {}
        for char in line:
            seen_letters[char] = seen_letters.get(char, 0) + 1

        # Check for double or triple letters
        char_counts = seen_letters.values()
        if 3 in char_counts:
            num_triples += 1
        if 2 in char_counts:
            num_doubles += 1   

    return num_doubles * num_triples

def part2(input):
    # Do pairwise comparison of strings in input
    for line1 in input:
        for line2 in input:
            if line1 == line2:
                continue

            # Go char by char and compare for equality
            # Exit if more than one char is different
            num_differences = 0
            common_letters = []
            for char1, char2 in zip(line1, line2):
                if char1 == char2:
                    common_letters.append(char1)
                else:
                    num_differences += 1
                    if num_differences > 1:
                        break

            if num_differences <= 1:
                return "".join(common_letters)
            


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    example2_input = open('./example2.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part1_example_result = part2(example2_input)
    print(f"Part 2 (example): {part1_example_result}")

    # Part 2
    part1_result = part2(input)
    print(f"Part 2: {part1_result}")


main()