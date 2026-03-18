use std::fs;

#[derive(Debug, Clone)]
enum InstructionType {
    Cut(isize),
    Deal(isize),
    Reverse
}

fn part1(input: &Vec<&str>, card_count: isize, card_to_locate: isize, num_repitions: usize) -> isize {
    // Parse the instructions once
    let instructions: Vec<InstructionType> = input
        .iter()
        .map(|line| {
            let line_parts: Vec<&str> = line.trim().split_whitespace().collect();
            if line_parts[0] == "cut" {
                return InstructionType::Cut(line_parts[1].parse::<isize>().expect("Value not numeric"));
            }
            else if line_parts[0] == "deal" && line_parts[1] == "into" {
                return InstructionType::Reverse;
            }
            else if line_parts[0] == "deal" && line_parts[1] == "with" {
                return InstructionType::Deal(line_parts[3].parse::<isize>().expect("Value not numeric"));
            }
            else {
                panic!("Unmatched input!")
            }
        })
        .collect();

    (0..num_repitions).fold(card_to_locate, |current_card_idx, _| {
        instructions
            .iter()
            .fold(current_card_idx, |current_card_idx, instruction| {
                match instruction {
                    InstructionType::Cut(cut_idx) => {
                        (current_card_idx - cut_idx + card_count) % card_count
                    },
                    InstructionType::Reverse => {
                        (-current_card_idx - 1) % card_count
                    },
                    InstructionType::Deal(increment) => {
                        current_card_idx * increment % card_count
                    }
                }
            })
    })
    
}

fn part2(input: &Vec<&str>, card_count: i128, card_to_locate: i128, num_repetitions: i128) -> i128 {
    // Parse the instructions once
    // Each operation is a linear congruence, e.g. ax + b mod m
    // Can pipe each instruction into the next and accumulate a and b
    // Then when time to "run" the instructions the solution is closed form for one repitition
    let (scalar, translator) = input
        .iter()
        .fold((1, 0), |(scalar, translator), line| {
            let line_parts: Vec<&str> = line.trim().split_whitespace().collect();
            if line_parts[0] == "cut" {
                let cut_idx = line_parts[1].parse::<i128>().expect("Value not numeric");
                return (scalar, (translator - cut_idx + card_count) % card_count);
            }
            else if line_parts[0] == "deal" && line_parts[1] == "into" {
                return ((card_count - scalar) % card_count, (card_count - translator - 1) % card_count);
            }
            else if line_parts[0] == "deal" && line_parts[1] == "with" {
                let increment = line_parts[3].parse::<i128>().expect("Value not numeric");
                return ((scalar * increment)  % card_count, (translator * increment) % card_count);
            }
            else {
                panic!("Unmatched input!")
            }
        });

    // To do num_repititions shuffles, It's just composing (ax + b) mod m over and over
    // This becomes a geometrics series
    let total_forward_scalar = modular_exponentiation(scalar, num_repetitions, card_count);
    let forward_denominator_inverse = inverse_shuffle(scalar - 1, card_count);
    let total_forward_translator = (translator * (total_forward_scalar - 1 + card_count) % card_count) % card_count;
    let total_forward_translator = (total_forward_translator * forward_denominator_inverse) % card_count;

    // Now that we have the result of running the shuffle many times, we need to invert it.
    let final_scalar_inverse = inverse_shuffle(total_forward_scalar, card_count);
    (card_to_locate - total_forward_translator + card_count) * final_scalar_inverse % card_count
}

fn inverse_shuffle(target_value: i128, modulus: i128) -> i128 {
    let mut current_remainder = target_value;
    let mut next_remainder = modulus;
    
    let mut current_coefficient = 1;
    let mut next_coefficient = 0;

    // We continue until the remainder becomes 0
    while next_remainder != 0 {
        let quotient = current_remainder / next_remainder;

        let temporary_remainder = next_remainder;
        next_remainder = current_remainder % next_remainder;
        current_remainder = temporary_remainder;

        let temporary_coefficient = next_coefficient;
        next_coefficient = current_coefficient - (quotient * next_coefficient);
        current_coefficient = temporary_coefficient;
    }

    if current_coefficient < 0 {
        current_coefficient += modulus;
    }

    current_coefficient
}

fn modular_exponentiation(mut base: i128, mut exponent: i128, modulus: i128) -> i128 {
    let mut result = 1;
    base %= modulus;
    while exponent > 0 {
        if exponent % 2 == 1 {
            result = (result * base) % modulus;
        }
        base = (base * base) % modulus;
        exponent /= 2;
    }
    result
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_lines: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_lines: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_lines, 10, 7, 1);
    println!("Part 1 (example): {}", part1_example_result);

    //  Part 1
    let part1_result = part1(&input_lines, 10007, 2019, 1);
    println!("Part 1: {}", part1_result);

    // Part 2
    let part2_result = part2(&input_lines, 119_315_717_514_047, 2020, 101_741_582_076_661);
    println!("Part 2: {:?}", part2_result);
}