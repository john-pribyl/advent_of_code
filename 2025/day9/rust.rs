use std::fs;
use std::collections::HashMap;

fn part1(input: &Vec<&str>) -> usize {
    // Parse input to coordinates
    let mut parsed_coordinates: Vec<Vec<usize>> = Vec::new();
    for line in input {
        let parsed_line = line
            .split(',')
            .map(|val| val.parse().expect("Value is not numeric"))
            .collect();
        parsed_coordinates.push(parsed_line);
    }
    
    // Compute area of all pair-wise rectangles, keeping track of max
    let mut max_area = 0;
    for first_coords in &parsed_coordinates {
        for second_coords in &parsed_coordinates {
            let width = first_coords[0].abs_diff(second_coords[0]) + 1;
            let height = first_coords[1].abs_diff(second_coords[1]) + 1;
            let area = width * height;
            max_area = std::cmp::max(max_area, area);
        }
    }

    return max_area;
}

fn part2(input: &Vec<&str>) -> usize {
    // Parse input to coordinates
    let mut corner_tiles: Vec<Vec<usize>> = Vec::new();
    for line in input {
        let parsed_line = line
            .split(',')
            .map(|val| val.parse().expect("Value is not numeric"))
            .collect();
        corner_tiles.push(parsed_line);
    }

    // Construct boundary edges
    // When we build our rectangles later, we'll want to check if they're intersected by an edge
    // Hash edges by row/column for easier lookups
    let mut vertical_edges: HashMap<usize, Vec<(usize, usize)>> = HashMap::new();
    let mut horizontal_edges: HashMap<usize, Vec<(usize, usize)>> = HashMap::new();
    for idx in 0..corner_tiles.len() {
        let this_corner_coords = &corner_tiles[idx];
        let next_corner_coords = &corner_tiles[(idx + 1) % corner_tiles.len()];
        
        if this_corner_coords[0] == next_corner_coords[0] {
            // Found a vertical edge (x-coordinates are equal)
            let y_min = std::cmp::min(this_corner_coords[1], next_corner_coords[1]);
            let y_max = std::cmp::max(this_corner_coords[1], next_corner_coords[1]);
            // Initialize key if it doesn't exist
            if !vertical_edges.contains_key(&this_corner_coords[0]) {
                vertical_edges.insert(this_corner_coords[0], Vec::new());
            }
            // Push edge to the column
            if let Some(val) = vertical_edges.get_mut(&this_corner_coords[0]) {
                val.push((y_min, y_max));
            }
        } else if this_corner_coords[1] == next_corner_coords[1] {
            // Found a horizontal edge (y-coordinates are equal)
            let x_min = std::cmp::min(this_corner_coords[0], next_corner_coords[0]);
            let x_max = std::cmp::max(this_corner_coords[0], next_corner_coords[0]);
            // Initialize key if it doesn't exist
            if !horizontal_edges.contains_key(&this_corner_coords[1]) {
                horizontal_edges.insert(this_corner_coords[1], Vec::new());
            }
            // Push edge to the column
            if let Some(val) = horizontal_edges.get_mut(&this_corner_coords[1]) {
                val.push((x_min, x_max));
            }
        }
    }

    // Build rectangles and check if they're valid (not intersected by an edge)
    let mut max_area = 0;
    for first_coords in &corner_tiles {
        for second_coords in &corner_tiles {
            let x_min = std::cmp::min(first_coords[0], second_coords[0]);
            let x_max = std::cmp::max(first_coords[0], second_coords[0]);
            let y_min = std::cmp::min(first_coords[1], second_coords[1]);
            let y_max = std::cmp::max(first_coords[1], second_coords[1]);

            let mut rect_is_valid = true;

            // Check for intersecting vertical edge
            for &vertical_edge_x in vertical_edges.keys() {
                if x_min < vertical_edge_x && vertical_edge_x < x_max {
                    // Edge intersects the rectangle's top or bottom boundary
                    // Check if it is also between the rectangle's left and right boundary
                    let edges = &vertical_edges[&vertical_edge_x];
                    for edge in edges2 {
                        if edge.0 < y_max && y_min < edge.1 {
                            rect_is_valid = false;
                            break;
                        }
                    }
                }
            }

            // Check for intersecting horizontal edge
            for &horizontal_edge_y in horizontal_edges.keys() {
                if y_min < horizontal_edge_y && horizontal_edge_y < y_max {
                    // Edge intersects the rectangle's left or right boundary
                    // Check if it is also between the rectangle's top and bottom boundary
                    let edges = &horizontal_edges[&horizontal_edge_y];
                    for edge in edges {
                        if edge.0 < x_max && x_min < edge.1 {
                            rect_is_valid = false;
                            break;
                        }
                    }
                }
            }

            if rect_is_valid {
                let width = first_coords[0].abs_diff(second_coords[0]) + 1;
                let height = first_coords[1].abs_diff(second_coords[1]) + 1;
                let area = width * height;
                max_area = std::cmp::max(max_area, area); 
            }
        }
    }

    return max_area;
}

fn main() {
    // Example input
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_input_list: Vec<&str> = example_input.trim().split('\n').collect();

    // Input
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_list: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_input_list);
    println!("Part 1 (example): {}", part1_example_result);

    // Part 1
    let part1_result = part1(&input_list);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_input_list);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&input_list);
    println!("Part 2: {}", part2_result);
}