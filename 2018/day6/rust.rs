use std::{collections::HashMap, fs};

fn part1(input: &Vec<&str>) -> isize {
    // Parse input nodes to coordinate tuples
    let nodes: Vec<(usize, (usize, usize))> = input
        .iter()
        .enumerate()
        .map(|(idx, line)| {
            let mut line_parts = line
                .split(", ")
                .map(|line_part| line_part.parse::<usize>().expect("Value is not numeric"));
        
            (
                idx,
                (
                    line_parts.next().expect("Missing first value"),
                    line_parts.next().expect("Missing second value")
                )
            )
        })
        .collect();

    // Find boundaries of search area
    let min_row = nodes.iter().min_by_key(|tuple| tuple.1.0).unwrap().1.0;
    let max_row = nodes.iter().max_by_key(|tuple| tuple.1.0).unwrap().1.0;
    let min_col = nodes.iter().min_by_key(|tuple| tuple.1.1).unwrap().1.1;
    let max_col = nodes.iter().max_by_key(|tuple| tuple.1.1).unwrap().1.1;

    // For each tile in the search area, compute its distance to every node
    (min_row..=max_row)
        .flat_map(|row_idx|
            (min_col..=max_col).map(move |col_idx| 
                // Generate coordinates to check
                (row_idx, col_idx)
            )
        )
        // Create map of node_idx keys, count of number of tiles that are closest to the node as values
        .fold(HashMap::new(), |mut closest_nodes, (row_idx, col_idx)| {
            // Compute distance between these coordinates and all nodes
            // Keep track of closest node and its distance
            let (closest_node_idx, _) = nodes
                .iter()
                .fold((0 as isize, usize::MAX),|(closest_node_idx, min_distance), node| {
                    let distance = row_idx.abs_diff(node.1.0) + col_idx.abs_diff(node.1.1);
                    if distance < min_distance {
                        // This node is closer than the previous closest
                        (node.0 as isize, distance)
                    } else if distance == min_distance {
                        // Tie with previous closest node
                        (-1, min_distance)
                    } else {
                        // This node is not closest
                        (closest_node_idx, min_distance)
                    }
                });
            
            // Update coordinate map with the closest found node for these coordinates
            // Ignore the tiles with a tie
            if closest_node_idx != -1 {
                *closest_nodes
                    .entry(closest_node_idx)
                    .or_insert(0) += 1;
            }

            closest_nodes
        })
        .into_iter()
        // Find node with highest count and return its count
        .map(|(_node_idx, count)| count)
        .max()
        .unwrap_or(0)
}

fn part2(input: &Vec<&str>, max_total_distance: usize) -> usize {
    // Parse input node to coordinate tuples
    let nodes: Vec<(usize, usize)> = input
        .iter()
        .map(|line| {
            let mut line_parts = line
                .split(", ")
                .map(|line_part| line_part.parse::<usize>().expect("Value is not numeric"));
        
            (
                line_parts.next().expect("Missing first value"),
                line_parts.next().expect("Missing second value")
            )
        })
        .collect();

    // Find boundaries of search area
    let min_row = nodes.iter().min_by_key(|tuple| tuple.0).unwrap().0;
    let max_row = nodes.iter().max_by_key(|tuple| tuple.0).unwrap().0;
    let min_col = nodes.iter().min_by_key(|tuple| tuple.1).unwrap().1;
    let max_col = nodes.iter().max_by_key(|tuple| tuple.1).unwrap().1;

    // For each tile in the search area, compute its distance to every node
    (min_row..max_row)
        .flat_map(|row_idx|
            (min_col.. max_col).map(move |col_idx| 
                // Generate coordinates to check
                (row_idx, col_idx)
            )
        )
        .filter(|(row_idx, col_idx)| {
            // Compute sum of distance between coordinates and all nodes
            nodes
                .iter()
                .map(|node| {
                    row_idx.abs_diff(node.0) + col_idx.abs_diff(node.1)
                })
                .sum::<usize>() < max_total_distance
        })
        .count()

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
    let part2_example_result = part2(&example_instructions, 32);
    println!("Part 2 (example): {:?}", part2_example_result);

    // Part 2
    let part2_result = part2(&instructions, 10_000);
    println!("Part 2: {:?}", part2_result);
}