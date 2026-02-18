from collections import defaultdict
import heapq

def part1(input):
    # Build adjacency list
    prereqs_map = defaultdict(list)
    indegree_map = defaultdict(int)
    nodes = set()
    for node, dependent in input:
        prereqs_map[node].append(dependent)
        indegree_map[dependent] += 1
        nodes.add(node)
        nodes.add(dependent)

    # BFS Kahn's algorithm to process queue
    # Queue up nodes with no prerequisites, keep queue sorted via heap
    queue = [node for node in nodes if not indegree_map[node]]
    heapq.heapify(queue)
    result = []
    while queue:
        current_node = heapq.heappop(queue)
        result.append(current_node)

        for child in prereqs_map[current_node]:
            # Notify dependents of completion
            indegree_map[child] -= 1
            if indegree_map[child] == 0:
                heapq.heappush(queue, child)

    return "".join(result)


def part2(input, num_workers, base_completion_time):
    # Build adjacency list
    prereqs_map = defaultdict(list)
    indegree_map = defaultdict(int)
    nodes = set()
    for node, dependent in input:
        prereqs_map[node].append(dependent)
        indegree_map[dependent] += 1
        nodes.add(node)
        nodes.add(dependent)

    # BFS Kahn's algorithm to process queue
    # Queue up nodes with no prerequisites, keep queue sorted via heap
    to_work_queue = [node for node in nodes if not indegree_map[node]]
    heapq.heapify(to_work_queue)
    worker_tasks = {} # { worker_idx: (task, remaining_time)}
    time_elapsed = -1
    result = []
    while len(result) < len(nodes):
        # Check for finished tasks
        completed_tasks_this_tick = []
        for worker_idx, (task, remaining_time) in worker_tasks.items():
            remaining_time -= 1
            # Check if worker has completed task
            if remaining_time == 0:
                completed_tasks_this_tick.append((worker_idx, task))
            else:
                worker_tasks[worker_idx] = (task, remaining_time)

        # Update queue
        for worker_idx, task in completed_tasks_this_tick:
            result.append(task)
            del worker_tasks[worker_idx]
            # Notify dependent tasks of completion
            for child in prereqs_map[task]:
                indegree_map[child] -= 1
                if indegree_map[child] == 0:
                    heapq.heappush(to_work_queue, child)

        # Assign tasks to open workers
        for worker_idx in range(num_workers):
            if worker_idx not in worker_tasks and len(to_work_queue) > 0:
                next_task = heapq.heappop(to_work_queue)
                completion_time = base_completion_time + ord(next_task) - 64
                worker_tasks[worker_idx] = (next_task, completion_time)

        time_elapsed += 1

    return time_elapsed

def parse_input(input):
    # Split line by whitespace and grab 2nd and 8th values
    return [(parts[1], parts[7]) for line in input for parts in [line.split(" ")]]

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().split('\n')
    input = parse_input(input)

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part1_example_result = part2(example_input, num_workers=2, base_completion_time=0)
    print(f"Part 2 (example): {part1_example_result}")

    # Part 2
    part1_result = part2(input, num_workers=5, base_completion_time=60)
    print(f"Part 2: {part1_result}")


main()