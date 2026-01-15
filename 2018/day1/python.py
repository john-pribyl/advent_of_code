def part1(input):
    return sum([int(line) for line in input])

def part2(input):
    current_value = 0
    seen_values = set()
    seen_values.add(current_value)
    
    while True:
        for line in input:
            current_value += int(line)
            if current_value in seen_values:
                return current_value
            else:
                seen_values.add(current_value)


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part1_example_result = part2(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 2
    part1_result = part2(input)
    print(f"Part 1: {part1_result}")


main()