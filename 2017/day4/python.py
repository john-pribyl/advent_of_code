# Does part 1 and 2
def part1(input, perform_anagram_check = False):
    result = 0
    for line in input:
        is_valid = True
        distinct_words = set()
        for word in line.split():
            if perform_anagram_check:
                word = "".join(sorted(word))

            # check if word is duplicate
            if word in distinct_words:
                is_valid = False
                break
            distinct_words.add(word)

        result += is_valid
    
    return result

def main():
    part1_example_input = open('./part1_example.txt', 'r').read().strip().split('\n')
    part2_example_input = open('./part2_example.txt', 'r').read().strip().split('\n')
    input = open('./input.txt', 'r').read().strip().split('\n')

    # Part 1 (Example)
    part1_example_result = part1(part1_example_input)
    print(f"Part 1 (Example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 (Example)
    part2_example_result = part1(part2_example_input, True)
    print(f"Part 2 (Example): {part2_example_result}")

    # Part 2
    part2_result = part1(input, True)
    print(f"Part 2: {part2_result}")

main()