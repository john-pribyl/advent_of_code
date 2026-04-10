use std::fs;

fn part1(input: Vec<&str>) -> isize {
    0
}

fn part2(input: &Vec<&str>) -> isize {
    0
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(example_instructions);
    println!("Part 1 (example): {}", part1_example_result);

    // // Part 1
    // let part1_result = part1(&instructions);
    // println!("Part 1: {}", part1_result);

    // // Part 2 Example
    // let part2_example_result = part2(&example_instructions);
    // println!("Part 2 (example): {:?}", part2_example_result);

    // // Part 2
    // let part2_result = part2(&instructions);
    // println!("Part 2: {:?}", part2_result);
}