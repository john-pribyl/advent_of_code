# Does parts 1 and 2
def part1(input):
    _, part1_result, part2_result = dfs_parse_node(input, left=0, running_total=0)
    return part1_result, part2_result

def dfs_parse_node(input, left, running_total):
    # Get node information
    num_children = int(input[left])
    num_metadata_entries = int(input[left + 1])

    # Drill down any child nodes
    left += 2
    child_node_idx = 1
    child_node_data = {} # For lookups in part 2
    while child_node_idx <= num_children:
        left, running_total, child_node_value = dfs_parse_node(input, left, running_total)
        child_node_data[child_node_idx] = child_node_value
        child_node_idx += 1
    
    # Metadata appears after all child nodes, add it up
    # Part 1
    part1_left = left
    metadata_sum = 0
    for _ in range(num_metadata_entries):
        metadata_sum += int(input[part1_left])
        part1_left += 1

    # Part 2
    node_value = 0
    part2_left = left
    if num_children == 0:
        node_value = metadata_sum
    else:
        for _ in range(num_metadata_entries):
            child_node_idx = int(input[part2_left])
            if child_node_idx in child_node_data:
                node_value += child_node_data[child_node_idx]
            part2_left += 1

    return part1_left, running_total + metadata_sum, node_value   


def main():
    example_input = open('./example.txt', 'r').read().strip().split()
    input = open('./input.txt', 'r').read().strip().split()

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part1(input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

main()