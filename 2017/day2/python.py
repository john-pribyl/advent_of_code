def part1(grid):
    # Go row by row and find min and max value of each row
    result = 0
    for row in grid:
        result += max(row) - min(row)
    return result

def part2(grid):
    result = 0
    for row in grid:
        # Check pairwise values in row for divisibility
        for left_idx in range(len(row)):
            found_pair = False
            for right_idx in range(left_idx + 1, len(row)):
                # Check if right value divides left value
                if row[left_idx] % row[right_idx] == 0:
                    result += row[left_idx] // row[right_idx]
                    found_pair = True
                    break
                # Check if left value divides right value
                if row[right_idx] % row[left_idx] == 0:
                    result += row[right_idx] // row[left_idx]
                    found_pair = True
                    break
            if found_pair:
                break

    return result
    
def parse_input(input):
    result = []
    for line in input:
        values = line.split()
        result.append([int(value) for value in values])
    return result

def main():
    part1_example_input = open('./part1_example.txt', 'r').read().strip().split("\n")
    parsed_part1_example_input = parse_input(part1_example_input)
    part2_example_input = open('./part2_example.txt', 'r').read().strip().split("\n")
    parsed_part2_example_input = parse_input(part2_example_input)
    input = open('./input.txt', 'r').read().strip().split("\n")
    parsed_input = parse_input(input)

    # Part 1 (Example)
    part1_example_result = part1(parsed_part1_example_input)
    print(f"Part 1 (Example): {part1_example_result}")

    # Part 1
    part1_result = part1(parsed_input)
    print(f"Part 1: {part1_result}")

    # Part 2 (Example)
    part2_example_result = part2(parsed_part2_example_input)
    print(f"Part 2 (Example): {part2_example_result}")

    # Part 2
    part2_result = part2(parsed_input)
    print(f"Part 2: {part2_result}")

main()