from collections import deque
import heapq

def part1(entrance_coords, exit_coords, path_graph):
    # BFS to find path, portal endpoint are already marked as neighbors of each other,
    # so no need to handle portal logic
    queue = deque([(entrance_coords, 0)])
    seen = set()
    while len(queue) > 0:
        current_coords, current_distance = queue.popleft()

        # Check if we hit the exit
        if current_coords == exit_coords:
            return current_distance
        
        # Queue up neighbors for visiting
        seen.add(current_coords)
        for neighbor_coords in path_graph[current_coords]:
            if neighbor_coords not in seen:
                queue.append((neighbor_coords, current_distance + 1))
    
    return "path not found"
    

def part2(entrance_coords, exit_coords, path_graph, portals, inner_portals, outer_portals):
    # Build weighted graph of connections between portals
    connected_portals = {}
    connected_portals[entrance_coords] = bfs_find_reachable_portals(path_graph, entrance_coords, inner_portals, outer_portals, entrance_coords, exit_coords)
    for _, endpoints in portals.items():
        for endpoint_coords in endpoints:
            connected_portals[endpoint_coords] = bfs_find_reachable_portals(path_graph, endpoint_coords, inner_portals, outer_portals, entrance_coords, exit_coords)

    # Do BFS traversal of graph, use heap to process the shortest cumulative distances first
    heap_queue = [(0, 0, entrance_coords)] # (distance, level, coordinates)
    seen = set()
    while len(heap_queue) > 0:
        current_distance, current_level, current_coords = heapq.heappop(heap_queue)
        # Check if we've been at this portal at this level before
        if (current_level, current_coords) in seen:
            continue
        seen.add((current_level, current_coords))

        available_portals = connected_portals[current_coords]
        # Check for exit
        if current_level == 0 and available_portals["exit"] != None:
            return current_distance + available_portals["exit"]
        
        # Queue up neighboring portals
        if current_level > 0: # Can't use outer portals at base level
            for portal_coords, distance in available_portals["outer_portals"].items():
                portal_exit = outer_portals[portal_coords]
                heapq.heappush(heap_queue, (current_distance + distance + 1, current_level - 1, portal_exit))
        for portal_coords, distance in available_portals["inner_portals"].items():
            portal_exit = inner_portals[portal_coords]
            heapq.heappush(heap_queue, (current_distance + distance + 1, current_level + 1, portal_exit))

    return "Could not find path"

def bfs_find_reachable_portals(path_graph, start_coords, inner_portals, outer_portals, entrance_coords, exit_coords):
    # Classify reachable portals
    result = {
        "entrance": None,
        "exit": None,
        "inner_portals": {},
        "outer_portals": {}
    }

    # BFS to find reachable portals
    queue = deque([(0, start_coords)])
    seen = set()
    while len(queue) > 0:
        current_distance, current_coords = queue.popleft()
        if current_coords in seen:
            continue
        seen.add(current_coords)

        # Check if we've found a portal (stop going down this path)
        if current_coords in inner_portals and current_coords != start_coords:
            result["inner_portals"][current_coords] = current_distance
            continue
        elif current_coords in outer_portals and current_coords != start_coords:
            result["outer_portals"][current_coords] = current_distance
            continue
        elif current_coords == entrance_coords and current_coords != start_coords:
            result["entrance"] = current_distance
            continue
        elif current_coords == exit_coords and current_coords != start_coords:
            result["exit"] = current_distance
            continue

        # Visit neighbors
        for neighbor_coords in path_graph[current_coords]:
            if neighbor_coords not in seen:
                queue.append((current_distance + 1, neighbor_coords))

    return result

def parse_input(input):
    height = len(input)
    width = len(input[2])

    portals = {}
    path_graph = {}
    entrance = None
    exit = None
    for row_idx in range(height):
        for col_idx in range(width):
            # Check for portal letters
            if input[row_idx][col_idx].isalpha():
                # Check if portal letters are positioned horizontally
                if col_idx < width - 1 and input[row_idx][col_idx + 1].isalpha():
                    portal_name = f"{input[row_idx][col_idx]}{input[row_idx][col_idx + 1]}"
                    portal_exit = None
                    # Got portal name, find nearest path cell
                    if col_idx > 0 and input[row_idx][col_idx - 1] == ".":
                        portal_exit = (row_idx, col_idx - 1)
                    else:
                        portal_exit = (row_idx, col_idx + 2)
                    
                    # Check if portal is entrance or exit
                    if portal_name == "AA":
                        entrance = portal_exit
                    elif portal_name == "ZZ":
                        exit = portal_exit
                    # Check if portal's other end has already been found or not
                    elif portal_name in portals:
                        other_exit = portals[portal_name]
                        if portal_exit not in path_graph:
                            path_graph[portal_exit] = [other_exit]
                        else:
                            path_graph[portal_exit].append(other_exit)

                        if other_exit not in path_graph:
                            path_graph[other_exit] = [portal_exit]
                        else:
                            path_graph[other_exit].append(portal_exit)
                    # No connection yet, save portal for later
                    else:
                        portals[portal_name] = portal_exit
                # check if portal letters are positioned vertically
                elif row_idx < height - 1 and input[row_idx + 1][col_idx].isalpha():
                    portal_name = portal_name = f"{input[row_idx][col_idx]}{input[row_idx + 1][col_idx]}"
                    portal_exit = None
                    if row_idx > 0 and input[row_idx - 1][col_idx] == ".":
                        portal_exit = (row_idx - 1, col_idx)
                    else:
                        portal_exit = (row_idx + 2, col_idx)

                    if portal_name == "AA":
                        entrance = portal_exit
                    elif portal_name == "ZZ":
                        exit = portal_exit
                    elif portal_name in portals:
                        other_exit = portals[portal_name]
                        if portal_exit not in path_graph:
                            path_graph[portal_exit] = [other_exit]
                        else:
                            path_graph[portal_exit].append(other_exit)

                        if other_exit not in path_graph:
                            path_graph[other_exit] = [portal_exit]
                        else:
                            path_graph[other_exit].append(portal_exit)
                    else:
                        portals[portal_name] = portal_exit
            # Check for path cell
            elif input[row_idx][col_idx] == ".":
                if (row_idx, col_idx) not in path_graph:
                    path_graph[(row_idx, col_idx)] = []
                # check for neighboring path cells
                for (row_offset, col_offset) in [(1,0), (-1,0), (0,1), (0,-1)]:
                    if input[row_idx + row_offset][col_idx + col_offset] == ".":
                        path_graph[(row_idx, col_idx)].append((row_idx + row_offset, col_idx + col_offset))

    return entrance, exit, path_graph

def parse_input_part2(input):
    height = len(input)
    width = len(input[2])

    unconnected_portals = {}
    connected_portals = {}
    path_graph = {}
    entrance = None
    exit = None
    for row_idx in range(height):
        for col_idx in range(width):
            # Check for portal letters
            if input[row_idx][col_idx].isalpha():
                # Check if portal letters are positioned horizontally
                if col_idx < width - 1 and input[row_idx][col_idx + 1].isalpha():
                    portal_name = f"{input[row_idx][col_idx]}{input[row_idx][col_idx + 1]}"
                    portal_exit = None
                    # Got portal name, find nearest path cell
                    if col_idx > 0 and input[row_idx][col_idx - 1] == ".":
                        portal_exit = (row_idx, col_idx - 1)
                    else:
                        portal_exit = (row_idx, col_idx + 2)
                    
                    # Check if portal is entrance or exit
                    if portal_name == "AA":
                        entrance = portal_exit
                    elif portal_name == "ZZ":
                        exit = portal_exit
                    # Check if portal's other end has already been found or not
                    elif portal_name in unconnected_portals:
                        other_exit = unconnected_portals[portal_name]
                        if portal_name not in connected_portals:
                            connected_portals[portal_name] = [portal_exit, other_exit]
                    # No connection yet, save portal for later
                    else:
                        unconnected_portals[portal_name] = portal_exit
                # check if portal letters are positioned vertically
                elif row_idx < height - 1 and input[row_idx + 1][col_idx].isalpha():
                    portal_name = portal_name = f"{input[row_idx][col_idx]}{input[row_idx + 1][col_idx]}"
                    portal_exit = None
                    if row_idx > 0 and input[row_idx - 1][col_idx] == ".":
                        portal_exit = (row_idx - 1, col_idx)
                    else:
                        portal_exit = (row_idx + 2, col_idx)

                    if portal_name == "AA":
                        entrance = portal_exit
                    elif portal_name == "ZZ":
                        exit = portal_exit
                    elif portal_name in unconnected_portals:
                        other_exit = unconnected_portals[portal_name]
                        if portal_name not in connected_portals:
                            connected_portals[portal_name] = [portal_exit, other_exit]
                    else:
                        unconnected_portals[portal_name] = portal_exit
            # Check for path cell
            elif input[row_idx][col_idx] == ".":
                if (row_idx, col_idx) not in path_graph:
                    path_graph[(row_idx, col_idx)] = []
                # check for neighboring path cells
                for (row_offset, col_offset) in [(1,0), (-1,0), (0,1), (0,-1)]:
                    if input[row_idx + row_offset][col_idx + col_offset] == ".":
                        path_graph[(row_idx, col_idx)].append((row_idx + row_offset, col_idx + col_offset))

    outer_portals = {}
    inner_portals = {}
    for portal_name, coordinates_list in connected_portals.items():
        for idx, (row_idx, col_idx) in enumerate(coordinates_list):
            if row_idx == 2 or row_idx == height - 3 or col_idx == 2 or col_idx == width - 3:
                outer_portals[(row_idx, col_idx)] = coordinates_list[(idx + 1) % 2]
            else:
                inner_portals[(row_idx, col_idx)] = coordinates_list[(idx + 1) % 2]

    return entrance, exit, path_graph, connected_portals, inner_portals, outer_portals


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    part2_example_input = open('./part2_example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_entrance, part1_example_exit, part1_example_path_graph = parse_input(example_input)
    part1_example_result = part1(part1_example_entrance, part1_example_exit, part1_example_path_graph)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_entrance, part1_exit, part1_path_graph = parse_input(input)
    part1_result = part1(part1_entrance, part1_exit, part1_path_graph)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part2_example_entrance, part2_example_exit, part2_example_path_graph, part2_example_portals, part2_example_inner_portals, part2_example_outer_portals = parse_input_part2(part2_example_input)
    part2_example_result = part2(part2_example_entrance, part2_example_exit, part2_example_path_graph, part2_example_portals, part2_example_inner_portals, part2_example_outer_portals)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_entrance, part2_exit, part2_path_graph, part2_portals, part2_inner_portals, part2_outer_portals = parse_input_part2(input)
    part2_result = part2(part2_entrance, part2_exit, part2_path_graph, part2_portals, part2_inner_portals, part2_outer_portals)
    print(f"Part 2: {part2_result}")

main()