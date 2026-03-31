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
    // Each operation is a linear congruence, e.g. ax + b mod m. The result is also a linear congruence
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
    let total_scalar = modular_exponentiation(scalar, num_repetitions, card_count);
    let total_translator = (translator * (total_scalar - 1 + card_count) % card_count) 
        * inverse_shuffle(scalar - 1, card_count) % card_count;

    // Found the total forward scalar and translator, need to invert them
    ((card_to_locate - total_translator + card_count) % card_count) 
        * inverse_shuffle(total_scalar, card_count) % card_count
}

fn inverse_shuffle(target_value: i128, modulus: i128) -> i128 {
    // Inner recursive function to maintain the state of the Euclidean Algorithm
    fn extended_euclidean_recursive(
        current_remainder: i128,
        next_remainder: i128,
        current_coefficient: i128,
        next_coefficient: i128,
        modulus: i128,
    ) -> i128 {
        if next_remainder == 0 {
            // Base case: return the coefficient adjusted to be within [0, modulus)
            return (current_coefficient + modulus) % modulus;
        }

        let quotient = current_remainder / next_remainder;

        extended_euclidean_recursive(
            next_remainder,
            current_remainder % next_remainder,
            next_coefficient,
            current_coefficient - (quotient * next_coefficient),
            modulus,
        )
    }

    extended_euclidean_recursive(target_value, modulus, 1, 0, modulus)
}

fn modular_exponentiation(base: i128, exponent: i128, modulus: i128) -> i128 {
    fn exponentiate_recursive(
        current_base: i128,
        remaining_exponent: i128,
        accumulated_result: i128,
        modulus: i128,
    ) -> i128 {
        if remaining_exponent == 0 {
            return accumulated_result;
        }

        // If the exponent is odd, multiply the current base into our result
        let next_result = if remaining_exponent % 2 == 1 {
            (accumulated_result * current_base) % modulus
        } else {
            accumulated_result
        };

        // Square the base and halve the exponent for the next bit
        exponentiate_recursive(
            (current_base * current_base) % modulus,
            remaining_exponent / 2,
            next_result,
            modulus,
        )
    }

    exponentiate_recursive(base % modulus, exponent, 1, modulus)
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