import copy
import time

def part1(initial_state, rules, num_generations):
    current_state = copy.copy(initial_state)

    for _ in range(num_generations):
        new_state = copy.copy(current_state)

        # Go through each existing plot and check if it matches a rule
        # Need to also check plots 1 space to left and right of boundary
        for idx in range(min(current_state) - 1, max(current_state) + 2):
            pattern = f"{'#' if idx - 2 in current_state else '.'}{'#' if idx - 1 in current_state else '.'}{'#' if idx in current_state else '.'}{'#' if idx + 1 in current_state else '.'}{'#' if idx + 2 in current_state else '.'}"
            if pattern in rules:
                new_state.add(idx)
            else:
                new_state.discard(idx)
        
        current_state = new_state

    result = 0
    for val in current_state:
        result += int(val)
    
    return result

# Same as part 1 with an escape clause for the outer loop
def part2(initial_state, rules, num_generations):
    current_state = copy.copy(initial_state)

    final_iteration = 0
    for generation_idx in range(1, num_generations + 1):
        new_state = copy.copy(current_state)

        # Go through each existing plot and check if it matches a rule
        # Need to also check plots 1 space to left and right of boundary
        for idx in range(min(current_state) - 1, max(current_state) + 2):
            pattern = f"{'#' if idx - 2 in current_state else '.'}{'#' if idx - 1 in current_state else '.'}{'#' if idx in current_state else '.'}{'#' if idx + 1 in current_state else '.'}{'#' if idx + 2 in current_state else '.'}"
            if pattern in rules:
                new_state.add(idx)
            else:
                new_state.discard(idx)

        # Check if new state is just the old state shifted right by one index
        # After this, it will just continue gliding to the right, so no need to keep simulating
        # print("".join('0' if val == 0 else '#' if val in new_state else '.' for val in range(min(0,min(new_state)), max(new_state) + 1)))
        # time.sleep(0.1)
        if new_state == set([val + 1 for val in current_state]):
            print(f"Stabilized at iteration: {idx}")
            final_iteration = generation_idx
            current_state = new_state
            break
        
        current_state = new_state


    result = 0
    for val in current_state:
        result += int(val) + (num_generations - final_iteration)
    
    return result

def parse_input(input):
    initial_state = input[0].split(': ')[1]
    initial_state_set = set()
    # Only need to keep track of occupied indices
    for idx in range(len(initial_state)):
        if initial_state[idx] == '#':
            initial_state_set.add(idx)

    # Only need to keep track of rules that result in occupied indices
    rule_map = {}
    for idx in range(2, len(input)):
        input_val, output_val = input[idx].strip().split(' => ')
        if output_val == "#":
            rule_map[input_val] = output_val

    return initial_state_set, rule_map


def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    example_initial_state, example_rules = parse_input(example_input)
    input = open('./input.txt', 'r').read().strip().split('\n')
    initial_state, rules = parse_input(input)

    # Part 1 Example
    part1_example_result = part1(example_initial_state, example_rules, 20)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(initial_state, rules, 20)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part2_example_result = part2(example_initial_state, example_rules, 200)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2(initial_state, rules, 50_000_000_000)
    print(f"Part 2: {part2_result}")


main()