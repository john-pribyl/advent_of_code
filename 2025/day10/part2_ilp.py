import pulp

class MachineSchematic:
    def __init__(self, desired_state, button_config, joltage_limits):
        self.desired_state = desired_state
        self.button_config = button_config
        self.joltage_limits = joltage_limits

def parse_input(input):
    machine_schematics = []
    for line in input:
        opening_bracket_idx = line.index('[')
        closing_bracket_idx = line.index(']')
        desired_state = line[opening_bracket_idx+1:closing_bracket_idx]

        opening_curly_brace_idx = line.index('{')
        closing_curly_brace_idx = line.index('}')
        joltage_limits = line[opening_curly_brace_idx+1:closing_curly_brace_idx].split(',')
        joltage_limit_list = [0] * len(joltage_limits)
        for idx in range(len(joltage_limits)):
            joltage_limit_list[idx] = int(joltage_limits[idx])
       

        button_config = line[closing_bracket_idx+1:opening_curly_brace_idx-1].split()
        for idx in range(len(button_config)):
            button = button_config[idx]
            parsed_button = []
            lights = button[1:len(button)-1].split(',')
            for jdx in range(len(lights)):
                parsed_button.append(int(lights[jdx]))
            button_config[idx] = set(parsed_button)
        
        machine_schematics.append(MachineSchematic(desired_state, button_config, joltage_limit_list))

    return machine_schematics

def part2(machine_schematics):
    result = 0
    for idx, machine_schematic in enumerate(machine_schematics):
        depth = configure_joltage(machine_schematic)
        result += depth
        if idx < 3 or depth > 0:  # Print first 3 and any non-zero results
            print(f"Machine {idx + 1}/{len(machine_schematics)}: depth {depth}, total so far: {result}")

    return result

def configure_joltage(machine_schematic):
    # Transform to linear algebra problem and use PULP to solve    
    target = machine_schematic.joltage_limits
    n_positions = len(target)
    n_buttons = len(machine_schematic.button_config)
    
    # Want to minimize button presses
    prob = pulp.LpProblem("Joltage_Configuration", pulp.LpMinimize)
    
    # Each button is turned into a variable of how many times it is pressed
    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(n_buttons)]
    
    # Want to minimize the sum of button presses
    prob += pulp.lpSum(x), "Total_Button_Presses"
    
    # Make sure that button presses add up to the target value
    for i in range(n_positions):
        # Sum of all buttons that affect position i
        constraint_expr = pulp.lpSum([x[j] for j in range(n_buttons) if i in machine_schematic.button_config[j]])
        prob += constraint_expr == target[i], f"Position_{i}_Constraint"
    
    # Have PULP solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    result = int(pulp.value(prob.objective))
    print(f"Found: {target} with {result} presses")
    return result



def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    parsed_example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().split('\n')
    parsed_input = parse_input(input)

    # Part 2 Example (Correct answer: 33)
    part2_example_result = part2(parsed_example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2 (Correct answer: 19293)
    part2_result = part2(parsed_input)
    print(f"Part 2: {part2_result}")

main()
