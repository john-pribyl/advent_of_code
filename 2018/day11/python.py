import math

def part1(serial_number):
    cell_power_values = {}
    max_subgrid_value = 0
    max_subgrid_corner = (0,0)
    for x_val in range(1, 301):
        for y_val in range(1, 301):
            box_power_value = 0
            for box_idx in range(9):
                x_coord = x_val + (box_idx // 3)
                y_coord = y_val + (box_idx % 3)

                cell_value = 0
                if (x_coord, y_coord) in cell_power_values:
                    cell_value = cell_power_values[(x_coord, y_coord)]
                else:
                    rack_id = x_coord + 10
                    cell_value = ((((rack_id * y_coord) + serial_number) * rack_id) // 100 % 10) - 5
                    cell_power_values[(x_coord, y_coord)] = cell_value

                box_power_value += cell_value

            if box_power_value > max_subgrid_value:
                max_subgrid_value = box_power_value
                max_subgrid_corner = (x_val, y_val)

    return max_subgrid_corner

def part2(serial_number):
    cell_power_values = {}
    # Compute all the values in the grid
    for x_val in range(1, 301):
        for y_val in range(1, 301):
            rack_id = x_val + 10
            cell_value = ((((rack_id * y_val) + serial_number) * rack_id) // 100 % 10) - 5
            cell_power_values[(x_val, y_val)] = cell_value

    max_subgrid_value = 0
    max_subgrid_corner = (0,0)
    max_subgrid_dimension = 1

    previous_dimension_squares = {}
    for box_dimension in range(2, 301):
        print(f"Computing boxes of size {box_dimension}. Max so far: {max_subgrid_value} starting at {max_subgrid_corner} with dimension {max_subgrid_dimension}")
        
        this_dimension_squares = {}
        if box_dimension == 2:
            # First box size, just brute force it.
            for top_left_x in range(1, 301 - box_dimension):
                for top_left_y in range(1, 301 - box_dimension):
                    box_power_value = 0
                    for idx in range(box_dimension ** 2):
                        box_power_value += cell_power_values[(top_left_x + (idx // box_dimension), top_left_y + (idx % box_dimension))]

                    this_dimension_squares[(top_left_x, top_left_y)] = box_power_value

                    if box_power_value > max_subgrid_value:
                        max_subgrid_value = box_power_value
                        max_subgrid_corner = (top_left_x, top_left_y)
                        max_subgrid_dimension = box_dimension
        else:
            # Build these boxes from previous boxes, we just need to add the right and bottom layer
            for top_left_x in range(1, 301 - box_dimension):
                for top_left_y in range(1, 301 - box_dimension):
                    box_power_value = previous_dimension_squares[(top_left_x, top_left_y)]
                    # Add right layer
                    for y_offset in range(box_dimension):
                        box_power_value += cell_power_values[(top_left_x + box_dimension - 1, top_left_y + y_offset)]
                    # Add bottom layer
                    for x_offset in range(box_dimension - 1):
                        box_power_value += cell_power_values[(top_left_x + x_offset, top_left_y + box_dimension - 1)]

                    this_dimension_squares[(top_left_x, top_left_y)] = box_power_value

                    if box_power_value > max_subgrid_value:
                        max_subgrid_value = box_power_value
                        max_subgrid_corner = (top_left_x, top_left_y)
                        max_subgrid_dimension = box_dimension

        previous_dimension_squares = this_dimension_squares

    return max_subgrid_corner, max_subgrid_dimension

def part2_sat(serial_number):
    summed_area_table = [[0] * 301 for _ in range(301)]

    # Compute each cell's value as in part 1 and construct a Summed Area Table
    # A variant of prefix sums
    for x_val in range(1, 301):
        for y_val in range(1, 301):
            rack_id = (x_val + 1) + 10
            cell_value = ((((rack_id * (y_val + 1)) + serial_number) * rack_id) // 100 % 10) - 5
            sat_value = summed_area_table[x_val][y_val - 1] \
                + summed_area_table[x_val - 1][y_val] \
                - summed_area_table[x_val - 1][y_val - 1] \
                + cell_value
            summed_area_table[x_val][y_val] = sat_value
    
    # Use SAT to calculate all box sums of all sizes. Can compute each box in O(1) time
    max_box_value = 0
    max_box_corner = (0,0)
    max_box_dimension = 1
    for box_dimension in range(2, 301):
        for x_val in range(1, 301 - box_dimension):
            for y_val in range(1, 301 - box_dimension):
                box_value = summed_area_table[x_val + box_dimension - 1][y_val + box_dimension - 1] \
                    - summed_area_table[x_val + box_dimension - 1][y_val - 1] \
                    - summed_area_table[x_val - 1][y_val + box_dimension - 1] \
                    + summed_area_table[x_val - 1][y_val - 1]
                
                if box_value >= max_box_value:
                    max_box_value = box_value
                    max_box_corner = (x_val + 1, y_val + 1)
                    max_box_dimension = box_dimension

    return max_box_corner, max_box_dimension
                    
def main():
    # # Part 1 example 1
    # part1_example_result = part1(18)
    # print(f"Part 1 (example): {part1_example_result}")

    # # Part 1 example 2
    # part1_example2_result = part1(42)
    # print(f"Part 1 (example): {part1_example2_result}")

    # # Part 1 example 2
    # part1_result = part1(5153)
    # print(f"Part 1 (example): {part1_result}")

    # Part 2 example 1
    # part2_example_result = part2(42)
    # print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2_sat(5153)
    print(f"Part 2: {part2_result}")



main()