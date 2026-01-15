# Handles both Part1 and Part2
def part2(input):
    # Map of (row_idx, col_idx) tuples as keys and array of claims to the square as values
    # E.g. { (1,1): [1,2,3], (1,2): [2,3,4], ... }
    claimed_squares = {}
    # Set of valid claims. All claims are assumed valid initially,
    # but as contested spaces are found, claims will be removed
    valid_claims = set(range(1, len(input) + 1))
    for line in input:
        claimed_squares, valid_claims = process_claim(line, claimed_squares, valid_claims)

    # Part 1: Filter claimed_squares map down to entries that have more than one claim
    part1_result = len(list(filter(lambda key: len(claimed_squares.get(key, [])) > 1, claimed_squares.keys())))
    # Part 2: per problem description, only one claim will remain valid at the end
    part2_result = list(valid_claims)[0]
    return part1_result, part2_result

def process_claim(line, claimed_squares, valid_claims):
    # Parse line into section
    line_parts = line.split('@')
    claim_idx = int(line_parts[0][1:].strip())

    raw_coords, raw_dimensions = line_parts[1].split(':')
    start_col_idx, start_row_idx = raw_coords.split(',')
    section_width, section_height = raw_dimensions.split('x')

    # Mark squares as occupied
    for col_offset in range(int(section_width)):
        for row_offset in range (int(section_height)):
            row_idx = int(start_row_idx) + row_offset
            col_idx = int(start_col_idx) + col_offset

            if (row_idx, col_idx) in claimed_squares:
                claimed_squares[(row_idx, col_idx)].append(claim_idx)
                # If we're adding to an already claimed square, all claims to this square are invalid
                valid_claims -= set(claimed_squares[(row_idx, col_idx)])
            else:
                claimed_squares[(row_idx, col_idx)] = [claim_idx]

    return claimed_squares, valid_claims
        

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part2(example_input)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part2(input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

main()