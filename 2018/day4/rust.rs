use std::collections::HashMap;
use chrono::{Duration, NaiveDateTime, Timelike};

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
struct LogEntry {
    timestamp: NaiveDateTime,
    detail: String
}

struct GuardData {
    id: usize,
    total_minutes_asleep: usize,
    sleep_minutes_map: HashMap<usize, usize>
}

struct ParsingState {
    all_guards_data: HashMap<usize, GuardData>,
    current_guard_id: Option<usize>,
    sleep_start_time: Option<NaiveDateTime> 
}


fn part2(input: &Vec<&str>) -> (Option<usize>, Option<usize>) {
    // Parse input to sorted LogEntries
    let mut log_entries: Vec<LogEntry> = input
        .iter()
        .map(|line| {
            let (timestamp_str, detail) = line[1..].split_once(']').unwrap();
            let timestamp = NaiveDateTime::parse_from_str(
                timestamp_str, 
                "%Y-%m-%d %H:%M"
            )
            .expect("Value is not a valid datetime");

            LogEntry {
                timestamp: timestamp,
                detail: detail.trim().to_string()
            }
        })
        .collect();

    log_entries.sort();

    let end_parsing_state = log_entries
        .into_iter()
        .fold(
            ParsingState {
                all_guards_data: HashMap::new(),
                current_guard_id: None,
                sleep_start_time: None
            },
            |mut current_state, entry| {
                if entry.detail.contains('#') {
                    // Start of guard's shift. Keep track of current guard and add guard
                    // to map if not already present 
                    let line_parts: Vec<&str> = entry.detail.split_whitespace().collect();
                    let id_str = &line_parts[1][1..];
                    let guard_id = id_str.parse::<usize>().expect("Guard ID is not numeric");
                    current_state.current_guard_id = Some(guard_id);
                    current_state.all_guards_data
                        .entry(guard_id)
                        .or_insert_with(|| GuardData {
                            id: guard_id,
                            total_minutes_asleep: 0,
                            sleep_minutes_map: HashMap::new(),
                        });
                } else if entry.detail == "falls asleep" {
                    // Record start of guard's sleep time
                    current_state.sleep_start_time = Some(entry.timestamp);
                } else {
                    if let (Some(guard_id), Some(start_time)) = (current_state.current_guard_id, current_state.sleep_start_time) {
                        let this_guard_data = current_state.all_guards_data
                            .get_mut(&guard_id)
                            .unwrap();
                        let mut current_time = start_time;
                        while current_time < entry.timestamp {
                            this_guard_data.total_minutes_asleep += 1;
                            *this_guard_data.sleep_minutes_map
                                .entry(current_time.minute() as usize)
                                .or_insert(0) += 1;
                            current_time += Duration::minutes(1);
                        }
                    }
                }
                current_state
            }
        );
    
    let part1_result = end_parsing_state.all_guards_data
        .values()
        .max_by_key(|guard_data| guard_data.total_minutes_asleep)
        .and_then(|guard| {
            guard.sleep_minutes_map
                .iter()
                .max_by_key(|&(_minute, count)| count)
                .map(|(minute, _count)| guard.id * minute)
        });
    
    let part2_result = end_parsing_state.all_guards_data
        .values()
        .filter_map(|guard_data| {
            guard_data.sleep_minutes_map
                .iter()
                .map(|(minute, count)| (guard_data.id, minute, count))
                .max_by_key(|&(_, _, count)| count)
        })
        .max_by_key(|&(_, _, count)| count)
        .map(|(id, minute, _)| id * minute);
        

    (part1_result, part2_result)
}

fn main() {
    let example_input = include_str!("example.txt");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let input = include_str!("input.txt");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 & 2 Example
    let (part1_example_result, part2_example_result) = part2(&example_instructions);
    println!("Part 1 (example): {:?}", part1_example_result);
    println!("Part 2 (example): {:?}", part2_example_result);

    // # Part 1 & 2
    let (part1_result, part2_result) = part2(&instructions);
    println!("Part 1: {:?}", part1_result);
    println!("Part 2: {:?}", part2_result);
}