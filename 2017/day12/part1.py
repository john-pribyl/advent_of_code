from collections import deque

def traverse_graph(adjacency_list):
    seen = set()
    to_visit = deque()
    to_visit.append(0)

    while len(to_visit) > 0:
        node_index = to_visit.popleft()
        seen.add(node_index)
        
        for neighbor in adjacency_list[node_index]:
            if neighbor not in seen:
                to_visit.append(neighbor)

    return len(seen)


def parse_input(input):
    parsed_input = {}
    for line in input:
        line_parts = line.split("<->")
        program_id = int(line_parts[0].strip())
        neighbors = list(map(lambda x: int(x.strip()), line_parts[1].split(',')))
        parsed_input[program_id] = neighbors
    return parsed_input

def main():
    input = input = open('./input.txt', 'r').read().strip().split('\n')
    parsed_input = parse_input(input)

    result = traverse_graph(parsed_input)
    print(f"Part 1: {result}")

main()