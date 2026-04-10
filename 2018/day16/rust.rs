// To run this script, cd to root and run `cargo run --bin 2018day16 --release`
use std::fs;
use std::collections::HashMap;

type FunctionApplication = fn(&[usize], &[usize]) -> usize;

fn part1(part1_input: &Vec<&str>, operations: &HashMap<&str, FunctionApplication>) -> usize {
    let num_samples = (part1_input.len() / 4) + 1;
    (0..num_samples)
        .fold(0, |sample_count, sample_idx| {
            let line_idx = sample_idx * 4;
            let line = part1_input[line_idx];
            // Parse "Before" line
            let before_state: Vec<usize> = line
                .strip_prefix("Before: [")
                .unwrap()
                .trim_end_matches(']')
                .split(", ")
                .map(|s| s.parse().unwrap())
                .collect();

            // Parse opcode line
            let opcode_line = part1_input[line_idx + 1];
            let opcode_params: Vec<usize> = opcode_line
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();

            // Parse "After" line
            let after_state: Vec<usize> = part1_input[line_idx + 2]
                .strip_prefix("After:  [") 
                .unwrap()
                .trim_end_matches(']')
                .split(", ")
                .map(|s| s.parse().unwrap())
                .collect();

            // Check which operations would produce the given output from the input and parameters
            let num_matching_operations = operations.values()
                .fold(0, |num_matching_operations, func_application| {
                    let mut output_state = before_state.clone();
                    let target_register = opcode_params[3];
                    output_state[target_register] = func_application(&output_state, &opcode_params);
                    let operation_matches = output_state == after_state;
                    num_matching_operations + (operation_matches as usize)
                });
            let has_three_matches = num_matching_operations >= 3;
            sample_count + (has_three_matches as usize)
        })

}

fn part2(part1_input: &Vec<&str>, part2_input: &Vec<&str>, operations: &HashMap<&str, FunctionApplication>) -> Vec<usize> {
    // Pass through samples and figure out the mapping of opcode names to values
    let num_samples = (part1_input.len() / 4) + 1;
    let initial_state: HashMap<String, usize> = HashMap::new();
    let opcode_values = (0..num_samples)
        .fold(initial_state, |mut current_opcode_values, sample_idx| {
            let line_idx = sample_idx * 4;
            let line = part1_input[line_idx];

            // Parse "Before" line
            let before_state: Vec<usize> = line
                .strip_prefix("Before: [")
                .unwrap()
                .trim_end_matches(']')
                .split(", ")
                .map(|s| s.parse().unwrap())
                .collect();

            // Parse opcode line
            let opcode_params: Vec<usize> = part1_input[line_idx + 1]
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();

            // Parse "After" line
            let after_state: Vec<usize> = part1_input[line_idx + 2]
                .strip_prefix("After:  [") 
                .unwrap()
                .trim_end_matches(']')
                .split(", ")
                .map(|s| s.parse().unwrap())
                .collect();

            // Check which operations would produce the given output from the input and parameters
            let initial_sample_result: Vec<(usize, String)> = Vec::new();
            let sample_result = operations
                .iter()
                .fold(initial_sample_result, |mut sample_result, (func_name, func_application)| {
                    let mut output_state = before_state.clone();
                    let target_register = opcode_params[3];
                    output_state[target_register] = func_application(&output_state, &opcode_params);
                    if output_state == after_state && !current_opcode_values.contains_key(*func_name) {
                        sample_result.push((opcode_params[0], func_name.to_string()));
                    }
                    sample_result
                });

            if sample_result.len() == 1 {
                let (opcode_val, func_name) = &sample_result[0];
                current_opcode_values.insert(func_name.clone(), opcode_val.clone());
            }
            current_opcode_values
        });

    // We now know the mapping of opcode names to values, so we can run the program
    let opcode_names: HashMap<usize, String> = opcode_values
        .into_iter()
        .map(|(key, val)| (val, key))
        .collect();
    let initial_register_state: Vec<usize> = Vec::from([0,0,0,0]);
    part2_input
        .iter()
        .fold(initial_register_state, |mut current_register_state, line| {
            let opcode_params: Vec<usize> = line
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            let operation_name = opcode_names.get(&opcode_params[0]).unwrap();
            let target_register = &opcode_params[3];
            let func_application = operations.get(operation_name.as_str()).unwrap();
            current_register_state[*target_register] = func_application(&current_register_state, &opcode_params);

            current_register_state
        })
}


fn main() {
    // Dispatch table defined here since it can't be declared globally
    let operations: HashMap<&str, FunctionApplication> = HashMap::from([
        ("addr", (|registers, params| registers[params[1] as usize] + registers[params[2] as usize]) as FunctionApplication),
        ("addi", (|registers, params| registers[params[1] as usize] + params[2]) as FunctionApplication),
        ("mulr", (|registers, params| registers[params[1] as usize] * registers[params[2] as usize]) as FunctionApplication),
        ("muli", (|registers, params| registers[params[1] as usize] * params[2]) as FunctionApplication),
        ("banr", (|registers, params| registers[params[1] as usize] & registers[params[2] as usize]) as FunctionApplication),
        ("bani", (|registers, params| registers[params[1] as usize] & params[2]) as FunctionApplication),
        ("borr", (|registers, params| registers[params[1] as usize] | registers[params[2] as usize]) as FunctionApplication),
        ("bori", (|registers, params| registers[params[1] as usize] | params[2]) as FunctionApplication),
        ("setr", (|registers, params| registers[params[1] as usize]) as FunctionApplication),
        ("seti", (|_registers, params| params[1]) as FunctionApplication),
        ("gtir", (|registers, params| if params[1] > registers[params[2] as usize] { 1 } else { 0 }) as FunctionApplication),
        ("gtri", (|registers, params| if registers[params[1] as usize] > params[2] { 1 } else { 0 }) as FunctionApplication),
        ("gtrr", (|registers, params| if registers[params[1] as usize] > registers[params[2] as usize] { 1 } else { 0 }) as FunctionApplication),
        ("eqir", (|registers, params| if params[1] == registers[params[2] as usize] { 1 } else { 0 }) as FunctionApplication),
        ("eqri", (|registers, params| if registers[params[1] as usize] == params[2] { 1 } else { 0 }) as FunctionApplication),
        ("eqrr", (|registers, params| if registers[params[1] as usize] == registers[params[2] as usize] { 1 } else { 0 }) as FunctionApplication),
    ]);

    let part1_example_input = fs::read_to_string("2018/day16/part1_example.txt")
        .expect("Something went wrong reading the file");
    let part1_example_lines: Vec<&str> = part1_example_input.trim().split('\n').collect();
    let part1_input = fs::read_to_string("2018/day16/part1_input.txt")
        .expect("Something went wrong reading the file");
    let part1_input_lines: Vec<&str> = part1_input.trim().split('\n').collect();
    let part2_input = fs::read_to_string("2018/day16/part2_input.txt")
        .expect("Something went wrong reading the file");
    let part2_input_lines: Vec<&str> = part2_input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&part1_example_lines, &operations);
    println!("Part 1 (example): {:?}", part1_example_result);

    // Part 1
    let part1_result = part1(&part1_input_lines, &operations);
    println!("Part 1: {:?}", part1_result);

    // Part 2
    let part2_result = part2(&part1_input_lines, &part2_input_lines, &operations);
    println!("Part 2: {:?}", part2_result);
}