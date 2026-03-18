import math
def part1(num_squares):
    # Take a mathy-based O(1) approach
    num_layers = math.ceil((math.sqrt(num_squares) - 1) / 2)
    outer_side_length = (2 * num_layers) + 1
    last_value_in_outer_layer = outer_side_length ** 2
    numbers_per_side = outer_side_length - 1

    # Check if val is bottom edge of outer layer
    if num_squares >= last_value_in_outer_layer - numbers_per_side:
        x_coord = num_layers - (last_value_in_outer_layer - num_squares)
        y_coord = -num_layers
        return abs(x_coord) + abs(y_coord)
    
    # Move to left edge and check
    last_value_in_outer_layer -= numbers_per_side
    if num_squares >= last_value_in_outer_layer - numbers_per_side:
        x_coord = -num_layers
        y_coord = -num_layers + last_value_in_outer_layer - num_squares
        return abs(x_coord) + abs(y_coord)

    # Move to top edge and check
    last_value_in_outer_layer -= numbers_per_side 
    if num_squares >= last_value_in_outer_layer - numbers_per_side:
        x_coord = -num_layers + (last_value_in_outer_layer - num_squares)
        y_coord = num_layers
        return abs(x_coord) + abs(y_coord)
    else:
        # Must be in right edge
        x_coord = num_layers
        y_coord = num_layers - (last_value_in_outer_layer - num_squares - numbers_per_side)
        return abs(x_coord) + abs(y_coord)
    
def part2(high_value):
    direction_vectors = {
        'right': (1, 0),
        'left': (-1, 0),
        'up': (0, 1),
        'down': (0, -1)
    }
    next_direction_map = {
        'right': 'up',
        'up': 'left',
        'left': 'down',
        'down': 'right'
    }
    neighbor_offsets = [
        (-1,  1), (0,  1), (1,  1),
        (-1,  0),          (1,  0),
        (-1, -1), (0, -1), (1, -1) 
    ]
    value_written = 1
    current_x, current_y = 0, 0
    coord_vals = { (0,0): 1 }
    current_direction = 'right'
    while value_written <= high_value:
        # Move to next square
        x_offset, y_offset = direction_vectors[current_direction]
        current_x += x_offset
        current_y += y_offset

        # Sum up neighbor squares to get this square's value
        this_square_value = 0
        for neightbor_x_offset, neighbor_y_offset in neighbor_offsets:
            this_square_value += coord_vals.get((current_x + neightbor_x_offset, current_y + neighbor_y_offset), 0)
        coord_vals[(current_x, current_y)] = this_square_value
        value_written = this_square_value

        # Check if we need to turn
        left_vector_x, left_vector_y = direction_vectors[next_direction_map[current_direction]]
        current_left_x = current_x + left_vector_x
        current_left_y = current_y + left_vector_y
        if (current_left_x, current_left_y) not in coord_vals:
            current_direction = next_direction_map[current_direction]

    return value_written

def main():
    # Part 1 (Example)
    part1_example_result = part1(1024)
    print(f"Part 1 (Example): {part1_example_result}")

    # Part 1
    part1_result = part1(361527)
    print(f"Part 1: {part1_result}")

    # Part 2 (Example)
    part2_example_result = part2(800)
    print(f"Part 2 (Example): {part2_example_result}")

    # Part 2
    part2_result = part2(361527)
    print(f"Part 2: {part2_result}")

main()