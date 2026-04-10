// To run this script, cd to root and run `cargo run --bin 2018day14`
use itertools::Itertools;
use itertools::FoldWhile::{Continue, Done};

fn part1(num_recipes: usize) -> String {
    let initial_state = (vec![3,7], 0, 1); // recipes, elf1_idx, elf2_idx

    let (final_recipes, _, _) = (0..)
        .fold_while(initial_state, |(mut recipes, elf1_idx, elf2_idx), _| {
            // Generate score and push digits to recipes
            let new_recipe_score = recipes[elf1_idx] + recipes[elf2_idx];
            if new_recipe_score >= 10 {
                recipes.push(new_recipe_score / 10);
            }
            recipes.push(new_recipe_score % 10);

            // Check if we're finished
            if recipes.len() >= num_recipes + 10 {
                return Done((recipes, elf1_idx, elf2_idx))
            }

            // Move elves and continue
            let new_elf1_idx = (elf1_idx + 1 + recipes[elf1_idx]) % recipes.len();
            let new_elf2_idx = (elf2_idx + 1 + recipes[elf2_idx]) % recipes.len();

            Continue((recipes, new_elf1_idx, new_elf2_idx))
        })
        .into_inner();
    
    final_recipes
        .iter()
        .skip(num_recipes)
        .take(10)
        .map(|score| score.to_string())
        .collect::<Vec<String>>()
        .join("")
        
}

fn part2(target_val: usize) -> usize {
    let target_length: u32 = target_val.to_string().len().try_into().unwrap();
    let target_modulus = 10usize.pow(target_length);
    let initial_state = (vec![3,7], 0, 1, 37); // recipes, elf1_idx, elf2_idx, sliding_window

    let (final_recipes, _, _, _) = (0..)
        .fold_while(initial_state, |(mut recipes, elf1_idx, elf2_idx, mut sliding_window), _| {
            // Generate score and parse digits
            let new_recipe_score = recipes[elf1_idx] + recipes[elf2_idx];
            
            let digit1 = if new_recipe_score >= 10 {
                Some(new_recipe_score / 10)
            } else {
                None
            };
            let digit2 = Some(new_recipe_score % 10);

            // Go digit-by-digit of new score and see if we've hit the target value
            for &digit in [digit1, digit2].iter().flatten() {
                recipes.push(digit);
                sliding_window = (sliding_window * 10 + digit) % target_modulus;
                if sliding_window == target_val {
                    return Done((recipes, elf1_idx, elf2_idx, sliding_window));
                }
            }

            // Not finished yet, move the elf pointers and continue
            let new_elf1_idx = (elf1_idx + 1 + recipes[elf1_idx]) % recipes.len();
            let new_elf2_idx = (elf2_idx + 1 + recipes[elf2_idx]) % recipes.len();

            Continue((recipes, new_elf1_idx, new_elf2_idx, sliding_window))
        })
        .into_inner();

    final_recipes.len() - target_length as usize
}

fn main() {
    // Part 1 Example
    let part1_example_result = part1(2018);
    println!("Part 1 (example): {:?}", part1_example_result);

    // # Part 1
    let part1_result = part1(157901);
    println!("Part 1: {:?}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(59414);
    println!("Part 2 (example): {:?}", part2_example_result);

    // Part 2
    let part2_result = part2(157901);
    println!("Part 2: {:?}", part2_result);
}