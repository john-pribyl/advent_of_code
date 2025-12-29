use std::fs;
use std::collections::HashMap;

struct MachineSchematic {
    button_config: Vec<Vec<usize>>,
    desired_joltages: Vec<isize>
}

fn part2(machine_schematics: &Vec<MachineSchematic>) -> usize {
    let mut result = 0;
    for machine_schematic in machine_schematics {
        let button_combo_effects = get_button_combinations(
            &machine_schematic.button_config,
            machine_schematic.desired_joltages.len()
        );
        let min_presses_required = dfs_compute_min_presses(
            &machine_schematic.desired_joltages,
            &machine_schematic.button_config,
            &button_combo_effects
        );
        // Recursion returns max value if no solution is found
        if min_presses_required < usize::MAX {
            result += min_presses_required;
        }
    }
    return result;
}

fn dfs_compute_min_presses(
    current_joltages: &Vec<isize>,
    button_config:  &Vec<Vec<usize>>,
    button_combo_effects: &HashMap<Vec<usize>, Vec<Vec<usize>>>
) -> usize {
    // Check if we've hit target (reduced all joltages to 0)
    if current_joltages.iter().sum::<isize>() == 0 {
        return 0
    }

    // Find parity pattern of current joltages and button press combos that match
    // Applying those combos will result in all joltages being even
    let parity_pattern: Vec<usize> = current_joltages
        .iter()
        .map(|joltage| (joltage % 2).abs() as usize)
        .collect();
    
    let mut min_found = usize::MAX;
    if let Some(possible_combos) = button_combo_effects.get(&parity_pattern) {
        // Try each possible button press combo and ensure it's valid (does not reduce joltages below 0)
        for button_press_combo in possible_combos {
            let mut reduced_joltages = current_joltages.clone();
            let mut num_presses = 0;

            // Push all buttons in the button combination
            let mut is_valid_combo = true;
            for idx in 0..button_press_combo.len() {
                if button_press_combo[idx] == 1 {
                    // Apply button's effects to joltages
                    num_presses += 1;
                    let button_effect = &button_config[idx];

                    for joltage_idx in 0..current_joltages.len() {
                        if button_effect[joltage_idx] == 1 {
                            reduced_joltages[joltage_idx] -= 1;
                            if reduced_joltages[joltage_idx] < 0 {
                                is_valid_combo = false;
                                break;
                            }
                        }
                    }
                    if !is_valid_combo {
                        break;
                    }
                }
            }

            if !is_valid_combo {
                continue;
            }

            // This combo is valid and makes joltages even.
            // Reduce joltages by half and recurse
            reduced_joltages = reduced_joltages
                .iter()
                .map(|joltage| joltage / 2)
                .collect();
            let min_from_here = dfs_compute_min_presses(
                &reduced_joltages,
                &button_config,
                &button_combo_effects
            );

            // Recursion found a solution to the halved problem
            // Doulbe it and see if it's the new minimum
            if min_from_here < usize::MAX {
                let total_cost = 2 * min_from_here + num_presses; // Also add on current number of presses
                min_found = std::cmp::min(min_found, total_cost);
            }
        }
    }
    return min_found;
}

// Gets the parity effect of every combination of single-button presses
// I.e. How a button press combination affects whether each joltages is even or odd
fn get_button_combinations(
    button_config: &Vec<Vec<usize>>,
    num_joltages: usize
) -> HashMap<Vec<usize>, Vec<Vec<usize>>> {
    let num_buttons = button_config.len();
    let total_combinations = 1usize << num_buttons;
    let mut seen_combinations: HashMap<Vec<usize>, Vec<Vec<usize>>> = HashMap::new();

    for idx in 0..total_combinations {
        // Treat idx as a binary number and use bitshifting to figure out which buttons are pressed
        let mut current_combination: Vec<usize> = Vec::with_capacity(num_buttons);
        for bit_index in 0..num_buttons {
            let is_pressed = ((idx >> (num_buttons - 1 - bit_index)) & 1) as usize;
            current_combination.push(is_pressed);
        }

        // Press buttons in combo and note their affect on each joltage's parity
        let mut combination_effect = vec![0; num_joltages];
        for button_idx in 0..num_buttons {
            let button_effect = &button_config[button_idx];
            // Check if this button is pressed in this combination
            if current_combination[button_idx] == 1 {
                // Apply parity affect of button press to affected joltages
                for joltage_idx in 0..num_joltages {
                    if button_effect[joltage_idx] == 1 {
                        combination_effect[joltage_idx] = 1 - combination_effect[joltage_idx];
                    }
                }
            }
        }

        // Record result of button press combination
        seen_combinations
            .entry(combination_effect)
            .or_insert(Vec::new())
            .push(current_combination);
    }

    return seen_combinations;
}

fn parse_input(input: Vec<&str>) -> Vec<MachineSchematic> {
    let mut machine_schematics: Vec<MachineSchematic> = Vec::new();
    for line in input {
        // Parse desired joltages
        let opening_curly_brace_idx = line.chars().position(|char| char == '{').expect("Could not find opening curly brace in line");
        let closing_curly_brace_idx = line.chars().position(|char| char == '}').expect("Could not find closing curly brace in line");
        let desired_joltages: Vec<isize> = line[opening_curly_brace_idx+1..closing_curly_brace_idx]
            .split(',')
            .map(|val| val.parse().expect("Joltage value is not numeric"))
            .collect();

        // Parse buttons
        let closing_bracket_idx = line.chars().position(|char| char == ']').expect("Could not find closing bracket in line");
        let button_config = line[closing_bracket_idx+1..opening_curly_brace_idx-1]
            .split_whitespace()
            .map(|button| {
                // Extract lights that are affected by the button
                let affected_lights: &Vec<usize> = &button[1..button.len()-1]
                    .split(',')
                    .map(|light| light.parse::<usize>().expect("Light value is not numeric"))
                    .collect();

                // Build a vector of length {number of light} whose values are 1 for the affected lights and 0 otherwise
                let mut button_vector = vec![0; desired_joltages.len()];
                for light in affected_lights {
                    button_vector[*light] = 1;
                }
                return button_vector;
            })
            .collect();

        machine_schematics.push(MachineSchematic {
            desired_joltages: desired_joltages,
            button_config: button_config
        });
    }   

    return machine_schematics;
}

fn main() {
    // Example input
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_input_list: Vec<&str> = example_input.trim().split('\n').collect();
    let parsed_example_input = parse_input(example_input_list);

    // Input
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_list: Vec<&str> = input.trim().split('\n').collect();
    let parsed_input = parse_input(input_list);

    // Part 2 Example
    let part2_example_result = part2(&parsed_example_input);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&parsed_input);
    println!("Part 2: {}", part2_result);
}