# Does part 1 and 2
def part1(input, skip_value):
    result = 0
    for idx in range(len(input)):
        next_char_idx = (idx + skip_value) % len(input)
        if input[idx] == input[next_char_idx]:
            result += int(input[idx])
    return result
    

def main():
    example_input = open('./example.txt', 'r').read().strip()
    input = open('./input.txt', 'r').read().strip()

    # Part 1 (Example)
    part1_example_result = part1(example_input, 1)
    print(f"Part 1 (Example): {part1_example_result}")

    # Part 1
    part1_result = part1(input, 1)
    print(f"Part 1: {part1_result}")

    # Part 2 (Example)
    part2_example_result = part1(example_input, len(example_input) // 2)
    print(f"Part 2 (Example): {part2_example_result}")

    # Part 2
    part2_result = part1(input, len(input) // 2)
    print(f"Part 2: {part2_result}")

main()