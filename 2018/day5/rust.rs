use std::fs;

fn part1(input: &str) -> usize {
    input
        .chars()
        .fold(Vec::with_capacity(input.len()), |mut chars_to_keep: Vec<char>, char| {
            if chars_to_keep.len() > 0 
                && char.to_ascii_lowercase().eq(&chars_to_keep[chars_to_keep.len() - 1].to_ascii_lowercase()) 
                && char != chars_to_keep[chars_to_keep.len() - 1] 
            {
                chars_to_keep.pop();
                return chars_to_keep;
            }

            chars_to_keep.push(char);

            chars_to_keep
        })
        .len()
}

fn part2(input: &str) -> usize {
    ('a'..'z')
        .map(|char_to_remove| {
            let filtered_string: String = input
                .chars()
                .filter(|char| !char.to_ascii_lowercase().eq(&char_to_remove.to_ascii_lowercase()))
                .collect();

            part1(&filtered_string)
        })
        .min()
        .unwrap_or(0)
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");

    // Part 1 Example
    let part1_example_result = part1(&example_input);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&input);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_input);
    println!("Part 2 (example): {:?}", part2_example_result);

    // Part 2
    let part2_result = part2(&input);
    println!("Part 2: {:?}", part2_result);
}