use std::{cmp::Reverse, collections::{BinaryHeap, HashMap, HashSet}, fs};

fn part1(input: Vec<(char, char)>) -> String {
    // For Kahn's algorithm, build adjacency map and indegree map
    let (prereqs_map, mut indegrees_map, node_set) = input
        .iter()
        .fold( 
            (HashMap::new(), HashMap::new(), HashSet::new()),
            |
                (mut prereqs_map, mut indegrees_map, mut node_set),
                (node, dependent)| {
                prereqs_map
                    .entry(node)
                    .or_insert(Vec::new())
                    .push(dependent);

                *indegrees_map
                    .entry(dependent)
                    .or_insert(0) += 1;

                node_set.insert(*node);
                node_set.insert(*dependent);

                (prereqs_map, indegrees_map, node_set)
            }
        );

        // Parse nodes with no indegrees to a min-heap queue
        let mut queue: BinaryHeap<Reverse<char>> = node_set
            .iter()
            .filter(|&node| indegrees_map.get(node).unwrap_or(&0) == &0)
            .map(|node| Reverse(*node))
            .collect();

        // BFS to process the queue
        std::iter::from_fn(|| {
            queue
                .pop()
                .map(|Reverse(current_node)| {
                    if let Some(dependents) = prereqs_map.get(&current_node) {
                        dependents
                            .iter()
                            .for_each(|dependent| {
                                *indegrees_map
                                    .entry(*dependent)
                                    .or_insert(0) -= 1;

                                if indegrees_map.get(dependent).unwrap_or(&0) == &0 {
                                    queue.push(Reverse(**dependent));
                                }
                            });
                    }

                    current_node
                })
        })
        .collect()

}

fn part2(input: &Vec<&str>, max_total_distance: usize) -> usize {
    0
}

fn parse_input(input: &Vec<&str>) -> Vec<(char, char)> {
    input
        .iter()
        .map(|line| {
            let nodes: Vec<&str> = line
                .split_whitespace()
                .collect();

            (
                nodes[1].chars().next().expect("Missing value"),
                nodes[7].chars().next().expect("Missing value")
            )
        })
        .collect()
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_lines: Vec<&str> = example_input.trim().split('\n').collect();
    let parsed_example_input = parse_input(&example_lines);
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_lines: Vec<&str> = input.trim().split('\n').collect();
    let parsed_input = parse_input(&input_lines);

    // Part 1 Example
    let part1_example_result = part1(parsed_example_input);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(parsed_input);
    println!("Part 1: {}", part1_result);

    // // Part 2 Example
    // let part2_example_result = part2(&parsed_example_input, 32);
    // println!("Part 2 (example): {:?}", part2_example_result);

    // // Part 2
    // let part2_result = part2(&parsed_input, 10_000);
    // println!("Part 2: {:?}", part2_result);
}