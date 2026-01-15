use std::fs;
use std::collections::HashSet;

fn part1(input: &Vec<&str>) -> isize {
    input
        .iter()
        .map(|val| val.parse::<isize>().expect("Value is not numeric"))
        .sum()
}

fn part2(input: &Vec<&str>) -> isize {
    let mut current_value = 0;
    let mut seen_values: HashSet<isize> = HashSet::from([0]);

    loop {
        for line in input {
            let line_value = line.parse::<isize>().expect("Value is not numeric");
            current_value += line_value;
            if !seen_values.insert(current_value) {
                return current_value;
            }
        }
    }
}

fn part2_functional(input: &Vec<&str>) -> isize {
    let mut seen_values: HashSet<isize> = HashSet::from([0]);
    input
        .iter()
        .cycle()
        .scan(0, |current_value, line| {
            *current_value += line.parse::<isize>().expect("Value is not numeric");
            Some(*current_value)
        })
        .find(|&value| {
            !seen_values.insert(value)
        })
        .unwrap()
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_instructions);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&instructions);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2_functional(&example_instructions);
    println!("Part 2 (example): {:?}", part2_example_result);

    // Part 2
    let part2_result = part2_functional(&instructions);
    println!("Part 2: {:?}", part2_result);
}