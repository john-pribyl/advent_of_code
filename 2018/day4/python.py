from datetime import datetime, timedelta

class LogEntry():
    def __init__(self, input_line):
        # Parse datetime from string
        time_string, detail = input_line[1:].split(']')
        timestamp = datetime.strptime(time_string.strip(), "%Y-%m-%d %H:%M")

        # Rest is the action
        self.timestamp = timestamp
        self.detail = detail.strip()

class GuardData():
    def __init__(self, id):
        self.id = id
        self.total_minutes_asleep = 0
        self.sleep_minutes_map = {}


def part2(input):
    # Parse the lines of log entries
    log_entries = []
    for line in input:
        log_entries.append(LogEntry(line))

    # Sort log entries by timestamp
    log_entries = sorted(log_entries, key=lambda log_entry: log_entry.timestamp)

    guard_data = {}
    guard_id = 0
    sleep_start_time = None

    # Part 2 running totals
    max_sleepy_guard_id = 0
    max_sleepy_minute = 0
    max_minute_sleep_count = 0
    for log_entry in log_entries:
        # Check for start of guard shift (has a # sign in the detail)
        if log_entry.detail.find('#') != -1:
            detail_parts = log_entry.detail.split()
            guard_id = int(detail_parts[1][1:])
            if guard_id not in guard_data:
                guard_data[guard_id] = GuardData(guard_id)
        elif log_entry.detail == "falls asleep":
            # Record start of sleeping window
            sleep_start_time = log_entry.timestamp
        else:
            # When waking up mark all minutes between start and now as asleep
            current_time = sleep_start_time
            this_guard_data = guard_data[guard_id]
            while current_time < log_entry.timestamp:
                this_guard_data.total_minutes_asleep += 1
                this_guard_data.sleep_minutes_map[current_time.minute] = this_guard_data.sleep_minutes_map.get(current_time.minute, 0) + 1
                # Part 2: Check if this is the sleepiest minute
                if this_guard_data.sleep_minutes_map.get(current_time.minute, 0) > max_minute_sleep_count:
                    max_minute_sleep_count = this_guard_data.sleep_minutes_map.get(current_time.minute, 0)
                    max_sleepy_guard_id = guard_id
                    max_sleepy_minute = current_time.minute
                current_time += timedelta(minutes=1)
            sleep_start_time = None

    # Part 1: Sort data by total minutes asleep to find sleepiest guard
    sorted_guard_data = sorted(guard_data.items(), key=lambda guard: guard[1].total_minutes_asleep, reverse=True)
    most_asleep_guard_id = sorted_guard_data[0][0]

    # Part 2: Sort sleepiest guard's data by minute most frequently asleep
    sorted_asleep_minutes = sorted(sorted_guard_data[0][1].sleep_minutes_map.items(), key=lambda timestamp: timestamp[1], reverse=True)
    most_asleep_minute = sorted_asleep_minutes[0][0]

    part1_result = most_asleep_guard_id * most_asleep_minute
    part2_result = max_sleepy_guard_id * max_sleepy_minute
    return part1_result, part2_result


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part2(example_input)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part2(input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")


main()