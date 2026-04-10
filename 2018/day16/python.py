# Map operation names to their execution
OPERATIONS = {
    'addr': lambda registers, params: registers[params[1]] + registers[params[2]],
    'addi': lambda registers, params: registers[params[1]] + params[2],
    'mulr': lambda registers, params: registers[params[1]] * registers[params[2]],
    'muli': lambda registers, params: registers[params[1]] * params[2],
    'banr': lambda registers, params: registers[params[1]] & registers[params[2]],
    'bani': lambda registers, params: registers[params[1]] & params[2],
    'borr': lambda registers, params: registers[params[1]] | registers[params[2]],
    'bori': lambda registers, params: registers[params[1]] | params[2],
    'setr': lambda registers, params: registers[params[1]],
    'seti': lambda registers, params: params[1],
    'gtir': lambda registers, params: 1 if params[1] > registers[params[2]] else 0,
    'gtri': lambda registers, params: 1 if registers[params[1]] > params[2] else 0,
    'gtrr': lambda registers, params: 1 if registers[params[1]] > registers[params[2]] else 0,
    'eqir': lambda registers, params: 1 if params[1] == registers[params[2]] else 0,
    'eqri': lambda registers, params: 1 if registers[params[1]] == params[2] else 0,
    'eqrr': lambda registers, params: 1 if registers[params[1]] == registers[params[2]] else 0,
}

def part1(input: list[str]):
    result = 0
    before_state = None
    opcode_params = None
    after_state = None
    line_idx = 0

    while line_idx < len(input):
        line = input[line_idx]
        if line.startswith("Before:"):
            # Parse "Before" line
            _, before_values = line.split('[')
            before_values = before_values[:len(before_values) - 1]
            before_state = [int(val) for val in before_values.split(',')]

            # Parse opcode line
            opcode_line = input[line_idx + 1]
            opcode_params = [int(val) for val in opcode_line.split()]

            # Parse "After" line
            _, after_values = input[line_idx + 2].split('[')
            after_values = after_values[:len(after_values) - 1]
            after_state = [int(val) for val in after_values.split(',')]

            # Check which opcodes would produce the given output from the parameters
            num_matching_operations = 0
            for func_application in OPERATIONS.values():
                output_state = [val for val in before_state]
                target_register = opcode_params[3]
                output_state[target_register] = func_application(output_state, opcode_params)

                if output_state == after_state:
                    num_matching_operations += 1

            if num_matching_operations >= 3:
                result += 1

        line_idx += 4

    return result

def part2(part1_input, part2_input):
    before_state = None
    opcode_params = None
    after_state = None
    line_idx = 0
    operation_vals = {} # name key, number val

    # First part: run through the samples and identify the mapping of op names to values
    while line_idx < len(part1_input):
        line = part1_input[line_idx]
        if line.startswith("Before:"):
            # Parse "Before" line
            _, before_values = line.split('[')
            before_values = before_values[:len(before_values) - 1]
            before_state = [int(val) for val in before_values.split(',')]

            # Parse opcode line
            opcode_line = part1_input[line_idx + 1]
            opcode_params = [int(val) for val in opcode_line.split()]

            # Parse "After" line
            _, after_values = part1_input[line_idx + 2].split('[')
            after_values = after_values[:len(after_values) - 1]
            after_state = [int(val) for val in after_values.split(',')]

            # Check which opcodes would produce the given output from the parameters
            sample_result = []
            for func_name, func_application in OPERATIONS.items():
                output_state = [val for val in before_state]
                target_register = opcode_params[3]
                output_state[target_register] = func_application(before_state, opcode_params)

                # See if this operation produces the desired state (and if it's an operation we haven't already identified)
                if output_state == after_state and func_name not in operation_vals:
                    sample_result.append((opcode_params[0], func_name))

            # Check if only one operation could have produced the output (then we know the operation's value)
            if len(sample_result) == 1:
                opcode_val, func_name = sample_result[0]
                operation_vals[func_name] = opcode_val

        line_idx += 4

    # We now know each opcode_val, run the program
    opcode_names = { val: key for key, val in operation_vals.items()} # Flip the dictionary we just made
    current_state = [0, 0, 0, 0]
    for line in part2_input:
        opcode_params = [int(val) for val in line.split()]
        operation_name = opcode_names[opcode_params[0]]
        target_register = opcode_params[3]
        current_state[target_register] = OPERATIONS[operation_name](current_state, opcode_params)

    return current_state

def main():
    part1_example_input = open('./part1_example.txt', 'r').read().strip().split('\n')
    part1_input = open('./part1_input.txt', 'r').read().strip().split('\n')
    part2_input = open('./part2_input.txt', 'r').read().strip().split('\n')

    # Part 1 Example
    part1_example_result = part1(part1_example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(part1_input)
    print(f"Part 1: {part1_result}")

    # Part 2
    part2_result = part2(part1_input, part2_input)
    print(f"Part 2: {part2_result}")


main()