# Does parts 1 and 2
def part1(input, use_part2_rule=False):
    copy = [int(val) for val in input]
    length = len(copy)
    current_idx = 0
    count = 0
    while 0 <= current_idx < length:
        current_val = copy[current_idx]
        if use_part2_rule and current_val >= 3:
            copy[current_idx] -= 1
        else:
            copy[current_idx] += 1
        current_idx += current_val

        count += 1

    return count

def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    input = open('./input.txt', 'r').read().strip().split('\n')

    # Part 1 (Example)
    part1_example_result = part1(example_input)
    print(f"Part 1 (Example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 (Example)
    part2_example_result = part1(example_input, True)
    print(f"Part 2 (Example): {part2_example_result}")

    # Part 2
    part2_result = part1(input, True)
    print(f"Part 2: {part2_result}")

main()