use std::fs;
use std::collections::HashMap;
use std::collections::HashSet;

fn part2(input: &Vec<&str>) -> (usize, usize) {
    let mut claimed_squares: HashMap<(usize, usize), Vec<usize>> = HashMap::new();
    let mut valid_claims: HashSet<usize> = (1..input.len()+1).collect(); 
    let _ = input
        .iter()
        .for_each(|line| {
            // Parse line
            let line_parts: Vec<usize> = line
                .split(|c: char| !c.is_numeric())
                .filter_map(|val_string| val_string.parse::<usize>().ok())
                .collect();

            let (claim_id, start_col_idx, start_row_idx, section_width, section_height) =
                (line_parts[0], line_parts[1], line_parts[2], line_parts[3], line_parts[4]);
            
            // Mark squares as occupied
            (0..section_width)
                .flat_map(|column_offset| {
                    (0..section_height).map(move |row_offset| {
                        (start_row_idx + row_offset, start_col_idx + column_offset)
                    })
                })
                .for_each(|(row_index, column_index)| {
                    claimed_squares
                        .entry((row_index, column_index))
                        .and_modify(|claim_ids| {
                            claim_ids.push(claim_id);
                            // Invalidate all IDs at this coordinate
                            claim_ids.iter().for_each(|id| {
                                valid_claims.remove(id);
                            });
                        })
                        .or_insert_with(|| vec![claim_id]);
                });
        });

    let part1_result = claimed_squares
        .values()
        .filter(|values| values.len() > 1)
        .count();
    let part2_result = valid_claims
        .iter()
        .next()
        .expect("No valid claims remain");
    
    (part1_result, *part2_result)
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 & 2Example
    let (part1_example_result, part2_example_result) = part2(&example_instructions);
    println!("Part 1 (example): {:?}", part1_example_result);
    println!("Part 2 (example): {:?}", part2_example_result);

    // # Part 1 & 2
    let (part1_result, part2_result) = part2(&instructions);
    println!("Part 1: {:?}", part1_result);
    println!("Part 2: {:?}", part2_result);
}