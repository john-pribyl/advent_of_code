def part1(input):
    # Parse input to coordinates
    parsed_input = []
    for line in input:
        x_coord, y_coord = line.split(',')
        x_coord, y_coord = int(x_coord), int(y_coord)
        parsed_input.append((x_coord, y_coord))

    # Compute all pair-wise rectangle areas
    max_area = 0
    for x1_coord, y1_coord in parsed_input:
        for x2_coord, y2_coord in parsed_input:
            width = abs(x2_coord - x1_coord + 1)
            height = abs(y2_coord - y1_coord + 1)
            area = width * height
            max_area = max(max_area, area)

    return max_area

def part2(input):
    # Parse input to coordinates
    parsed_input = []
    for line in input:
        x_coord, y_coord = line.split(',')
        x_coord, y_coord = int(x_coord), int(y_coord)
        parsed_input.append((x_coord, y_coord))

    corner_tiles = []
    # Get red corner tiles
    for line in parsed_input:
        x_coord, y_coord = line
        corner_tiles.append((x_coord, y_coord))

    # Compute all boundary edges
    # When we start making our rectangles, we'll want to check if they are intersected by these edges
    vertical_edges = {} # Hash by column (will speed up lookups later)
    horizontal_edges = {} # Hash by row (will speed up lookups later)
    for idx in range(len(corner_tiles)):
        this_corner_x, this_corner_y = corner_tiles[idx]
        next_corner_x, next_corner_y = corner_tiles[(idx + 1) % len(corner_tiles)] # Modulus to handle wrapping at the end

        if this_corner_x == next_corner_x:
            # vertical edge
            y_min = min(this_corner_y, next_corner_y)
            y_max = max(this_corner_y, next_corner_y)
            vertical_edges.setdefault(this_corner_x, []).append((y_min, y_max))
        elif this_corner_y == next_corner_y:
            # horizontal edge
            x_min = min(this_corner_x, next_corner_x)
            x_max = max(this_corner_x, next_corner_x)
            horizontal_edges.setdefault(this_corner_y, []).append((x_min, x_max)) 
                 

    # Compute all pair-wise rectangle areas
    max_area = 0
    for x1_coord, y1_coord in parsed_input:
        for x2_coord, y2_coord in parsed_input:
            x_min = min(x1_coord, x2_coord)
            x_max = max(x1_coord, x2_coord)
            y_min = min(y1_coord, y2_coord)
            y_max = max(y1_coord, y2_coord)

            rect_is_valid = True
            # check for intersecting vertical edge
            for vertical_edge_x, edges in vertical_edges.items():
                if x_min < vertical_edge_x < x_max:
                    # Some vertical edge exists between rectang'es left and right boundaries
                    # Check if one of the edges intersects the top or bottom boundary of rectanble
                    # (Edge may completely miss the rectangle)
                    for vertical_edge_y_min, vertical_edge_y_max in edges:
                        if vertical_edge_y_min < y_max and y_min < vertical_edge_y_max:
                            rect_is_valid = False
                            break
                        
            # Check for intersecting horizontal edge
            for horizontal_edge_y, edges in horizontal_edges.items():
                if y_min < horizontal_edge_y < y_max:
                    # Some horizontal edge exists between rectang'es top and bottom boundaries
                    # Check if one of the edges intersects the right or left boundary of rectanble
                    # (Edge may completely miss the rectangle)
                    for horizontal_edge_x_min, horizontal_edge_x_max in edges:
                        if horizontal_edge_x_min < x_max and x_min < horizontal_edge_x_max:
                            rect_is_valid = False
                            break

            if rect_is_valid:
                width = abs(x2_coord - x1_coord) + 1
                height = abs(y2_coord - y1_coord) + 1
                area = width * height
                max_area = max(max_area, area)

    return max_area

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part2_example_result = part2(example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2(input)
    print(f"Part 2: {part2_result}")

main()