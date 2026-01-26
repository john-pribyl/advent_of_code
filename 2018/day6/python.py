import math
from collections import deque

def part1(input):
    left_col = math.inf
    right_col = -math.inf
    top_row = math.inf
    bottom_row = -math.inf
    nodes = []

    # Parse coordinates and determine boundaries
    for idx, line in enumerate(input):
        # 1, 2
        col_idx, row_idx = line.split(', ')
        row_idx, col_idx = int(row_idx), int(col_idx)
        top_row = min(top_row, row_idx)
        bottom_row = max(bottom_row, row_idx)
        left_col = min(left_col, col_idx)
        right_col = max(right_col, col_idx)
        nodes.append([idx, (row_idx, col_idx)])
    
    # Will hold grid coordinates as keys and tuple of (closest_node, distance) as value
    tile_map = {}
        
    # BFS to find all tiles within a given distance of nodes
    to_visit = deque()
    for node in nodes:
        node_idx, coordinates = node
        to_visit.append((coordinates, node_idx, 0))

    while len(to_visit) > 0:
        coordinates, node_idx, distance = to_visit.popleft()
        row_idx, col_idx = coordinates
        
        # Boundary check
        if row_idx < top_row or row_idx > bottom_row or col_idx < left_col or col_idx > right_col:
            continue

        # Check if we've seen these coordinates before
        if coordinates in tile_map:
            contesting_node_idx, contesting_distance = tile_map[coordinates]
            if distance < contesting_distance:
                # If current path is shorter than previous path, mark this node as closest to these coordinates
                tile_map[coordinates] = (node_idx, distance)
            # If coordinates have already been visited, make sure they have been visited from a different node.
            # Do not re-traverse '.' spaces (will result in infinite loop)
            elif distance == contesting_distance and contesting_node_idx != -1 and contesting_node_idx != node_idx:
                # If equally close, we shouldn't count it
                tile_map[coordinates] = (-1, distance)
            else:
                continue
        else:
            # If we haven't been to these coordinates yet, mark them visited
            tile_map[coordinates] = (node_idx, distance)

        # Queue up neighbors
        neighbor_offsets = [(0,-1), (0,1), (-1, 0), (1, 0)]
        for row_offset, col_offset in neighbor_offsets:
            neighbor_coordinates = (row_idx + row_offset, col_idx + col_offset)
            to_visit.append((neighbor_coordinates, node_idx, distance + 1))
    
    # For each node, get a count of how many tiles are closest to it
    closest_node_count_map = {}
    max_count = 0
    for coordinates in tile_map.keys():
        node_idx, _ = tile_map[coordinates]
        closest_node_count_map[node_idx] = closest_node_count_map.get(node_idx, 0) + 1
        max_count = max(max_count, closest_node_count_map[node_idx])

    return max_count

# Deprecated by more efficient solution below because BFS is not very good here
def part2_bfs(input, max_total_distance):
    left_col = math.inf
    right_col = -math.inf
    top_row = math.inf
    bottom_row = -math.inf
    nodes = []

    # Parse coordinates and determine boundaries
    for idx, line in enumerate(input):
        col_idx, row_idx = line.split(', ')
        row_idx, col_idx = int(row_idx), int(col_idx)
        top_row = min(top_row, row_idx)
        bottom_row = max(bottom_row, row_idx)
        left_col = min(left_col, col_idx)
        right_col = max(right_col, col_idx)
        nodes.append([idx, (row_idx, col_idx)])
    
    # Will hold grid coordinates as keys and tuple of (set(closest_node), total_distance) as value
    tile_map = {}
        
    # BFS to find all tiles within a given distance of nodes
    to_visit = deque()
    for node in nodes:
        node_idx, coordinates = node
        to_visit.append((coordinates, node_idx, 0))

    while len(to_visit) > 0:
        coordinates, node_idx, distance = to_visit.popleft()
        row_idx, col_idx = coordinates
        
        # Boundary check
        if row_idx < top_row or row_idx > bottom_row or col_idx < left_col or col_idx > right_col:
            continue

        # Check if we've seen these coordinates before
        if coordinates in tile_map:
            node_idxs, total_distance = tile_map[coordinates]
            # Check if we've already found distance between these coordinates and the given node
            if node_idx in node_idxs:
                continue

            node_idxs.add(node_idx)
            total_distance += distance
            tile_map[coordinates] = (node_idxs, total_distance)
        else:
            # If we haven't been to these coordinates yet, mark them visited
            tile_map[coordinates] = (set([node_idx]), distance)

        # Queue up neighbors
        neighbor_offsets = [(0,-1), (0,1), (-1, 0), (1, 0)]
        for row_offset, col_offset in neighbor_offsets:
            neighbor_coordinates = (row_idx + row_offset, col_idx + col_offset)
            to_visit.append((neighbor_coordinates, node_idx, distance + 1))
    
    # Filter map down to tiles with total_distance < 10_000
    filtered_tiles = {coordinates: total_distance for coordinates, (node_idxs, total_distance) in tile_map.items() if total_distance < max_total_distance}
    return len(filtered_tiles)

def part2(input, max_total_distance):
    left_col = math.inf
    right_col = -math.inf
    top_row = math.inf
    bottom_row = -math.inf
    nodes = []

    # Parse coordinates and determine boundaries
    for line in input:
        col_idx, row_idx = line.split(', ')
        row_idx, col_idx = int(row_idx), int(col_idx)
        top_row = min(top_row, row_idx)
        bottom_row = max(bottom_row, row_idx)
        left_col = min(left_col, col_idx)
        right_col = max(right_col, col_idx)
        nodes.append((row_idx, col_idx))
    
    # Will hold grid coordinates as keys and total_distance as value
    good_tile_count = 0
    for row_idx in range(top_row, bottom_row + 1):
        for col_idx in range(left_col, right_col + 1):
            total_distance = 0
            for node_row_idx, node_col_idx in nodes:
                total_distance += abs(row_idx - node_row_idx) + abs(col_idx - node_col_idx)
                if total_distance >= max_total_distance:
                    break

            if total_distance < max_total_distance:
                good_tile_count += 1

    return good_tile_count


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example (34)
    part1_example_result = part2(example_input, max_total_distance=32)
    print(f"Part 2 (example): {part1_example_result}")

    # Part 2 (92428)
    part1_result = part2(input, max_total_distance=10_000)
    print(f"Part 2: {part1_result}")


main()