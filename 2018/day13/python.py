import copy

DIRECTION_DELTAS = {
    'right': (0, 1),
    'left': (0, -1),
    'up': (-1, 0),
    'down': (1, 0)
}

DIRECTIONS = {
    '^': 'up',
    'v': 'down',
    '>': 'right',
    '<': 'left'
}

TURNS = ['left', 'straight', 'right']

LEFT_TURNS = {
    'left': 'down',
    'down': 'right',
    'right': 'up',
    'up': 'left'
}

RIGHT_TURNS = {
    'right': 'down',
    'down': 'left',
    'left': 'up',
    'up': 'right'
}

CORNERS = {
    '/': {
        'up': 'right',
        'down': 'left',
        'right': 'up',
        'left': 'down'
    },
    '\\': {
        'up': 'left',
        'down': 'right',
        'right': 'down',
        'left': 'up'
    }
}

class Cart:
    def __init__(self, direction):
        self.direction = direction
        self.next_turn = 'left'

# Does part 1 as well
def part2(grid):
    # First scan, find the carts
    occupied_positions = {}
    num_carts = 0
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[0])):
            if grid[row_idx][col_idx] in DIRECTIONS:
                occupied_positions[(int(row_idx), int(col_idx))] = Cart(DIRECTIONS[grid[row_idx][col_idx]])
                num_carts += 1

    # Simulate cart movement
    part1_result = None
    while num_carts > 1:
        cart_positions = sorted(copy.copy(list(occupied_positions.items())))
        crash_coordinates = set([])
        for (cart_row, cart_col), cart_info in cart_positions:
            # Remove cart from its current space
            if (cart_row, cart_col) in occupied_positions:
                del occupied_positions[(cart_row, cart_col)]

            # Check if an earlier cart crashed into this one already
            if (cart_row, cart_col) in crash_coordinates:
                continue

            # Calculate new space
            row_delta, col_delta = DIRECTION_DELTAS[cart_info.direction]
            cart_row += row_delta
            cart_col += col_delta
            
            # Check for collision with another cart
            if (cart_row, cart_col) in occupied_positions:
                # Delete the other cart at this position and don't continue with this cart
                del occupied_positions[(cart_row, cart_col)]
                crash_coordinates.add((cart_row, cart_col))
                num_carts -= 2

                if not part1_result:
                    part1_result = (cart_col, cart_row)
                continue

            # Check for corner
            if grid[cart_row][cart_col] in CORNERS:
                cart_info.direction = CORNERS[grid[cart_row][cart_col]][cart_info.direction]

            # Check for intersection
            if grid[cart_row][cart_col] == '+':
                if cart_info.next_turn == 'left':
                    cart_info.direction = LEFT_TURNS[cart_info.direction]
                    cart_info.next_turn = 'straight'
                elif cart_info.next_turn == 'right':
                    cart_info.direction = RIGHT_TURNS[cart_info.direction]
                    cart_info.next_turn = 'left'
                else:
                    cart_info.next_turn = 'right'

            # Update cart's new space
            occupied_positions[(cart_row, cart_col)] = cart_info

    part2_result = None
    if len(list(occupied_positions.items())) > 0:
        (last_cart_row_idx, last_cart_col_idx), _ = list(occupied_positions.items())[0]
        part2_result = (last_cart_col_idx, last_cart_row_idx)
    return part1_result, part2_result


def main():
    part1_example_input = open('./part1_example.txt', 'r').read().split('\n')
    part2_example_input = open('./part2_example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result, _ = part2(part1_example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 2 Example
    _, part2_example_result = part2(part2_example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1
    part1_result, part2_result = part2(input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")


main()