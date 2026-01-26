use std::fs;
use std::collections::HashMap;
use std::collections::HashSet;

fn part1(input: &Vec<&str>) -> usize {
    let (num_doubles, num_triples) = input
        .iter()
        .map(|line| {
            // Buld charmap, parse values to set, and check for 2 and 3
            let char_map = line.chars().fold(HashMap::new(), |mut char_map, char| {
                *char_map.entry(char).or_insert(0) += 1;
                char_map
            });
            let char_count_values = char_map.values().copied().collect::<HashSet<_>>();
            (char_count_values.contains(&2), char_count_values.contains(&3))
        })
        .fold(
            // Iterate over the results and count doubles and triples
            (0, 0),
            |(doubles_count, triples_count), (has_double, has_triple)| {
                (doubles_count + has_double as usize, triples_count + has_triple as usize)
            }
        );

    num_doubles * num_triples
}

fn part2(input: &Vec<&str>) -> Option<String> {
    let string_lengths = input
                .first()
                .map_or(0, |s| s.len());
    input
        .iter()
        .enumerate()
        .flat_map(|(idx, line1)| {
            // Pair up lines for comparison
            input
                .iter()
                .skip(idx + 1)
                .map(move |line2| (line1, line2))
        })
        .map(|(line1, line2)| {
            // Pair up chars in both strings and check for equality
            line1.chars()
                .zip(line2.chars())
                .filter(|(char1, char2)| char1 == char2)
                .map(|(char1, _)| char1)
                .collect::<String>()
        })
        .find(|common| {
            common.len() == string_lengths - 1
        })
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let example2_input = fs::read_to_string("example2.txt")
        .expect("Something went wrong reading the file");
    let example2_instructions: Vec<&str> = example2_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_instructions);
    println!("Part 1 (example): {:?}", part1_example_result);

    // # Part 1
    let part1_result = part1(&instructions);
    println!("Part 1: {:?}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example2_instructions);
    println!("Part 2 (example): {:?}", part2_example_result);

    // Part 2
    let part2_result = part2(&instructions);
    println!("Part 2: {:?}", part2_result);
}